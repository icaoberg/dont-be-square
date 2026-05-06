# metadata.py - Diagram

## Description
Simple example script demonstrating metadata retrieval for a HuBMAP dataset using the fairhelp module.

## Flow Diagram

```mermaid
flowchart TD
    Start([Script Start]) --> SetID[Set hubmap_id]
    SetID --> GetMetadata[__get_metadata]
    GetMetadata --> PrintResult[Print metadata]
    PrintResult --> End([Complete])
    
    subgraph "Metadata Retrieval"
        GetMetadata --> API[Entity API Call]
        API --> ReturnMetadata[Return metadata dict]
    end
    
    style Start fill:#e1f5ff
    style End fill:#e1f5ff
    style GetMetadata fill:#fff4e1
```

## Key Components

- **hubmap_id**: Hardcoded dataset ID "HBM666.NDQZ.365"
- **__get_metadata()**: Internal function from fairhelp module that retrieves metadata from HuBMAP Entity API
- **Simple demonstration**: Shows basic usage pattern for metadata retrieval
