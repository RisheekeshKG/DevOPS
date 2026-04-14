"""Sensor data generation utilities."""

import random
import time
from dataclasses import dataclass
from typing import Dict


@dataclass
class SensorReading:
    patient_id: str
    ward: str
    bed: str
    unit: str
    scenario: str
    hr: int
    spo2: int
    temp: float
    ecg: int
    bp_sys: int
    bp_dia: int
    timestamp: int

    def to_dict(self) -> Dict[str, object]:
        return {
            "patient_id": self.patient_id,
            "ward": self.ward,
            "bed": self.bed,
            "unit": self.unit,
            "scenario": self.scenario,
            "hr": self.hr,
            "spo2": self.spo2,
            "temp": self.temp,
            "ecg": self.ecg,
            "bp_sys": self.bp_sys,
            "bp_dia": self.bp_dia,
            "timestamp": self.timestamp,
        }


class SensorSimulator:
    """Generates realistic hospital telemetry with scenario variation."""

    def __init__(self, patient_id: str):
        self.patient_id = patient_id
        self.ward = "medical"
        self.bed = f"B{patient_id[-1]}"
        self.unit = "general_ward"
        self.base = {
            "hr": 72,
            "spo2": 98,
            "temp": 37.0,
            "bp_sys": 112,
            "bp_dia": 72,
        }

    @staticmethod
    def _clamp(value: float, low: float, high: float) -> float:
        return max(low, min(high, value))

    def generate(self, scenario: str = "normal") -> SensorReading:
        if scenario == "admission":
            self.ward = "emergency"
            self.unit = "triage"
            hr = int(random.gauss(self.base["hr"] + 8, 4))
            spo2 = int(random.gauss(self.base["spo2"] - 1, 1))
            temp = random.gauss(self.base["temp"] + 0.3, 0.12)
            bp_sys = int(random.gauss(self.base["bp_sys"] + 6, 4))
            bp_dia = int(random.gauss(self.base["bp_dia"] + 4, 3))
            ecg = random.randint(70, 150)
        elif scenario == "post_op":
            self.ward = "surgical"
            self.unit = "recovery"
            hr = int(random.gauss(self.base["hr"] + 12, 5))
            spo2 = int(random.gauss(self.base["spo2"] - 2, 1))
            temp = random.gauss(self.base["temp"] + 0.5, 0.15)
            bp_sys = int(random.gauss(self.base["bp_sys"] + 10, 5))
            bp_dia = int(random.gauss(self.base["bp_dia"] + 6, 3))
            ecg = random.randint(85, 165)
        elif scenario == "icu_monitoring":
            self.ward = "icu"
            self.unit = "critical_care"
            hr = int(random.gauss(self.base["hr"] + 18, 7))
            spo2 = int(random.gauss(self.base["spo2"] - 4, 2))
            temp = random.gauss(self.base["temp"] + 0.7, 0.2)
            bp_sys = int(random.gauss(self.base["bp_sys"] - 8, 7))
            bp_dia = int(random.gauss(self.base["bp_dia"] - 4, 4))
            ecg = random.randint(95, 185)
        elif scenario == "night_rounds":
            self.ward = "medical"
            self.unit = "overnight"
            hr = int(random.gauss(self.base["hr"] - 3, 3))
            spo2 = int(random.gauss(self.base["spo2"], 1))
            temp = random.gauss(self.base["temp"] + 0.05, 0.08)
            bp_sys = int(random.gauss(self.base["bp_sys"] - 2, 3))
            bp_dia = int(random.gauss(self.base["bp_dia"] - 1, 2))
            ecg = random.randint(55, 130)
        else:
            self.ward = "medical"
            self.unit = "general_ward"
            hr = int(random.gauss(self.base["hr"], 2.5))
            spo2 = int(random.gauss(self.base["spo2"], 1))
            temp = random.gauss(self.base["temp"], 0.12)
            bp_sys = int(random.gauss(self.base["bp_sys"], 3))
            bp_dia = int(random.gauss(self.base["bp_dia"], 2.5))
            ecg = random.randint(50, 150)

        return SensorReading(
            patient_id=self.patient_id,
            ward=self.ward,
            bed=self.bed,
            unit=self.unit,
            scenario=scenario,
            hr=int(self._clamp(hr, 35, 210)),
            spo2=int(self._clamp(spo2, 70, 100)),
            temp=round(float(self._clamp(temp, 34.0, 41.0)), 2),
            ecg=int(self._clamp(ecg, 0, 300)),
            bp_sys=int(self._clamp(bp_sys, 70, 200)),
            bp_dia=int(self._clamp(bp_dia, 40, 140)),
            timestamp=int(time.time()),
        )
