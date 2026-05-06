# Precomputation and Data Loading System

## Description
This diagram shows the complete precomputation pipeline that processes HuBMAP datasets, calculates FAIR scores, and stores results in `fair_results.json`. This is a batch processing system that runs offline to preload all FAIR calculations.

## Precomputation Flow Diagram

```mermaid
flowchart TD
    Start([Script Execution: create_fair_json.py]) --> InitSDK[Initialize HuBMAP SDKs]
    InitSDK --> SearchSDK[SearchSdk instance]
    InitSDK --> EntitySDK[EntitySdk instance]
    
    SearchSDK --> FindUni[find_by_university]
    FindUni --> LoopGroups[Loop through 22 university groups]
    
    LoopGroups --> CreateQuery[SearchInstance_group_name]
    CreateQuery --> SearchAPI[SearchSdk.search API call]
    SearchAPI --> GetHits[Extract hit IDs from results]
    GetHits --> ConvertDatasets[convert_to_dataset]
    
    ConvertDatasets --> LoopHits[Loop through each hit]
    LoopHits --> GetEntity[EntitySdk.get_entity_by_id]
    GetEntity --> AddToList[Add Dataset object to list]
    AddToList --> Sleep[Sleep 1 second]
    Sleep --> MoreHits{More hits?}
    MoreHits -->|Yes| LoopHits
    MoreHits -->|No| MoreGroups{More groups?}
    MoreGroups -->|Yes| LoopGroups
    MoreGroups -->|No| ListToDF[list_objct_to_list_df]
    
    ListToDF --> LoopDatasets[Loop through all datasets]
    LoopDatasets --> DatasetToDF[dataset_to_df]
    DatasetToDF --> ExtractAttrs[Extract all attributes]
    ExtractAttrs --> CreateDFRow[Create DataFrame row]
    CreateDFRow --> AddToDFList[Add to DataFrame list]
    AddToDFList --> MoreDFs{More datasets?}
    MoreDFs -->|Yes| LoopDatasets
    MoreDFs -->|No| ProcessFAIR[process_fair_multi_datastes]
    
    ProcessFAIR --> LoopDataFrames[Loop through each DataFrame]
    LoopDataFrames --> ExtractID[Extract hubmap_id]
    ExtractID --> CalcFindable[findable module]
    ExtractID --> CalcAccessible[accessible module]
    ExtractID --> CalcInteroperable[interoperable module]
    ExtractID --> CalcReproducible[reproducible module]
    
    CalcFindable --> GetMetadata1[Get metadata from API]
    CalcAccessible --> GetMetadata2[Get metadata from API]
    CalcInteroperable --> GetMetadata3[Get metadata from API]
    CalcReproducible --> GetMetadata4[Get metadata from API]
    
    GetMetadata1 --> ScoreFindable[Calculate findable score]
    GetMetadata2 --> ScoreAccessible[Calculate accessible score]
    GetMetadata3 --> ScoreInteroperable[Calculate interoperable score]
    GetMetadata4 --> ScoreReproducible[Calculate reproducible score]
    
    ScoreFindable --> CollectFAIR[Collect F/A/I/R scores]
    ScoreAccessible --> CollectFAIR
    ScoreInteroperable --> CollectFAIR
    ScoreReproducible --> CollectFAIR
    
    CollectFAIR --> CreateResult[Create result dictionary]
    CreateResult --> StoreResult[Store in all_assay_results]
    StoreResult --> WriteJSON[Write to fair_results.json]
    WriteJSON --> MoreDataFrames{More DataFrames?}
    MoreDataFrames -->|Yes| LoopDataFrames
    MoreDataFrames -->|No| End([Precomputation Complete])
    
    subgraph "HuBMAP API Integration"
        SearchAPI --> SearchEndpoint[Search API v3]
        GetEntity --> EntityEndpoint[Entity API]
    end
    
    subgraph "FAIR Scoring Modules"
        CalcFindable --> FindableChecks[8 findability checks]
        CalcAccessible --> AccessibleChecks[7 accessibility checks]
        CalcInteroperable --> InteroperableChecks[7 interoperability checks]
        CalcReproducible --> ReproducibleChecks[11 reproducibility checks]
    end
    
    subgraph "Data Storage"
        WriteJSON --> JSONFile[fair/fair_results.json]
        JSONFile --> JSONStructure["Array of objects:<br/>- group_name<br/>- hubmap_id<br/>- dataset_type<br/>- fair: [F,A,I,R]"]
    end
    
    style Start fill:#e1f5ff
    style End fill:#e1ffe1
    style ProcessFAIR fill:#fff4e1
    style WriteJSON fill:#ffe1f5
    style JSONFile fill:#e1ffe1
```

## Key Components

### Data Collection Phase
- **22 University Groups**: Hardcoded list of all participating institutions
- **SearchSdk**: Searches for datasets by group name (size: 1700 per group)
- **EntitySdk**: Retrieves full dataset metadata for each found ID
- **Rate Limiting**: 1 second sleep between API calls to avoid overwhelming the API

### Data Transformation Phase
- **Dataset Objects → DataFrames**: Converts SDK Dataset objects to pandas DataFrames
- **Attribute Extraction**: Dynamically extracts all attributes from Dataset objects
- **DataFrame List**: Creates list of DataFrames, one per dataset

### FAIR Scoring Phase
- **process_fair_multi_datastes()**: Main processing function that iterates through DataFrames
- **Four FAIR Modules**: Calls findable, accessible, interoperable, and reproducible for each dataset
- **Metadata Caching**: Each FAIR module fetches and caches metadata to JSON/ folder
- **Score Aggregation**: Collects all four scores into [F, A, I, R] array

### Storage Phase
- **Incremental Writing**: Writes JSON after processing each DataFrame (allows progress tracking)
- **JSON Structure**: Array of objects containing group_name, hubmap_id, dataset_type, and fair scores
- **Output Location**: `fair/fair_results.json`

## Performance Characteristics
- **Batch Processing**: Processes all datasets offline
- **Time Intensive**: Can take hours depending on number of datasets
- **API Dependent**: Requires network access to HuBMAP APIs
- **Incremental Saves**: Progress is saved after each DataFrame to prevent data loss
