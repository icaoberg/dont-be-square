# Complete System Overview

## Description
This diagram shows how the entire FAIR scoring system works, from precomputation through to user interaction. It merges both the data loading pipeline and the Streamlit application display system.

## Complete System Flow Diagram

```mermaid
flowchart TD
    Start([System Overview]) --> Phase1[Phase 1: Precomputation]
    Phase1 --> Phase2[Phase 2: Data Storage]
    Phase2 --> Phase3[Phase 3: Application Display]
    
    subgraph Phase1["Phase 1: Precomputation Pipeline"]
        direction TB
        P1Start([create_fair_json.py execution]) --> P1SDK[Initialize HuBMAP SDKs]
        P1SDK --> P1Search[SearchSdk: Search by university groups]
        P1Search --> P1Entity[EntitySdk: Get dataset metadata]
        P1Entity --> P1Convert[Convert Dataset objects to DataFrames]
        P1Convert --> P1Process[process_fair_multi_datastes]
        
        P1Process --> P1FAIR[Calculate FAIR scores for each dataset]
        P1FAIR --> P1Findable[findable: 8 checks]
        P1FAIR --> P1Accessible[accessible: 7 checks]
        P1FAIR --> P1Interoperable[interoperable: 7 checks]
        P1FAIR --> P1Reproducible[reproducible: 11 checks]
        
        P1Findable --> P1Collect[Collect F/A/I/R scores]
        P1Accessible --> P1Collect
        P1Interoperable --> P1Collect
        P1Reproducible --> P1Collect
        
        P1Collect --> P1Store[Store results in memory]
    end
    
    subgraph Phase2["Phase 2: Data Storage"]
        direction TB
        P2Start[Precomputation complete] --> P2Write[Write to fair_results.json]
        P2Write --> P2Structure["JSON Structure:<br/>Array of objects with:<br/>- group_name<br/>- hubmap_id<br/>- dataset_type<br/>- fair: [F, A, I, R]"]
        P2Structure --> P2File[fair/fair_results.json file]
        P2File --> P2Ready[Data ready for application]
    end
    
    subgraph Phase3["Phase 3: Streamlit Application"]
        direction TB
        P3Start([streamlit_test.py launch]) --> P3Load[Load fair_results.json]
        P3Load --> P3Parse[Parse JSON to DataFrame]
        P3Parse --> P3Extract[Extract unique labs and assays]
        P3Extract --> P3UI[Render Streamlit UI]
        
        P3UI --> P3User[User interaction]
        P3User --> P3Select[User selects search type]
        P3Select --> P3Filter[Filter DataFrame]
        
        P3Filter --> P3SearchLab[search_by_lab]
        P3Filter --> P3SearchAssay[search_by_assay]
        P3Filter --> P3SearchBoth[search_by_lab_assay]
        P3Filter --> P3SearchID[search_by_id]
        P3Filter --> P3SearchAll[search_all_id]
        
        P3SearchLab --> P3ExtractFAIR[Extract FAIR scores]
        P3SearchAssay --> P3ExtractFAIR
        P3SearchBoth --> P3ExtractFAIR
        P3SearchID --> P3ExtractFAIR
        P3SearchAll --> P3ExtractFAIR
        
        P3ExtractFAIR --> P3Mean[Calculate mean scores]
        P3Mean --> P3Aggregate[Aggregate: [mean_F, mean_A, mean_I, mean_R]]
        P3Aggregate --> P3Visualize[Create heatmap visualization]
        P3Visualize --> P3Display[Display results to user]
        P3Display --> P3User
    end
    
    P1Store --> P2Start
    P2Ready --> P3Start
    
    subgraph "External Dependencies"
        direction LR
        Ext1[HuBMAP Search API v3]
        Ext2[HuBMAP Entity API]
        Ext3[UNIPROT API]
        Ext4[ORCID API]
        Ext5[DOI URLs]
    end
    
    P1Search -.->|API calls| Ext1
    P1Entity -.->|API calls| Ext2
    P1Findable -.->|Validate| Ext3
    P1Findable -.->|Validate| Ext4
    P1Accessible -.->|Check| Ext5
    
    subgraph "Data Flow"
        direction LR
        DF1[22 University Groups] --> DF2[Dataset IDs]
        DF2 --> DF3[Dataset Objects]
        DF3 --> DF4[DataFrames]
        DF4 --> DF5[FAIR Scores]
        DF5 --> DF6[JSON File]
        DF6 --> DF7[Filtered Results]
        DF7 --> DF8[Aggregated Scores]
        DF8 --> DF9[Visualization]
    end
    
    style Phase1 fill:#e1f5ff
    style Phase2 fill:#fff4e1
    style Phase3 fill:#e1ffe1
    style P1FAIR fill:#ffe1f5
    style P2File fill:#e1ffe1
    style P3Visualize fill:#ffe1f5
    style Start fill:#f0f0f0
```

