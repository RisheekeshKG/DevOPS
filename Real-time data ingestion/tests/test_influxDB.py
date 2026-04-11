"""Tests for InfluxDB writer."""

import pytest
from influxDB import InfluxDBWriter


class TestInfluxDBWriter:
    """Test InfluxDB line protocol generation."""

    @pytest.fixture
    def writer(self):
        return InfluxDBWriter(
            url="http://localhost:8086",
            token="test-token",
            org="test-org",
            bucket="test-bucket",
        )

    def test_line_protocol_generation(self, writer):
        reading = {
            "patient_id": "P001",
            "ward": "medical",
            "bed": "B1",
            "unit": "general_ward",
            "scenario": "normal",
            "hr": 75,
            "spo2": 98,
            "temp": 37.0,
            "ecg": 90,
            "bp_sys": 120,
            "bp_dia": 80,
            "timestamp": 1712345678,
        }
        line = writer._line_protocol(reading, 0.25, "low")

        assert "patient_vitals" in line
        assert "patient_id=P001" in line
        assert "hr=75i" in line
        assert "spo2=98i" in line
        assert "bp_sys=120i" in line
        assert "bp_dia=80i" in line
        assert "risk_score=0.25" in line
        assert "risk_label=low" in line

    def test_escape_special_characters(self, writer):
        escaped = writer._escape("test value")
        assert escaped == "test\\ value"

        escaped = writer._escape("test,value")
        assert escaped == "test\\,value"

    def test_timestamp_conversion(self, writer):
        reading = {
            "patient_id": "P001",
            "ward": "medical",
            "bed": "B1",
            "unit": "general_ward",
            "scenario": "normal",
            "hr": 75,
            "spo2": 98,
            "temp": 37.0,
            "ecg": 90,
            "bp_sys": 120,
            "bp_dia": 80,
            "timestamp": 1712345678,
        }
        line = writer._line_protocol(reading, 0.0, "low")
        # Timestamp should be in nanoseconds
        assert "1712345678000000000" in line

    def test_all_vital_signs_present(self, writer):
        reading = {
            "patient_id": "P001",
            "ward": "medical",
            "bed": "B1",
            "unit": "general_ward",
            "scenario": "normal",
            "hr": 75,
            "spo2": 98,
            "temp": 37.0,
            "ecg": 90,
            "bp_sys": 120,
            "bp_dia": 80,
            "timestamp": 1712345678,
        }
        line = writer._line_protocol(reading, 0.5, "medium")

        # All vital signs should be in the line protocol
        assert "hr=75i" in line
        assert "spo2=98i" in line
        assert "temp=37.0" in line
        assert "ecg=90i" in line
        assert "bp_sys=120i" in line
        assert "bp_dia=80i" in line

    def test_different_risk_labels(self, writer):
        reading = {
            "patient_id": "P001",
            "ward": "medical",
            "bed": "B1",
            "unit": "general_ward",
            "scenario": "normal",
            "hr": 75,
            "spo2": 98,
            "temp": 37.0,
            "ecg": 90,
            "bp_sys": 120,
            "bp_dia": 80,
            "timestamp": 1712345678,
        }

        line_low = writer._line_protocol(reading, 0.2, "low")
        line_medium = writer._line_protocol(reading, 0.5, "medium")
        line_high = writer._line_protocol(reading, 0.8, "high")

        assert "risk_label=low" in line_low
        assert "risk_label=medium" in line_medium
        assert "risk_label=high" in line_high
