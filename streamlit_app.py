import streamlit as st
from . import fairhelp
import numpy as np
from datetime import datetime

# ────────────────────────────────
# Streamlit App Title
# ────────────────────────────────
st.title("🔬 FAIR Score Visualizer for HuBMAP Datasets")

# ────────────────────────────────
# Input for HuBMAP Dataset ID
# ────────────────────────────────
hubmap_id = st.text_input("Enter HuBMAP Dataset ID:", value="HBM666.NDQZ.365")

if hubmap_id:
    try:
        # ────────────────────────────────
        # Compute FAIR Scores
        # ────────────────────────────────
        st.info("Calculating FAIR scores...")
        findable = fairhelp.findable(hubmap_id)
        accessible = fairhelp.accessible(hubmap_id)
        interoperable = fairhelp.interoperable(hubmap_id)
        reproducible = fairhelp.reproducible(hubmap_id)

        fair = [findable, accessible, interoperable, reproducible]
        st.success("Scores calculated successfully!")

        # ────────────────────────────────
        # Display Individual Scores
        # ────────────────────────────────
        st.subheader("📊 FAIR Scores")
        st.markdown(f"- **Findable:** {findable:.2f}")
        st.markdown(f"- **Accessible:** {accessible:.2f}")
        st.markdown(f"- **Interoperable:** {interoperable:.2f}")
        st.markdown(f"- **Reproducible:** {reproducible:.2f}")

        # ────────────────────────────────
        # Create and Display FAIR Plot
        # ────────────────────────────────
        st.subheader("🖼️ FAIR Heatmap")

        output_file = f"FAIR_{hubmap_id}_{datetime.now().strftime('%Y%m%d-%H%M%S')}.png"
        fairhelp.create_fair_plot(
            np.array(fair).reshape(2, 2),
            output_file=output_file,
            scale=100,
            dpi=100,
            curated=False,
        )

        st.image(output_file, caption=f"FAIR Heatmap for {hubmap_id}")

    except Exception as e:
        st.error(f"Failed to compute FAIR score: {e}")