## System Architecture

### Phase 1: Precomputation (Offline Batch Processing)
**Purpose**: Calculate FAIR scores for all datasets and store results

**Components**:
- **Input**: 22 university group names (hardcoded list)
- **Process**: 
  - Search HuBMAP API for datasets by group
  - Retrieve full metadata for each dataset
  - Convert to structured DataFrames
  - Calculate FAIR scores using 4 modules (33 total checks)
- **Output**: JSON file with all FAIR scores

**Characteristics**:
- Time-intensive (hours of processing)
- Requires network access to HuBMAP APIs
- Runs once or periodically to update data
- Incremental saves prevent data loss

### Phase 2: Data Storage (Persistent Storage)
**Purpose**: Store precomputed results for fast access

**Components**:
- **File**: `fair/fair_results.json`
- **Structure**: Array of objects, each containing:
  - `group_name`: Laboratory/institution name
  - `hubmap_id`: Unique dataset identifier
  - `dataset_type`: Type of assay/experiment
  - `fair`: Array of 4 scores `[Findable, Accessible, Interoperable, Reproducible]`

**Characteristics**:
- Single source of truth for FAIR scores
- Fast to read (local file, no API calls)
- Can be versioned and shared
- Enables offline application usage

### Phase 3: Application Display (Interactive User Interface)
**Purpose**: Provide user-friendly interface to explore FAIR scores

**Components**:
- **Input**: Precomputed JSON file
- **Process**:
  - Load and parse JSON to DataFrame
  - Extract unique values for UI dropdowns
  - Provide filtering by Lab, Assay, Lab+Assay, ID, or All
  - Calculate mean scores for filtered results
  - Generate visualizations
- **Output**: Interactive web interface with heatmaps

**Characteristics**:
- Fast response times (no API calls during use)
- Real-time filtering and aggregation
- User-friendly Streamlit interface
- Supports multiple search/filter modes

## Data Flow Summary

1. **Collection**: 22 university groups → Search API → Dataset IDs → Entity API → Full metadata
2. **Transformation**: Dataset objects → DataFrames → FAIR scoring → Score arrays
3. **Storage**: Score arrays → JSON file → Persistent storage
4. **Retrieval**: JSON file → DataFrame → Filtering → Aggregation
5. **Visualization**: Aggregated scores → Heatmap → User display

## Key Integration Points

### Between Phase 1 and Phase 2
- **process_fair_multi_datastes()**: Processes DataFrames and returns structured results
- **JSON serialization**: Converts Python objects to JSON format
- **File I/O**: Writes to `fair/fair_results.json`

### Between Phase 2 and Phase 3
- **read_json_fair()**: Loads and parses JSON file
- **DataFrame conversion**: Converts JSON array to pandas DataFrame
- **Data validation**: Ensures data integrity before use

### Within Phase 3
- **Search functions**: Filter DataFrame based on user selection
- **Aggregation**: Calculate mean scores across filtered results
- **Visualization**: Generate and display heatmaps

## System Benefits

1. **Separation of Concerns**: Precomputation separated from display logic
2. **Performance**: Fast user experience (no API calls during use)
3. **Scalability**: Can process thousands of datasets offline
4. **Flexibility**: Multiple filtering options for different use cases
5. **Maintainability**: Clear separation between data processing and UI

## Usage Patterns

### Initial Setup
1. Run `create_fair_json.py` to precompute all FAIR scores
2. Wait for completion (may take hours)
3. Verify `fair/fair_results.json` exists and contains data

### Regular Use
1. Launch Streamlit app: `streamlit run streamlit_test.py`
2. App automatically loads precomputed data
3. User selects filters and views results
4. No waiting for API calls or calculations

### Updates
1. Re-run `create_fair_json.py` when new datasets are added
2. Or run incrementally for specific university groups
3. Application automatically uses updated JSON file
