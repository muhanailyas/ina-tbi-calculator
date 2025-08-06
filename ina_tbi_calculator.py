import streamlit as st
import math

# Page setup
st.set_page_config(page_title="Ina-TBI Mortality Risk Calculator", layout="centered")
st.title("🧠 Ina-TBI Mortality Risk Calculator")

st.markdown("**#AIinNeurosurgery #AIinNeurotrauma**")

st.markdown("""
This calculator helps estimate the risk of mortality in traumatic brain injury (TBI) patients based on clinical and biomarker parameters.  
**Disclaimer:** This tool is intended for research and educational purposes only. Not for direct clinical use. Since this only pilot/ prototype for further research**  
(Developed by Muhana Fawwazy Ilyas, MD.)
""")

st.markdown("""
### 🧪 Tiers of Prediction

**Basic Tier** includes readily available clinical and blood test parameters:
- Age
- Glasgow Coma Scale (GCS)
- CT Rotterdam Score
- Hemoglobin
- Glucose
- Neutrophil-to-Lymphocyte Ratio (NLR)
- Platelet-to-Lymphocyte Ratio (PLR)

**Intermediate Tier** includes Basic + inflammatory markers:
- D-dimer
- Interleukin-6 (IL-6)

**Advanced Tier** includes Intermediate + specialized biomarkers:
- S100B
- Neuron-Specific Enolase (NSE)
- Glial Fibrillary Acidic Protein (GFAP)
- Copeptin
- CRP/Albumin Ratio (CAR)

The calculator automatically uses whatever data is provided and scores accordingly.
""")

# Input form
with st.form("tbi_form"):
    age = st.number_input("Age (years, leave 0 if unknown)", min_value=0, step=1)
    gcs = st.number_input("Glasgow Coma Scale (GCS, leave 0 if unknown)", min_value=0, max_value=15, step=1)
    rotterdam = st.number_input("CT Rotterdam Score (leave 0 if unknown)", min_value=0, max_value=6, step=1)
    hb = st.number_input("Hemoglobin (g/dL, leave 0 if unknown)", min_value=0.0, format="%.2f")
    glucose = st.number_input("Glucose (mg/dL, leave 0 if unknown)", min_value=0.0, format="%.2f")
    nlr = st.number_input("Neutrophil-to-Lymphocyte Ratio (NLR, leave 0 if unknown)", min_value=0.0, format="%.2f")
    plr = st.number_input("Platelet-to-Lymphocyte Ratio (PLR, leave 0 if unknown)", min_value=0.0, format="%.2f")
    ddimer = st.number_input("D-dimer (mg/L, leave 0 if unknown)", min_value=0.0, format="%.2f")
    il6 = st.number_input("Interleukin-6 (pg/mL, leave 0 if unknown)", min_value=0.0, format="%.2f")
    s100b = st.number_input("S100B (µg/L, leave 0 if unknown)", min_value=0.0, format="%.2f")
    nse = st.number_input("NSE (µg/L, leave 0 if unknown)", min_value=0.0, format="%.2f")
    gfap = st.number_input("GFAP (pg/mL, leave 0 if unknown)", min_value=0.0, format="%.2f")
    copeptin = st.number_input("Copeptin (pg/mL, leave 0 if unknown)", min_value=0.0, format="%.2f")
    car = st.number_input("CRP/Albumin Ratio (leave 0 if unknown)", min_value=0.0, format="%.2f")
    submitted = st.form_submit_button("Calculate Risk")

if submitted:
    score = 0
    if age > 40:
        score += 0.55
    if gcs != 0 and gcs <= 8:
        score += -0.42
    if rotterdam > 3:
        score += 1.83
    if hb != 0 and hb < 9.0:
        score += 1.13
    if glucose > 200:
        score += 0.69
    if nlr >= 4:
        score += 0.41
    if plr >= 190:
        score += 0.42
    if ddimer > 5:
        score += 0.74
    if il6 > 59:
        score += 0.36
    if s100b > 0.10:
        score += 0.59
    if nse > 33:
        score += 0.65
    if gfap > 15000:
        score += 0.88
    if copeptin > 451.8:
        score += 1.44
    if car > 0.38:
        score += 0.63

    # Risk tier classification
    if score < 2:
        tier = "Low"
    elif 2 <= score < 6:
        tier = "Moderate"
    else:
        tier = "High"

    # Output
    st.markdown("---")
    st.subheader("🧾 Results")
    st.write(f"**Total Score:** {score:.2f}")
    st.write(f"**Risk Tier:** {tier}")

    if tier == "High":
        st.error("⚠️ High Mortality Risk")
    elif tier == "Moderate":
        st.warning("⚠️ Moderate Mortality Risk")
    else:
        st.success("✅ Low Mortality Risk")

    st.markdown("---")
    st.caption("This tool is part of the Ina-TBI Project, aimed at improving TBI care in Indonesia.")