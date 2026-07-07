# INA-TBI Calculator

A transparent, rule-based **prototype prognostic calculator for traumatic brain injury (TBI)**.

The application organizes candidate prognostic factors into three tiers according to data availability:

- **Basic:** routinely available clinical, imaging, and laboratory variables
- **Intermediate:** adds selected inflammatory and coagulation biomarkers
- **Advanced:** adds selected neurological injury biomarkers

> **Important:** This repository is a research and demonstration prototype. It is not clinically validated and must not be used for diagnosis, treatment decisions, triage, prognostication, or patient counselling.

## Repository structure

```text
ina-tbi-calculator/
├── app.py
├── src/
│   ├── __init__.py
│   └── calculator.py
├── data/
│   └── README.md
├── README.md
├── requirements.txt
├── CITATION.cff
└── LICENSE
```

## Candidate factors in the prototype

### Basic tier

| Factor | Candidate threshold |
|---|---:|
| Age | > 39 years |
| Glasgow Coma Scale | ≤ 8 |
| Rotterdam CT score | > 3 |
| Hemoglobin | < 7.5 g/dL |
| Glucose | > 200 mg/dL |
| Neutrophil-to-lymphocyte ratio | > 7.44 |
| Platelet-to-lymphocyte ratio | ≥ 190 |

### Intermediate tier

Adds:

| Factor | Candidate threshold |
|---|---:|
| D-dimer | > 5 mg/L |
| IL-6 | > 59 pg/mL |

### Advanced tier

Adds:

| Factor | Candidate threshold |
|---|---:|
| S100B | > 0.10 µg/L |
| NSE | > 33 µg/L |
| GFAP | > 0.68 µg/L |
| GFAP | > 15,000 pg/mL |
| Copeptin | > 451.8 pg/mL |
| CRP/Albumin ratio | > 0.38 |

The app reports how many candidate high-risk thresholds are triggered. It does **not** convert this count into a validated probability of mortality or unfavorable functional outcome.

## Running locally

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it and install dependencies:

```bash
pip install -r requirements.txt
```

Run the app:

```bash
streamlit run app.py
```

## Methodological concept

The prototype follows a tiered-accessibility concept: models or rule sets can be evaluated with increasingly specialized data availability.

A future validated version should include:

1. prespecified outcome definitions;
2. independent model development and external validation cohorts;
3. missing-data handling;
4. continuous-variable modelling rather than simple dichotomization where appropriate;
5. calibration assessment;
6. discrimination assessment;
7. internal validation and optimism correction;
8. decision-curve analysis;
9. transparent reporting following appropriate prediction-model reporting standards;
10. prospective clinical-impact evaluation before implementation.

## Current limitations

The present repository is intentionally simple and transparent.

It has several important limitations:

- candidate thresholds are encoded as fixed binary rules;
- the contribution of each factor is treated equally;
- interactions between predictors are not modelled;
- no probability model is fitted;
- no calibration model is available;
- no external validation is included;
- biomarker units and assay differences require careful harmonization before real-world implementation.

## Intended use

This repository is suitable for:

- research demonstration;
- methodological prototyping;
- portfolio presentation;
- interface testing;
- future integration with validated prognostic modelling work.

It is not suitable for direct clinical use.

## Author

**Muhana Fawwazy Ilyas, MD**  
ORCID: https://orcid.org/0000-0002-0176-9773  
GitHub: https://github.com/muhanailyas

## Citation

Citation metadata are provided in `CITATION.cff`.

## License

MIT License.
