"""Tests for risk labeling and model predictor."""

import pytest
from kafka_prod_cons import RiskLabeler


class TestRiskLabeler:
    """Test risk labeling logic."""

    def test_low_risk_normal_reading(self):
        reading = {
            "hr": 72,
            "spo2": 98,
            "temp": 37.0,
            "bp_sys": 112,
            "bp_dia": 72,
        }
        score = RiskLabeler.score(reading)
        label = RiskLabeler.label(score)
        assert label == "low"
        assert score < 0.35

    def test_high_risk_low_spo2(self):
        reading = {
            "hr": 90,
            "spo2": 85,
            "temp": 37.0,
            "bp_sys": 120,
            "bp_dia": 80,
        }
        score = RiskLabeler.score(reading)
        assert score >= 0.35

    def test_high_risk_extreme_hr(self):
        reading = {
            "hr": 130,
            "spo2": 98,
            "temp": 37.0,
            "bp_sys": 120,
            "bp_dia": 80,
        }
        score = RiskLabeler.score(reading)
        assert score >= 0.25

    def test_high_risk_abnormal_temp(self):
        reading = {
            "hr": 72,
            "spo2": 98,
            "temp": 39.0,
            "bp_sys": 120,
            "bp_dia": 80,
        }
        score = RiskLabeler.score(reading)
        assert score >= 0.20

    def test_high_risk_abnormal_bp(self):
        reading = {
            "hr": 72,
            "spo2": 98,
            "temp": 37.0,
            "bp_sys": 170,
            "bp_dia": 105,
        }
        score = RiskLabeler.score(reading)
        assert score >= 0.20

    def test_multiple_risk_factors(self):
        reading = {
            "hr": 130,
            "spo2": 85,
            "temp": 39.0,
            "bp_sys": 170,
            "bp_dia": 105,
        }
        score = RiskLabeler.score(reading)
        label = RiskLabeler.label(score)
        assert label == "high"
        assert score > 0.70

    def test_label_boundaries(self):
        assert RiskLabeler.label(0.0) == "low"
        assert RiskLabeler.label(0.34) == "low"
        assert RiskLabeler.label(0.35) == "medium"
        assert RiskLabeler.label(0.69) == "medium"
        assert RiskLabeler.label(0.70) == "high"
        assert RiskLabeler.label(1.0) == "high"

    def test_score_capped_at_1(self):
        reading = {
            "hr": 200,
            "spo2": 70,
            "temp": 41.0,
            "bp_sys": 200,
            "bp_dia": 140,
        }
        score = RiskLabeler.score(reading)
        assert score <= 1.0

    def test_missing_fields_defaults(self):
        reading = {}
        score = RiskLabeler.score(reading)
        label = RiskLabeler.label(score)
        assert label == "low"
