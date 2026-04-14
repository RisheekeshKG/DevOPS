"""InfluxDB write helpers."""

import logging
import urllib.error
import urllib.parse
import urllib.request
from typing import Dict


logger = logging.getLogger(__name__)


class InfluxDBWriter:
    """Writes measurements to InfluxDB v2 using line protocol over HTTP."""

    def __init__(self, url: str, token: str, org: str, bucket: str, simulation_mode: bool = False):
        self.url = url.rstrip("/")
        self.token = token
        self.org = org
        self.bucket = bucket
        self.simulation_mode = simulation_mode
        if self.simulation_mode:
            logger.info("InfluxDBWriter: Running in PROXY/SIMULATION mode. Data will not be written to DB.")

    @staticmethod
    def _escape(value: str) -> str:
        return str(value).replace(" ", "\\ ").replace(",", "\\,").replace("=", "\\=")

    def _vitals_line_protocol(self, reading: Dict[str, object], score: float, label: str) -> str:
        patient_id = self._escape(reading["patient_id"])
        ward = self._escape(reading.get("ward", "medical"))
        bed = self._escape(reading.get("bed", "unknown"))
        unit = self._escape(reading.get("unit", "general_ward"))
        scenario = self._escape(reading.get("scenario", "general_care"))
        risk_label = self._escape(label)
        measurement = "patient_vitals"
        tags = f"patient_id={patient_id},ward={ward},bed={bed},unit={unit},scenario={scenario},risk_label={risk_label}"
        fields = (
            f"hr={int(reading['hr'])}i,"
            f"spo2={int(reading['spo2'])}i,"
            f"temp={float(reading['temp'])},"
            f"ecg={int(reading['ecg'])}i,"
            f"bp_sys={int(reading['bp_sys'])}i,"
            f"bp_dia={int(reading['bp_dia'])}i,"
            f"risk_score={score}"
        )
        timestamp_ns = int(reading["timestamp"]) * 1_000_000_000
        return f"{measurement},{tags} {fields} {timestamp_ns}"

    def _generic_line_protocol(self, measurement: str, tags: Dict[str, str], fields: Dict[str, object]) -> str:
        tag_str = ",".join([f"{self._escape(k)}={self._escape(v)}" for k, v in tags.items()])
        
        field_list = []
        for k, v in fields.items():
            if isinstance(v, int):
                field_list.append(f"{self._escape(k)}={v}i")
            elif isinstance(v, float):
                field_list.append(f"{self._escape(k)}={v}")
            else:
                field_list.append(f"{self._escape(k)}=\"{self._escape(str(v))}\"")
        field_str = ",".join(field_list)
        
        return f"{self._escape(measurement)},{tag_str} {field_str}"

    def write(self, reading: Dict[str, object], score: float, label: str) -> bool:
        lp = self._vitals_line_protocol(reading, score, label)
        return self._send_to_influx(lp)

    def write_metric(self, measurement: str, tags: Dict[str, str], fields: Dict[str, object]) -> bool:
        lp = self._generic_line_protocol(measurement, tags, fields)
        return self._send_to_influx(lp)

    def _send_to_influx(self, lp_content: str) -> bool:
        if self.simulation_mode:
            # In simulation mode, we just log the line protocol at debug level
            logger.debug("SIMULATION: [InfluxDB LP] %s", lp_content)
            return True

        query = urllib.parse.urlencode({"org": self.org, "bucket": self.bucket, "precision": "ns"})
        endpoint = f"{self.url}/api/v2/write?{query}"

        req = urllib.request.Request(endpoint, data=lp_content.encode("utf-8"), method="POST")
        req.add_header("Authorization", f"Token {self.token}")
        req.add_header("Content-Type", "text/plain; charset=utf-8")

        try:
            with urllib.request.urlopen(req, timeout=5):
                return True
        except urllib.error.HTTPError as exc:
            logger.error(
                "InfluxDB write failed: status=%s body=%s",
                exc.code,
                exc.read().decode("utf-8", errors="ignore"),
            )
            return False
        except Exception as exc:
            logger.error("InfluxDB write failed: %s", exc)
            return False
