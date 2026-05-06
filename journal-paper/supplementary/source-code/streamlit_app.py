import streamlit as st
import fairhelp
import numpy as np
from datetime import datetime

from fair.accessible import accessible
from fair.reproducible import reproducible
from fair.interoperable import interoperable
from fair.findable import findable

# ────────────────────────────────
# Streamlit App Title
# ────────────────────────────────
st.title("🔬 FAIR Score Visualizer for HuBMAP Datasets")


# ────────────────────────────────
# Input for HuBMAP Dataset ID
# ────────────────────────────────
hubmap_id = st.text_input("Enter HuBMAP Dataset ID:", value="HBM666.NDQZ.365")

# ────────────────────────────────
# Trigger Button
# ────────────────────────────────
if st.button("Calculate FAIR Score") and hubmap_id:
    try:
        # ────────────────────────────────
        # Compute FAIR Scores
        # ────────────────────────────────
        status_text = st.empty()
        status_text.text(f"Calculating FAIR scores...")
        #st.info("Calculating FAIR scores...")
        findable = findable(hubmap_id)[0]
        accessible = accessible(hubmap_id)[0]
        interoperable = interoperable(hubmap_id)[0]
        reproducible = reproducible(hubmap_id)[0]

        fair = [findable, accessible, interoperable, reproducible]
        
        status_text.success("Scores calculated successfully!")
        #st.success("Scores calculated successfully!")

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
        output_path = fairhelp.create_fair_plot(
            np.array(fair).reshape(2, 2),
            output_file=output_file,
            scale=100,
            dpi=100,
            curated=False,
        )

        st.image(output_path, caption=f"FAIR Heatmap for {hubmap_id}")
    except Exception as e:
        st.error(f"Failed to compute FAIR score: {e}")
