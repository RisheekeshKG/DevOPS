"""Tests for sensor data generation."""

import pytest
from sensor_data_gen import SensorSimulator, SensorReading


class TestSensorSimulator:
    """Test sensor simulator functionality."""

    @pytest.fixture
    def simulator(self):
        return SensorSimulator("P001")

    def test_initialization(self, simulator):
        assert simulator.patient_id == "P001"
        assert simulator.ward == "medical"
        assert simulator.bed == "B1"

    def test_generate_normal_scenario(self, simulator):
        reading = simulator.generate("normal")
        assert isinstance(reading, SensorReading)
        assert reading.patient_id == "P001"
        assert 35 <= reading.hr <= 210
        assert 70 <= reading.spo2 <= 100
        assert 34.0 <= reading.temp <= 41.0
        assert 70 <= reading.bp_sys <= 200
        assert 40 <= reading.bp_dia <= 140

    def test_generate_admission_scenario(self, simulator):
        reading = simulator.generate("admission")
        assert simulator.ward == "emergency"
        assert simulator.unit == "triage"
        assert reading.scenario == "admission"

    def test_generate_post_op_scenario(self, simulator):
        reading = simulator.generate("post_op")
        assert simulator.ward == "surgical"
        assert simulator.unit == "recovery"

    def test_generate_icu_scenario(self, simulator):
        reading = simulator.generate("icu_monitoring")
        assert simulator.ward == "icu"
        assert simulator.unit == "critical_care"

    def test_generate_night_rounds(self, simulator):
        reading = simulator.generate("night_rounds")
        assert simulator.ward == "medical"
        assert simulator.unit == "overnight"

    def test_to_dict(self, simulator):
        reading = simulator.generate("normal")
        data = reading.to_dict()
        assert isinstance(data, dict)
        assert "patient_id" in data
        assert "hr" in data
        assert "spo2" in data
        assert "bp_sys" in data
        assert "bp_dia" in data
        assert data["patient_id"] == "P001"

    def test_different_patients(self):
        sim1 = SensorSimulator("P001")
        sim2 = SensorSimulator("P002")
        assert sim1.bed == "B1"
        assert sim2.bed == "B2"

    def test_timestamp_generation(self, simulator):
        import time
        before = int(time.time())
        reading = simulator.generate("normal")
        after = int(time.time())
        assert before <= reading.timestamp <= after

    def test_ecg_range(self, simulator):
        reading = simulator.generate("normal")
        assert 0 <= reading.ecg <= 300
