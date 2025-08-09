# app.py — Ina-TBI Mortality Risk Calculator (ln(OR)-based)

import streamlit as st
import requests
from io import BytesIO

st.set_page_config(page_title="Ina-TBI Mortality Risk Calculator", layout="centered")

# --- Header with Google Drive image ---
FILE_ID = "1l2yk0URnXsDlnl5EYncF7og9mXuWQ7OL"
LOGO_URL = f"https://drive.google.com/uc?export=download&id={FILE_ID}"

col1, col2 = st.columns([1, 3], vertical_alignment="center")
with col1:
    try:
        resp = requests.get(LOGO_URL, timeout=10)
        resp.raise_for_status()
        st.image(BytesIO(resp.content), use_container_width=True)
    except Exception:
        st.write("")  # silent fallback

with col2:
    st.title("Ina-TBI Mortality Risk Calculator")
    st.markdown("**#AIinNeurosurgery #AIinNeurotrauma**")

st.markdown(
    "This calculator estimates mortality risk in traumatic brain injury (TBI) using "
    "clinical and biomarker cutoffs.\n\n"
    "**Disclaimer:** Research/education only—prototype, not for clinical use.\n\n"
    "(Developed by Muhana Fawwazy Ilyas, MD.)"
)

# --- Helper: compute risk score and triggered criteria ---
def compute_ln_or_score(inputs):
    """
    inputs: dict of values
    returns: (score: float, hits: list[str])
    """
    score = 0.0
    hits = []

    # Each condition adds its ln(OR) weight (from your table)
    if inputs["age"] > 39:
        score += 0.329
        hits.append("Age > 39y (+0.329)")
    if inputs["gcs"] != 0 and inputs["gcs"] <= 8:
        score += 0.762
        hits.append("GCS ≤ 8 (+0.762)")
    if inputs["rotterdam"] > 3:
        score += 0.724
        hits.append("Rotterdam > 3 (+0.724)")
    if inputs["hb"] != 0 and inputs["hb"] < 7.5:
        score += 0.737
        hits.append("Hb < 7.5 g/dL (+0.737)")
    if inputs["glucose"] > 200:
        score += 0.693
        hits.append("Glucose > 200 mg/dL (+0.693)")
    if inputs["nlr"] > 7.44:
        score += 0.610
        hits.append("NLR > 7.44 (+0.610)")
    if inputs["plr"] < 68.57 and inputs["plr"] != 0:
        score += 0.231
        hits.append("PLR < 68.57 (+0.231)")
    if inputs["ddimer"] > 5:
        score += 0.693
        hits.append("D-dimer > 5 mg/L (+0.693)")
    if inputs["il6"] > 59:
        score += 0.140
        hits.append("IL-6 > 59 pg/mL (+0.140)")
    # Units per your table: GFAP cutoff 0.68 ng/mL
    if inputs["gfap"] > 0.68:
        score += 0.728
        hits.append("GFAP > 0.68 ng/mL (+0.728)")
    if inputs["copeptin"] > 300.8:
        score += 0.020
        hits.append("Copeptin > 300.8 pg/mL (+0.020)")

    return score, hits

def infer_data_tier(values):
    # Basic = only basic vars; Intermediate = + (D-dimer or IL-6); Advanced = + (GFAP or Copeptin)
    if values["gfap"] > 0 or values["copeptin"] > 0:
        return "Advanced"
    if values["ddimer"] > 0 or values["il6"] > 0:
        return "Intermediate"
    return "Basic"

# --- Inputs ---
with st.form("tbi_form"):
    age = st.number_input("Age (years)", min_value=0, step=1)
    gcs = st.number_input("Glasgow Coma Scale (0–15)", min_value=0, max_value=15, step=1)
    rotterdam = st.number_input("CT Rotterdam Score (0–6)", min_value=0, max_value=6, step=1)
    hb = st.number_input("Hemoglobin (g/dL)", min_value=0.0, format="%.2f")
    glucose = st.number_input("Glucose (mg/dL)", min_value=0.0, format="%.2f")
    nlr = st.number_input("Neutrophil-to-Lymphocyte Ratio (NLR)", min_value=0.0, format="%.2f")
    plr = st.number_input("Platelet-to-Lymphocyte Ratio (PLR)", min_value=0.0, format="%.2f")
    ddimer = st.number_input("D-dimer (mg/L)", min_value=0.0, format="%.2f")
    il6 = st.number_input("Interleukin-6 (pg/mL)", min_value=0.0, format="%.2f")
    # GFAP input in ng/mL (per your cutoff)
    gfap = st.number_input("GFAP (ng/mL)", min_value=0.0, format="%.3f")
    copeptin = st.number_input("Copeptin (pg/mL)", min_value=0.0, format="%.2f")
    submitted = st.form_submit_button("Calculate Risk")

# --- Compute & display ---
if submitted:
    values = {
        "age": age, "gcs": gcs, "rotterdam": rotterdam, "hb": hb, "glucose": glucose,
        "nlr": nlr, "plr": plr, "ddimer": ddimer, "il6": il6, "gfap": gfap, "copeptin": copeptin
    }
    score, hits = compute_ln_or_score(values)

    # Risk tiers by total ln(OR)
    if score <= 1.36:
        tier = "Low"
    elif score <= 2.72:
        tier = "Moderate"
    else:
        tier = "High"

    used_tier = infer_data_tier(values)

    st.markdown("---")
    st.subheader("🧾 Results")
    st.write(f"**Total ln(OR):** {score:.3f}")
    st.write(f"**Risk Tier:** {tier}")
    st.caption("Risk Stratification — Low: 0–1.36 | Moderate: 1.37–2.72 | High: 2.73–4.086")

    if hits:
        with st.expander("Show contributing factors"):
            for h in hits:
                st.write(f"- {h}")
    st.info(f"Data tier used: **{used_tier}**")

    if tier == "High":
        st.error("⚠️ High Mortality Risk")
    elif tier == "Moderate":
        st.warning("⚠️ Moderate Mortality Risk")
    else:
        st.success("✅ Low Mortality Risk")

    st.markdown("---")
    st.caption("Part of the Ina-TBI Project to improve TBI care in Indonesia.")