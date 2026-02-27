from types import NoneType
import streamlit as st
import fairhelp
import numpy as np
from datetime import datetime

from fair.accessible import accessible
from fair.reproducible import reproducible
from fair.interoperable import interoperable
from fair.findable import findable
import pandas as pd
import os
from fair import utils
import time


# ──────────────────────────────────────────
# if exist read df 
# ──────────────────────────────────────────
status_text = st.empty()
file_path = "./fair/fair_results.json"

# Check if file exists
if not os.path.exists(file_path):
    status_text.error("Error: File not found.")
    st.stop()

status_text.text("File found, reading data from local storage...")

# Read data
df = utils.read_json_fair(file_path)
status_text.text("Loading data...")

# Validate data
if df is None or len(df) == 0:
    status_text.error("Error: Loading data failed or file is empty.")
    st.stop()

# Success
status_text.success("Data loaded successfully!")
st.write(f"Total datasets loaded: {len(df)}")
# ────────────────────────────────
# Streamlit App Title
# ────────────────────────────────
st.title("🔬 FAIR Score Visualizer for HuBMAP Datasets")

# ────────────────────────────────────────────
# List values for group names 
# ────────────────────────────────────────────
lab_list = utils.group_list(df)

# ────────────────────────────────────────────
# List values for assay types
# ────────────────────────────────────────────
assay_list = utils.type_list(df)
# ────────────────────────────────────────────

# ────────────────────────────────
# Input for HuBMAP Dataset ID
# ────────────────────────────────
# Display the selected option using success message
# ────────────────────────────────
search_form = st.radio("Select by Search:", ['Lab', 'Assay type', 'Lab and Assay type', 'Hubmap id','All datasets'])
if search_form == 'Lab':
    lab_selected = st.selectbox("Select Laboratories:", lab_list )

elif search_form == 'Assay type':
    assay_selected = st.selectbox("Select assay:", assay_list)

elif search_form == 'Lab and Assay type':
    lab_selected = st.selectbox("Select Laboratories:", lab_list )
    assay_selected = st.selectbox("Select assay:", assay_list)

elif search_form == 'Hubmap id':
    hubmap_id = st.text_input("Enter HuBMAP Dataset ID:", value="HBM666.NDQZ.365")

# ────────────────────────────────
# Compute FAIR Scores
# ────────────────────────────────

if st.button(f"Calculating FAIR scores") and search_form:
    try:
        status_text = st.empty()
        status_text.text(f"Calculating FAIR scores...")
        # calculate each posible  by search type results

        if search_form == 'Lab':
            result = (utils.search_by_lab(df,lab_selected))
            if result == [] or result == [np.nan,np.nan,np.nan]:
                st.error(f"No results found for lab: {lab_selected}")
                st.stop()
            
            result_mean = utils.mean_fair_results(result)
            label = lab_selected

        elif search_form == 'Assay type':
            result = (utils.search_by_assay(df,assay_selected))
            if result == [] or result == [np.nan,np.nan,np.nan]:
                st.error(f"No results found for assay: {assay_selected}")
                st.stop()
            result_mean = utils.mean_fair_results(result)
            label = assay_selected

        elif search_form == 'Lab and Assay type':
            result = (utils.search_by_lab_assay(df,lab_selected,assay_selected))
            if result == [] or result == [np.nan,np.nan,np.nan]:
                st.error(f"No results found for lab: {lab_selected} and assay: {assay_selected}")
                st.stop()
            result_mean = utils.mean_fair_results(result)
            label = ((lab_selected,assay_selected))
        
        elif search_form == 'Hubmap id':
            result = utils.search_by_id(df,hubmap_id)
            if result == [] or result == [np.nan,np.nan,np.nan]:
                st.error(f"No results found for HuBMAP ID: {hubmap_id}")
                st.stop()
            result_mean = utils.mean_fair_results(result)
            label = hubmap_id

        else: 
            result = utils.search_all_id(df)
            if result == [] or result == [np.nan,np.nan,np.nan]:
                st.error(f"No results found")
                st.stop()
            result_mean = utils.mean_fair_results(result)
            label = 'All Datasets'

        st.write(label)
        utils.create_heatmap_for(result_mean, label)

        status_text.success("Scores calculated successfully!")
    except Exception as e:
            st.error(f"Failed to compute FAIR score: {e}")
            