import streamlit as st

from src.calculator import (
    BASIC_FACTORS,
    INTERMEDIATE_FACTORS,
    ADVANCED_FACTORS,
    evaluate_tier,
    overall_summary,
)

st.set_page_config(
    page_title="INA-TBI Calculator",
    page_icon="🧠",
    layout="wide",
)

st.title("INA-TBI Calculator")
st.caption("Prototype rule-based traumatic brain injury prognostic calculator")

st.warning(
    "Prototype only. This tool is not clinically validated and must not be used "
    "for diagnosis, treatment decisions, triage, prognostication, or patient counselling."
)

with st.expander("About this prototype"):
    st.markdown(
        """
        The INA-TBI Calculator is a transparent, rule-based research prototype that
        organizes candidate prognostic factors into three tiers:

        - **Basic:** routinely available clinical and laboratory variables
        - **Intermediate:** adds selected inflammatory and coagulation biomarkers
        - **Advanced:** adds selected neurological injury biomarkers

        The current implementation is intended for research demonstration and portfolio use.
        Thresholds are based on the project's prior evidence synthesis and should be
        independently verified and prospectively validated before any clinical use.
        """
    )

tab1, tab2, tab3 = st.tabs(["Basic", "Intermediate", "Advanced"])

values = {}

with tab1:
    st.subheader("Basic tier")
    c1, c2 = st.columns(2)
    with c1:
        values["age"] = st.number_input("Age (years)", min_value=0, max_value=120, value=40)
        values["gcs"] = st.number_input("Glasgow Coma Scale", min_value=3, max_value=15, value=13)
        values["rotterdam"] = st.number_input("Rotterdam CT score", min_value=1, max_value=6, value=2)
        values["hemoglobin"] = st.number_input("Hemoglobin (g/dL)", min_value=0.0, max_value=30.0, value=12.0, step=0.1)
    with c2:
        values["glucose"] = st.number_input("Glucose (mg/dL)", min_value=0.0, max_value=1000.0, value=110.0, step=1.0)
        values["nlr"] = st.number_input("Neutrophil-to-lymphocyte ratio", min_value=0.0, max_value=100.0, value=4.0, step=0.1)
        values["plr"] = st.number_input("Platelet-to-lymphocyte ratio", min_value=0.0, max_value=1000.0, value=150.0, step=1.0)

with tab2:
    st.subheader("Intermediate tier")
    st.caption("Includes all Basic tier variables plus:")
    c1, c2 = st.columns(2)
    with c1:
        values["d_dimer"] = st.number_input("D-dimer (mg/L)", min_value=0.0, max_value=100.0, value=1.0, step=0.1)
    with c2:
        values["il6"] = st.number_input("IL-6 (pg/mL)", min_value=0.0, max_value=5000.0, value=20.0, step=1.0)

with tab3:
    st.subheader("Advanced tier")
    st.caption("Includes all Basic and Intermediate tier variables plus:")
    c1, c2 = st.columns(2)
    with c1:
        values["s100b"] = st.number_input("S100B (µg/L)", min_value=0.0, max_value=100.0, value=0.05, step=0.01)
        values["nse"] = st.number_input("NSE (µg/L)", min_value=0.0, max_value=500.0, value=20.0, step=1.0)
        values["gfap_ug"] = st.number_input("GFAP (µg/L)", min_value=0.0, max_value=100.0, value=0.30, step=0.01)
    with c2:
        values["gfap_pg"] = st.number_input("GFAP (pg/mL)", min_value=0.0, max_value=100000.0, value=5000.0, step=100.0)
        values["copeptin"] = st.number_input("Copeptin (pg/mL)", min_value=0.0, max_value=10000.0, value=200.0, step=10.0)
        values["crp_albumin"] = st.number_input("CRP/Albumin ratio", min_value=0.0, max_value=50.0, value=0.20, step=0.01)

st.divider()

tier_choice = st.radio(
    "Evaluation tier",
    ["Basic", "Intermediate", "Advanced"],
    horizontal=True,
)

if st.button("Evaluate prototype risk profile", type="primary", use_container_width=True):
    tier_map = {
        "Basic": BASIC_FACTORS,
        "Intermediate": BASIC_FACTORS + INTERMEDIATE_FACTORS,
        "Advanced": BASIC_FACTORS + INTERMEDIATE_FACTORS + ADVANCED_FACTORS,
    }

    result = evaluate_tier(values, tier_map[tier_choice])
    summary = overall_summary(result)

    st.subheader(f"{tier_choice} tier result")
    m1, m2, m3 = st.columns(3)
    m1.metric("Triggered factors", summary["triggered"])
    m2.metric("Total factors assessed", summary["total"])
    m3.metric("Triggered proportion", f'{summary["proportion"]:.0%}')

    if summary["triggered"] == 0:
        st.success("No candidate high-risk thresholds were triggered in the selected tier.")
    elif summary["proportion"] < 0.34:
        st.info("A minority of candidate high-risk thresholds were triggered.")
    elif summary["proportion"] < 0.67:
        st.warning("Several candidate high-risk thresholds were triggered.")
    else:
        st.error("Many candidate high-risk thresholds were triggered.")

    st.markdown("### Factor-level assessment")
    st.dataframe(result, use_container_width=True, hide_index=True)

    st.caption(
        "This output is a descriptive threshold profile, not a validated probability of mortality "
        "or unfavorable outcome."
    )
