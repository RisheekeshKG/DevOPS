"""Main workflow that generates data, labels it, and stores it in InfluxDB."""

import logging
import os
import threading
import time
from typing import List, Optional

from influxDB import InfluxDBWriter
from kafka_prod_cons import KafkaProdCons, RiskLabeler
from sensor_data_gen import SensorSimulator


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


class PatientMonitoringWorkflow:
    def __init__(
        self,
        kafka_servers: str,
        topic: str,
        patients: Optional[List[str]],
        influx_url: str,
        influx_token: str,
        influx_org: str,
        influx_bucket: str,
    ):
        self.kafka_servers = kafka_servers
        self.topic = topic
        self.patients = patients or ["P001", "P002", "P003"]

        self.simulators = {pid: SensorSimulator(pid) for pid in self.patients}
        self.influx = InfluxDBWriter(influx_url, influx_token, influx_org, influx_bucket)
        self.kafka = KafkaProdCons(bootstrap_servers=kafka_servers, topic=topic)
        self.stop_event = threading.Event()

    def _scenario_for_elapsed(self, elapsed: float, duration: int) -> str:
        if elapsed < duration * 0.25:
            return "admission"
        if elapsed < duration * 0.50:
            return "post_op"
        if elapsed < duration * 0.75:
            return "icu_monitoring"
        return "night_rounds"

    def producer_loop(self, duration: Optional[int], interval: float) -> None:
        start = time.time()
        sent = 0
        try:
            while not self.stop_event.is_set() and (duration is None or duration <= 0 or (time.time() - start) < duration):
                elapsed = time.time() - start
                scenario = self._scenario_for_elapsed(elapsed, duration) if duration and duration > 0 else ["admission", "post_op", "icu_monitoring", "night_rounds"][int(elapsed) % 4]

                for patient_id, simulator in self.simulators.items():
                    reading = simulator.generate(scenario).to_dict()
                    self.kafka.publish(key=patient_id, value=reading)
                    sent += 1

                self.kafka.flush()
                time.sleep(interval)
        finally:
            logger.info("Producer loop complete, sent=%d", sent)
            self.stop_event.set()

    def consumer_loop(self) -> None:
        processed = 0
        while not self.stop_event.is_set():
            for message in self.kafka.consumer:
                reading = message.value
                score = RiskLabeler.score(reading)
                label = RiskLabeler.label(score)

                ok = self.influx.write(reading, score, label)
                processed += 1

                logger.info(
                    "patient=%s hr=%s spo2=%s temp=%s risk=%.2f label=%s influx=%s",
                    reading.get("patient_id"),
                    reading.get("hr"),
                    reading.get("spo2"),
                    reading.get("temp"),
                    score,
                    label,
                    "ok" if ok else "failed",
                )

                if self.stop_event.is_set():
                    break

        logger.info("Consumer loop complete, processed=%d", processed)

    def run(self, duration: Optional[int] = None, interval: float = 1.0) -> None:
        runtime = "continuous" if not duration or duration <= 0 else f"{duration}s"
        logger.info("Starting workflow for %s, patients=%s", runtime, self.patients)

        producer_thread = threading.Thread(target=self.producer_loop, args=(duration, interval), name="producer")
        consumer_thread = threading.Thread(target=self.consumer_loop, name="consumer")

        consumer_thread.start()
        producer_thread.start()

        producer_thread.join()
        self.stop_event.set()
        consumer_thread.join(timeout=5)

        self.cleanup()
        logger.info("Workflow completed")

    def cleanup(self) -> None:
        self.kafka.close()


def main() -> None:
    duration_value = int(os.getenv("WORKFLOW_DURATION_SECONDS", "0"))
    workflow = PatientMonitoringWorkflow(
        kafka_servers=os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092"),
        topic=os.getenv("KAFKA_TOPIC", "sensor-data"),
        patients=os.getenv("PATIENT_IDS", "P001,P002,P003").split(","),
        influx_url=os.getenv("INFLUXDB_URL", "http://localhost:8086"),
        influx_token=os.getenv("INFLUXDB_TOKEN", "devops-token"),
        influx_org=os.getenv("INFLUXDB_ORG", "devops-org"),
        influx_bucket=os.getenv("INFLUXDB_BUCKET", "patient_vitals"),
    )
    workflow.run(
        duration=duration_value if duration_value > 0 else None,
        interval=float(os.getenv("WORKFLOW_INTERVAL_SECONDS", "1.0")),
    )


if __name__ == "__main__":
    main()
