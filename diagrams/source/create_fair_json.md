# create_fair_json.py - Diagram

## Description
Batch processing pipeline that searches for datasets by university group names, converts them to DataFrames, processes FAIR scores, and writes results to JSON.

## Flow Diagram

```mermaid
flowchart TD
    Start([Main Entry Point]) --> FindUni[find_by_university]
    FindUni --> SearchQuery[SearchInstance_group_name]
    SearchQuery --> SearchAPI[SearchSdk.search]
    SearchAPI --> Convert[convert_to_dataset]
    Convert --> EntityAPI[EntitySdk.get_entity_by_id]
    EntityAPI --> ListToDF[list_objct_to_list_df]
    ListToDF --> DatasetToDF[dataset_to_df]
    DatasetToDF --> ProcessFAIR[process_fair_multi_datastes]
    ProcessFAIR --> WriteJSON[Write to fair_results.json]
    WriteJSON --> End([Complete])
    
    subgraph "FAIR Processing"
        ProcessFAIR --> Findable[findable]
        ProcessFAIR --> Accessible[accessible]
        ProcessFAIR --> Interoperable[interoperable]
        ProcessFAIR --> Reproducible[reproducible]
    end
    
    subgraph "Data Conversion"
        DatasetToDF --> AttrExtract[Extract attributes]
        AttrExtract --> CreateDF[Create DataFrame]
    end
    
    style Start fill:#e1f5ff
    style End fill:#e1f5ff
    style ProcessFAIR fill:#fff4e1
    style WriteJSON fill:#e1ffe1
```

## Key Components

- **find_by_university()**: Searches for datasets by university group names using SearchSdk
- **convert_to_dataset()**: Converts search query results to Dataset objects using EntitySdk
- **list_objct_to_list_df()**: Converts list of Dataset objects to list of DataFrames
- **dataset_to_df()**: Converts a single Dataset object to a DataFrame row
- **process_fair_multi_datastes()**: Processes FAIR scores for multiple datasets (imported from fair.utils)
- **Main flow**: Orchestrates the entire batch processing pipeline and writes results to JSON
