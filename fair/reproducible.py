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
import streamlit as st


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
    valid_dataset_types = {
        'CODEX', 'IMC', 'scRNA-Seq-10x', 'ATACseq-bulk', 'snATACseq',
        'sciATACseq', 'sciRNAseq', 'scRNAseq-10xGenomics-v2', 'scRNAseq-10xGenomics-v3',
        'snRNAseq-10xGenomics-v3', 'snRNAseq', 'SNARE-ATACseq2', 'SNARE-RNAseq2',
        'seqFish', 'image_pyramid', 'CODEX [Cytokit + SPRM]', 'RNAseq [Salmon]', 'RNAseq',
        None, '2D Imaging Mass Cytometry [Image Pyramid]', 'Light Sheet',
        'Light Sheet [Image Pyramid]', '2D Imaging Mass Cytometry','3D Imaging Mass Cytometry',
        '3D Imaging Mass Cytometry [Image Pyramid]', 'LC-MS', 'ATACseq',
        'ATACseq [BWA + MACS2]', 'ATACseq [SnapATAC]', 'WGS',
        'Histology [Image Pyramid]', 'Histology', 'Publication', 'seqFISH','seqFISH [Image Pyramid]',
        'seqFISH [Lab Processed]', 'ATACseq [ArchR]', 'Slide-seq', 'Slide-seq [Salmon]', 
        'SNARE-seq2','SNARE-seq2 [Salmon + ArchR + Muon]', 'MUSIC', 'DESI','DESI [Image Pyramid]',
        '10X Multiome''10X Multiome [Salmon + ArchR + Muon]', 'Visium (no probes)','Visium (no probes) [Salmon + Scanpy]'

    }
    result = 0
    try:
        value = metadata.get("dataset_type") or metadata.get("metadata", {}).get("dataset_type")
        if value in valid_dataset_types:
            result = 1
    except Exception as e:
        logger.error(f"Error checking dataset_type: {e}")
    logger.info(f"__has_dataset_type() completed with result {result}")
    return result


def __has_analyte_class(metadata: dict) -> int:
    logger.info("__has_analyte_class() started")
    valid_analyte_classes = {'Protein', 'RNA', 'DNA', None}
    result = 0
    try:
        value = metadata.get("analyte_class") or metadata.get("metadata", {}).get("analyte_class")
        if value in valid_analyte_classes:
            result = 1
    except Exception as e:
        logger.error(f"Error checking analyte_class: {e}")
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

