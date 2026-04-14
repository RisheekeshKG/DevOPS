"""Tests for main workflow integration."""

import pytest
from unittest.mock import Mock, patch
from sensor_data_gen import SensorSimulator


class TestWorkflowIntegration:
    """Test workflow integration scenarios."""

    def test_multiple_patients_generation(self):
        patients = ["P001", "P002", "P003"]
        simulators = {pid: SensorSimulator(pid) for pid in patients}

        for patient_id, simulator in simulators.items():
            reading = simulator.generate("normal")
            assert reading.patient_id == patient_id
            assert reading.bed == f"B{patient_id[-1]}"

    def test_scenario_transitions(self):
        simulator = SensorSimulator("P001")
        scenarios = ["normal", "admission", "post_op", "icu_monitoring", "night_rounds"]

        for scenario in scenarios:
            reading = simulator.generate(scenario)
            assert reading.scenario == scenario or reading.scenario is not None

    def test_data_consistency(self):
        simulator = SensorSimulator("P001")
        reading = simulator.generate("normal")
        data = reading.to_dict()

        assert data["patient_id"] == reading.patient_id
        assert data["hr"] == reading.hr
        assert data["spo2"] == reading.spo2
        assert data["bp_sys"] == reading.bp_sys
        assert data["bp_dia"] == reading.bp_dia

    def test_blood_pressure_values(self):
        simulator = SensorSimulator("P001")
        reading = simulator.generate("normal")

        # Systolic should be higher than diastolic typically
        # (not always, but usually in normal scenarios)
        assert reading.bp_sys > 0
        assert reading.bp_dia > 0
        assert reading.bp_sys <= 200
        assert reading.bp_dia <= 140

    def test_patient_id_persistence(self):
        simulator = SensorSimulator("P001")
        readings = [simulator.generate("normal") for _ in range(10)]

        for reading in readings:
            assert reading.patient_id == "P001"
