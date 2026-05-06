# HuBMAP Metadata Retrieval

## Description
Retrieval of comprehensive metadata for a specific HuBMAP tissue mapping dataset from the Entity API.

## Metadata Retrieval

```mermaid
flowchart TD
    Start([Metadata Query]) --> QueryHuBMAP[Query by HuBMAP ID]
    QueryHuBMAP --> RetrieveMetadata[Retrieve dataset metadata]
    RetrieveMetadata --> DisplayMetadata[Display metadata]
    DisplayMetadata --> End([Complete])
    
    style Start fill:#e1f5ff
    style End fill:#e1ffe1
    style RetrieveMetadata fill:#fff4e1
```

## Retrieval Process

1. **Query**: Specify HuBMAP dataset identifier
2. **Retrieve**: Fetch comprehensive metadata from HuBMAP Entity API
3. **Display**: Present dataset information including assay type, identifiers, and metadata
