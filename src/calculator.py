from __future__ import annotations

from typing import Callable, Dict, List

import pandas as pd


def _gt(value: float, threshold: float) -> bool:
    return value > threshold


def _gte(value: float, threshold: float) -> bool:
    return value >= threshold


def _lte(value: float, threshold: float) -> bool:
    return value <= threshold


BASIC_FACTORS: List[Dict] = [
    {
        "key": "age",
        "label": "Age",
        "threshold": "> 39 years",
        "rule": lambda x: _gt(x, 39),
    },
    {
        "key": "gcs",
        "label": "Glasgow Coma Scale",
        "threshold": "≤ 8",
        "rule": lambda x: _lte(x, 8),
    },
    {
        "key": "rotterdam",
        "label": "Rotterdam CT score",
        "threshold": "> 3",
        "rule": lambda x: _gt(x, 3),
    },
    {
        "key": "hemoglobin",
        "label": "Hemoglobin",
        "threshold": "< 7.5 g/dL",
        "rule": lambda x: x < 7.5,
    },
    {
        "key": "glucose",
        "label": "Glucose",
        "threshold": "> 200 mg/dL",
        "rule": lambda x: _gt(x, 200),
    },
    {
        "key": "nlr",
        "label": "Neutrophil-to-lymphocyte ratio",
        "threshold": "> 7.44",
        "rule": lambda x: _gt(x, 7.44),
    },
    {
        "key": "plr",
        "label": "Platelet-to-lymphocyte ratio",
        "threshold": "≥ 190",
        "rule": lambda x: _gte(x, 190),
    },
]

INTERMEDIATE_FACTORS: List[Dict] = [
    {
        "key": "d_dimer",
        "label": "D-dimer",
        "threshold": "> 5 mg/L",
        "rule": lambda x: _gt(x, 5),
    },
    {
        "key": "il6",
        "label": "IL-6",
        "threshold": "> 59 pg/mL",
        "rule": lambda x: _gt(x, 59),
    },
]

ADVANCED_FACTORS: List[Dict] = [
    {
        "key": "s100b",
        "label": "S100B",
        "threshold": "> 0.10 µg/L",
        "rule": lambda x: _gt(x, 0.10),
    },
    {
        "key": "nse",
        "label": "NSE",
        "threshold": "> 33 µg/L",
        "rule": lambda x: _gt(x, 33),
    },
    {
        "key": "gfap_ug",
        "label": "GFAP",
        "threshold": "> 0.68 µg/L",
        "rule": lambda x: _gt(x, 0.68),
    },
    {
        "key": "gfap_pg",
        "label": "GFAP",
        "threshold": "> 15,000 pg/mL",
        "rule": lambda x: _gt(x, 15000),
    },
    {
        "key": "copeptin",
        "label": "Copeptin",
        "threshold": "> 451.8 pg/mL",
        "rule": lambda x: _gt(x, 451.8),
    },
    {
        "key": "crp_albumin",
        "label": "CRP/Albumin ratio",
        "threshold": "> 0.38",
        "rule": lambda x: _gt(x, 0.38),
    },
]


def evaluate_tier(values: Dict[str, float], factors: List[Dict]) -> pd.DataFrame:
    rows = []
    for factor in factors:
        key = factor["key"]
        value = values.get(key)
        triggered = bool(factor["rule"](value))
        rows.append(
            {
                "Factor": factor["label"],
                "Observed value": value,
                "Candidate threshold": factor["threshold"],
                "Triggered": "Yes" if triggered else "No",
            }
        )
    return pd.DataFrame(rows)


def overall_summary(result: pd.DataFrame) -> Dict[str, float]:
    total = len(result)
    triggered = int((result["Triggered"] == "Yes").sum())
    return {
        "total": total,
        "triggered": triggered,
        "proportion": triggered / total if total else 0.0,
    }
