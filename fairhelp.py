import json
import os
import random
import requests
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.colors import LinearSegmentedColormap
from tqdm import tqdm
from datetime import datetime
from typing import Dict
import logging

# Optional Streamlit integration
try:
    import streamlit as st
    STREAMLIT_AVAILABLE = True
    streamlit_logs = []
except ImportError:
    STREAMLIT_AVAILABLE = False
    streamlit_logs = []

# ────────────────────────────────
# Logging Setup
# ────────────────────────────────
timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
log_filename = f"dontbesquare-{timestamp}.log"

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

file_handler = logging.FileHandler(log_filename)
file_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))

if not logger.handlers:
    logger.addHandler(file_handler)

# Streamlit handler
class StreamlitHandler(logging.Handler):
    def emit(self, record):
        msg = self.format(record)
        streamlit_logs.append(msg)

if STREAMLIT_AVAILABLE:
    streamlit_handler = StreamlitHandler()
    streamlit_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
    logger.addHandler(streamlit_handler)


# ────────────────────────────────
# Core Functions
# ────────────────────────────────

def create_fair_plot(data, output_file=None, scale=100, dpi=100, curated=False):
    logger.info("create_fair_plot() started")
    if data.shape != (2, 2):
        logger.error("Input must be a 2x2 array.")
        raise ValueError("Input must be a 2x2 array.")
    if (data > 1).any():
        logger.error("All values must be less than or equal to 1.")
        raise ValueError("All values must be less than or equal to 1.")

    if output_file is None:
        date_str = datetime.today().strftime("%Y%m%d")
        output_file = f"output-{date_str}.png"

    labels = np.array([["F", "A"], ["I", "R"]])
    masked_data = np.where(data < 0, np.nan, data)
    colors_list = ["blue", "white", "red"]
    cmap = LinearSegmentedColormap.from_list("blue_white_red", colors_list, N=256)
    cmap.set_bad("white")

    base_width, base_height = 5, 4
    scale_factor = scale / 100
    fig = plt.figure(
        figsize=(base_width * scale_factor, base_height * scale_factor), dpi=dpi
    )
    spec = gridspec.GridSpec(ncols=2, nrows=1, width_ratios=[1, 0.05], wspace=0.2)
    ax = fig.add_subplot(spec[0])
    cax = fig.add_subplot(spec[1])
    im = ax.imshow(masked_data, cmap=cmap, vmin=0, vmax=1)

    for i in range(2):
        for j in range(2):
            ax.text(
                j,
                i,
                labels[i, j],
                ha="center",
                va="center",
                fontsize=36 * scale_factor,
                fontweight="bold",
                color="black",
            )

    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)

    cbar = fig.colorbar(im, cax=cax, orientation="vertical")
    cbar.set_label("Score")

    plt.tight_layout()
    plt.savefig(output_file, dpi=dpi, bbox_inches="tight")
    plt.close(fig)
    logger.info(f"create_fair_plot() completed and saved to {output_file}")






















# ────────────────────────────────
# Optional Log Display for Streamlit
# ────────────────────────────────
def show_logs_in_streamlit():
    if STREAMLIT_AVAILABLE and streamlit_logs:
        st.subheader("🪵 Execution Log")
        for log in streamlit_logs:
            st.text(log)

def show_status(label: str, condition: bool, detail: str = ""):
    """
    Display a labeled status in Streamlit with optional detail.
    
    Args:
        label (str): Description of the check.
        condition (bool): Whether it passed.
        detail (str): Optional detail to include in failure case.
    """
    if condition:
        st.success(f"✅ {label} passed")
    else:
        st.error(f"❌ {label} failed - Status: {detail}")
