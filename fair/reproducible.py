import json
import os
import random
import requests
import numpy as np
from tqdm import tqdm
from datetime import datetime
from typing import Dict
from fair.findable import __get_metadata
import logging

logger = logging.getLogger(__name__)

def reproducible(dataset_id: str) -> float:
    metadata = __get_metadata(dataset_id)
    score = [
        __average_metadata_success(dataset_id),

        __has_resolution_x_unit(metadata),#0
        __has_resolution_x_value(metadata),

        __has_resolution_y_unit(metadata),#0
        __has_resolution_y_value(metadata),

        __has_resolution_z_unit(metadata),#0
        __has_resolution_z_value(metadata),

        __has_dataset_type(metadata),
        __has_analyte_class(metadata),#0

        __has_preparation_instrument_kit(metadata),
        __has_acquisition_instrument_model(metadata)#0
    ]

    print(f'R: {score}')
    result = np.mean(score)
    return result,score

# ─────────────────────────────────────────────────────────────
# Helper Methods Section
# Add any additional helper methods below this block.
# These should be utility functions to support the main logic.
# ─────────────────────────────────────────────────────────────
    
def __average_metadata_success(hubmap_id: str) -> float:
    num_trials = random.randint(3, 10)
    success_count = 0

    for _ in tqdm(range(num_trials)):
        metadata = __get_metadata(hubmap_id)
        if metadata and isinstance(metadata, dict) and "error" not in metadata and len(metadata) > 0:
            success_count += 1

    result = success_count / num_trials
    return int(result)

# required
def __has_resolution_x_unit(metadata: dict) -> int:
    logger.info("__has_resolution_x_unit() started")
    try:
        meta = metadata["metadata"]
        value = meta.get("resolution_x_unit")
        if value == None:
            return 1
        result = 1 if isinstance(value, str) and not isinstance(value, bool) else 0
        print(f'x unite: {value},{result}')
    except (KeyError, TypeError):
        result = 1 
    logger.info(f"__has_resolution_x_unit() completed with result {result}")
    return result


def __has_resolution_x_value(metadata: dict) -> int:
    logger.info("__has_resolution_x_value() started")
    try:
        meta = metadata["metadata"]
        value = meta.get("resolution_x_value")
        # try casting to float, but exclude bools
        if isinstance(value, bool):
            result = 0
        else:
            float(value)
            result = 1
    except (KeyError, TypeError, ValueError):
        result = 1 if "resolution_x_value" not in metadata.get("metadata", {}) else 0
    logger.info(f"__has_resolution_x_value() completed with result {result}")
    return result


def __has_resolution_y_unit(metadata: dict) -> int:
    logger.info("__has_resolution_y_unit() started")
    try:
        meta = metadata["metadata"]
        value = meta.get("resolution_y_unit")
        if value == None:
            return 1
        result = 1 if isinstance(value, str) and not isinstance(value, bool) else 0
    except (KeyError, TypeError):
        result = 1
    logger.info(f"__has_resolution_y_unit() completed with result {result}")
    return result


def __has_resolution_y_value(metadata: dict) -> int:
    logger.info("__has_resolution_y_value() started")
    try:
        meta = metadata["metadata"]
        value = meta.get("resolution_y_value")
        if isinstance(value, bool):
            result = 0
        else:
            float(value)
            result = 1
    except (KeyError, TypeError, ValueError):
        result = 1 if "resolution_y_value" not in metadata.get("metadata", {}) else 0
    logger.info(f"__has_resolution_y_value() completed with result {result}")
    return result

def __has_resolution_z_unit(metadata: dict) -> int:
    logger.info("__has_resolution_z_unit() started")
    try:
        meta = metadata["metadata"]
        value = meta.get("resolution_z_unit")
        if value == None:
            return 1
        result = 1 if isinstance(value, str) and not isinstance(value, bool) else 0
    except (KeyError, TypeError):
        result = 1
    logger.info(f"__has_resolution_z_unit() completed with result {result}")
    return result


def __has_resolution_z_value(metadata: dict) -> int:
    logger.info("__has_resolution_z_value() started")
    try:
        meta = metadata["metadata"]
        value = meta.get("resolution_z_value")
        if isinstance(value, bool):
            result = 0
        else:
            float(value)
            result = 1
    except (KeyError, TypeError, ValueError):
        result = 1 if "resolution_z_value" not in metadata.get("metadata", {}) else 0
    logger.info(f"__has_resolution_z_value() completed with result {result}")
    return result


def __has_dataset_type(metadata: dict) -> int:
    logger.info("__has_dataset_type() started")
    try: 
        result = 1 if "dataset_type" in metadata else 0
    except:
        return 1 
    logger.info("__has_dataset_type() completed  with result {result}")
    return result 


def __has_analyte_class(metadata: dict) -> int:
    logger.info("__has_analyte_class() started")
    try:
        meta = metadata['metadata']
        value = meta.get("analyte_class")
        result = 1 if isinstance(value, str) else 0
    except:
        return 1 
    logger.info(f"__has_analyte_class() completed with result {result}")
    return result
#

def __has_preparation_instrument_kit(metadata: dict) -> int:
    logger.info("__has_preparation_instrument_kit() started")
    try: 
        meta = metadata['metadata']
        value = meta.get("preparation_instrument_kit")
        result = 1 if isinstance(value, str) else 0
    except: 
        return 1
    logger.info(f"__has_preparation_instrument_kit() completed with result {result}")
    return result

def __has_acquisition_instrument_model(metadata: dict) -> int:
    logger.info("__has_acquisition_instrument_model() started")
    try:
        meta = metadata['metadata']

        value = meta.get("acquisition_instrument_model")
        result = 1 if isinstance(value, str) else 0
    except:
        return 1
    logger.info(f"__has_acquisition_instrument_model() completed with result {result}")
    return result

