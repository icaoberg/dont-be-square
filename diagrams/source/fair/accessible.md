# fair/accessible.py - Diagram

## Description
Accessible scoring module that evaluates dataset accessibility based on 7 criteria including DOI URLs, group information, and protocol accessibility.

## Flow Diagram

```mermaid
flowchart TD
    Start([accessible function]) --> GetMetadata[__get_metadata]
    GetMetadata --> CheckDOI[Check doi_url accessible]
    GetMetadata --> CheckGroupName[__has_group_name]
    GetMetadata --> CheckGroupUUID[__has_group_uuid]
    GetMetadata --> CheckHubmapID[__has_hubmap_id]
    GetMetadata --> CheckRegDOI[__has_register_doi]
    GetMetadata --> CheckProtocolDOI[__has_protocols_io_doi]
    GetMetadata --> CheckReagentDOI[__has_reagent_prep_protocols_io_doi]
    
    CheckDOI --> CollectScores[Collect all scores]
    CheckGroupName --> CollectScores
    CheckGroupUUID --> CollectScores
    CheckHubmapID --> CollectScores
    CheckRegDOI --> CollectScores
    CheckProtocolDOI --> CollectScores
    CheckReagentDOI --> CollectScores
    
    CollectScores --> CalcMean[Calculate mean score]
    CalcMean --> ReturnResult[Return result and score list]
    ReturnResult --> End([Complete])
    
    subgraph "URL Accessibility Checks"
        CheckDOI --> IsLinkAccessible[__is_link_accessible]
        CheckRegDOI --> IsLinkAccessible
        CheckProtocolDOI --> IsLinkAccessible
        CheckReagentDOI --> IsLinkAccessible
        IsLinkAccessible --> HTTPRequest[HTTP GET request]
    end
    
    subgraph "Metadata Checks"
        CheckGroupName --> HasValue[Check if value exists]
        CheckGroupUUID --> HasValue
        CheckHubmapID --> HasValue
    end
    
    style Start fill:#e1f5ff
    style End fill:#e1f5ff
    style CollectScores fill:#fff4e1
    style CalcMean fill:#e1ffe1
```

## Key Components

- **accessible()**: Main function that calculates accessibility score (0-1)
- **__is_link_accessible()**: Checks if a URL is accessible via HTTP request
- **__has_group_name()**: Verifies group_name exists in metadata
- **__has_group_uuid()**: Verifies group_uuid exists in metadata
- **__has_hubmap_id()**: Verifies hubmap_id exists in metadata
- **__has_register_doi()**: Checks if registered DOI exists and is accessible
- **__has_protocols_io_doi()**: Checks if protocols.io DOI exists and is accessible
- **__has_reagent_prep_protocols_io_doi()**: Checks if reagent prep protocol DOI exists and is accessible
- **Score calculation**: Returns mean of all 7 accessibility criteria checks
