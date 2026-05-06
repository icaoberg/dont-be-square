import json
import os
import random
import requests
import numpy as np
from tqdm import tqdm
from datetime import datetime
from typing import Dict
import logging
from fair.findable import __get_metadata
import streamlit as st


logger = logging.getLogger(__name__)


def interoperable(dataset_id: str) -> float:
    metadata = __get_metadata(dataset_id)
    score = [
        __has_genetic_sequences(metadata),
        __has_assay_category(metadata), 
        __has_assay_type(metadata),
        __has_contributors_path(metadata),
        __has_version(metadata),
        __has_direct_ancestors(metadata),
        
        __has_antibody_version(metadata)
    ]
    print(f'I: {score}')
    result = np.mean(score)
    return result,score

# ─────────────────────────────────────────────────────────────
# Helper Methods Section
# Add any additional helper methods below this block.
# These should be utility functions to support the main logic.
# ─────────────────────────────────────────────────────────────
def __has_genetic_sequences(metadata: dict) -> int:
    logger.info("__has_genetic_sequences() started")
    if "contains_human_genetic_sequences" not in metadata:
        return 1
    result = 1 if "contains_human_genetic_sequences" in metadata else 0
    logger.info(f"__has_genetic_sequences() completed with result {result}")
    return result

def __has_assay_category(metadata: dict) -> int:
    logger.info("__has_assay_category() started")
    valid_categories = {'imaging', 'sequence', None}
    result = 0
    try:
        value = metadata.get("assay_category") or metadata.get("metadata", {}).get("assay_category")
        if value in valid_categories:
            result = 1
    except Exception as e:
        logger.error(f"Error checking assay category: {e}")

    logger.info(f"__has_assay_category() completed with result {result}")
    return result


def __has_assay_type(metadata: dict) -> int:
    logger.info("__has_assay_type() started")
    valid_types = {
        'CODEX', 'Imaging Mass Cytometry', 'scRNAseq-10xGenomics',
        'bulkATACseq','snATACseq', 'sciATACseq', 'sciRNAseq', 
        'scRNAseq-10xGenomics-v2','scRNAseq-10xGenomics-v3', 'snRNAseq',
        'snRNAseq-10xGenomics-v3','SNARE-seq2', 'SNARE2-RNAseq', 'seqFISH', None
    }
    result = 0
    try:
        value = metadata.get("assay_type") or metadata.get("metadata", {}).get("assay_type")
        if value in valid_types:
            result = 1
    except Exception as e:
        logger.error(f"Error checking assay type: {e}")

    logger.info(f"__has_assay_type() completed with result {result}")
    return result

def __has_contributors_path(metadata: dict) -> int:
    logger.info("__has_hubmap_id() started")
    result = 0 
    try:
        if "contributors_path" in metadata:
            result = 1

        elif "contributors_path" in metadata['metadata']:
            result = 1

    except Exception as e:
        logger.error(f"Error checking contributor path key: {e}")
                
    logger.info(f"__has_contributors_path() completed with result {result}")
    return result

def __has_version(metadata: dict) -> int:
    logger.info("__has_version() started")
    result = 0  # default
    try:
        if "version" in metadata:
            result = 1

        elif "version" in metadata['metadata']:
            result = 1

    except Exception as e:
        logger.error(f"Error checking version key: {e}")

    logger.info(f"__has_version() completed with result {result}")
    return result

def __has_direct_ancestors(metadata: dict) -> int:
    logger.info("__has_direct_ancestors() started")
    hubmap_id = metadata.get('hubmap_id')
    try:
        ancestry_hubamp_id = metadata['direct_ancestors'][0].get('hubmap_id')
        result = 1 if hubmap_id == ancestry_hubamp_id else 0
        logger.info(f"__has_direct_ancestors() completed with result {result}")
        return result
    except Exception as e:
        logger.error(f"Error checking antibodies key: {e}")     
        return 1    

def __has_antibody_version(metadata: dict) -> int:
    logger.info("__has_antibody_version() started")
    result = 0 
    try :
        anti = metadata['antibodies'][0]
        result = 1 if "version" in anti else 0
    except Exception as e:
        result = 1 
        logger.error(f"Error checking antibodies key: {e}")     
        return result 
    
    logger.info(f"__has_antibody_version() completed with result {result}")
    return result
