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

# Generate dynamic log filename
timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
log_filename = f"dontbesquare-{timestamp}.log"

# Create logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Add file handler (required to write to disk!)
file_handler = logging.FileHandler(log_filename)
file_handler.setFormatter(
    logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
)

if not logger.handlers:
    logger.addHandler(file_handler)


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


def __get_metadata(dataset_id: str, api_url: str = "https://entity.api.hubmapconsortium.org/entities") -> Dict:
    logger.info(f"__get_metadata() started for {dataset_id}")
    try:
        response = requests.get(f"{api_url}/{dataset_id}")
        response.raise_for_status()
        metadata = response.json()
        os.makedirs("JSON", exist_ok=True)
        filepath = os.path.join("JSON", f"{dataset_id}.json")
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(metadata, f, indent=2)
        logger.info(f"__get_metadata() completed successfully for {dataset_id}")
        return metadata
    except requests.RequestException as e:
        logger.error(f"Error fetching metadata for {dataset_id}: {e}")
        return {"error": str(e)}


def findable(dataset_id: str) -> float:
    logger.info(f"findable() started for {dataset_id}")
    metadata = __get_metadata(dataset_id)
    score = [
        __no_error(metadata),
        __has_antibodies(metadata),
        __has_uuid(metadata),
        __is_dataset_entity(metadata),
        __has_title(metadata)
    ]
    result = np.mean(score)
    logger.info(f"findable() completed for {dataset_id} with score {result}")
    return result


def accessible(dataset_id: str) -> float:
    logger.info(f"accessible() started for {dataset_id}")
    metadata = __get_metadata(dataset_id)
    score = [
        1 if "doi_url" in metadata and __is_link_accessible(metadata["doi_url"]) else 0,
             __is_published(metadata),
             __has_group_name(metadata),
            __has_group_uuid(metadata),
            __has_hubmap_id(metadata)
             ]
    result = np.mean(score)
    logger.info(f"accessible() completed for {dataset_id} with score {result}")
    return result


def interoperable(dataset_id: str) -> float:
    logger.info(f"interoperable() started for {dataset_id}")
    metadata = __get_metadata(dataset_id)
    score = [
        __has_genetic_sequences(metadata),
        __has_assay_category(metadata),
        __has_assay_type(metadata),
        __has_contributors_path(metadata),
        __has_version(metadata)
    ] 
    result = np.mean(score)
    logger.info(f"interoperable() completed for {dataset_id} with score {result}")
    return result


def reproducible(dataset_id: str) -> float:
    logger.info(f"reproducible() started for {dataset_id}")
    metadata = __get_metadata(dataset_id)
    score = [
        average_metadata_success(dataset_id)
        ]
    result = np.mean(score)
    logger.info(f"reproducible() completed for {dataset_id} with score {result}")
    return result


def __is_link_accessible(url: str, timeout: int = 5) -> bool:
    logger.info(f"__is_link_accessible() checking URL: {url}")
    try:
        response = requests.head(url, allow_redirects=True, timeout=timeout)
        success = response.status_code == 200
        logger.info(f"URL {url} is {'accessible' if success else 'not accessible'}")
        return success
    except requests.RequestException:
        logger.warning(f"URL check failed: {url}")
        return False


def __has_antibodies(metadata: dict) -> bool:
    logger.info("__has_antibodies() started")
    score = []
    antibodies = metadata.get("antibodies", [])
    score.append(bool(antibodies))

    for antibody in tqdm(antibodies):
        accession = antibody.get("uniprot_accession_number")
        if accession:
            url = f"https://rest.uniprot.org/uniprotkb/{accession}"
            if not __is_link_accessible(url):
                logger.error(f"Failed to access UniProt URL for accession: {accession}")
                score.append(False)
            else:
                score.append(True)

    result = all(score)
    logger.info(f"__has_antibodies() completed with result {result}")
    return result


def __is_published(metadata: dict) -> int:
    logger.info("__is_published() started")
    result = 1 if metadata.get("status") == "Published" else 0
    logger.info(f"__is_published() completed with result {result}")
    return result


def __has_uuid(metadata: dict) -> int:
    logger.info("__has_uuid() started")
    result = 1 if "uuid" in metadata else 0
    logger.info(f"__has_uuid() completed with result {result}")
    return result


def __is_dataset_entity(metadata: dict) -> int:
    logger.info("__is_dataset_entity() started")
    result = 1 if metadata.get("entity_type") == "Dataset" else 0
    logger.info(f"__is_dataset_entity() completed with result {result}")
    return result


def __no_error(metadata: dict) -> int:
    logger.info("__no_error() started")
    result = 0 if "error" in metadata else 1
    logger.info(f"__no_error() completed with result {result}")
    return result


def average_metadata_success(hubmap_id: str) -> float:
    logger.info(f"average_metadata_success() started for {hubmap_id}")
    num_trials = random.randint(3, 10)
    success_count = 0

    for _ in tqdm(range(num_trials)):
        metadata = __get_metadata(hubmap_id)
        if metadata and isinstance(metadata, dict) and "error" not in metadata and len(metadata) > 0:
            success_count += 1

    result = success_count / num_trials
    logger.info(f"average_metadata_success() completed with result {result}")
    return result

def __has_group_name(metadata: dict) -> int:
    logger.info("__has_group_name() started")
    result = 1 if "group_name" in metadata else 0
    logger.info(f"__has_group_name() completed with result {result}")
    return result

def __has_group_uuid(metadata: dict) -> int:
    logger.info("__has_group_uuid() started")
    result = 1 if "group_uuid" in metadata else 0
    logger.info(f"__has_group_uuid() completed with result {result}")
    return result

def __has_hubmap_id(metadata: dict) -> int:
    logger.info("__has_hubmap_id() started")
    result = 1 if "hubmap_id" in metadata else 0
    logger.info(f"__has_hubmap_id() completed with result {result}")
    return result

def __has_title(metadata: dict) -> int:
    logger.info("__has_title() started")
    result = 1 if "title" in metadata else 0
    logger.info(f"__has_title() completed with result {result}")
    return result

def __has_genetic_sequences(metadata: dict) -> int:
    logger.info("__has_genetic_sequences() started")
    result = 1 if "contains_human_genetic_sequences" in metadata else 0
    logger.info(f"__has_genetic_sequences() completed with result {result}")
    return result

def __has_assay_category(metadata: dict) -> int:
    logger.info("__has_assay_category() started")
    result = 1 if "assay_category" in metadata else 0
    logger.info(f"__has_assay_category() completed with result {result}")
    return result

def __has_assay_type(metadata: dict) -> int:
    logger.info("__has_assay_type() started")
    result = 1 if "assay_type" in metadata else 0
    logger.info(f"__has_assay_type() completed with result {result}")
    return result

def __has_contributors_path(metadata: dict) -> int:
    logger.info("__has_hubmap_id() started")
    result = 1 if "contributors_path" in metadata else 0
    logger.info(f"__has_contributors_path() completed with result {result}")
    return result
def __has_version(metadata: dict) -> int:
    logger.info("__has_version() started")
    result = 1 if "version" in metadata else 0
    logger.info(f"__has_version() completed with result {result}")
    return result
