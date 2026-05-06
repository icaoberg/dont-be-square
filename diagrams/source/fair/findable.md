# fair/findable.py - Diagram

## Description
Findable scoring module that evaluates dataset findability based on 8 criteria including metadata quality, identifiers, publication status, and contributor information.

## Flow Diagram

```mermaid
flowchart TD
    Start([findable function]) --> GetMetadata[__get_metadata]
    GetMetadata --> CheckNoError[__no_error]
    GetMetadata --> CheckAntibodies[__has_antibodies]
    GetMetadata --> CheckUUID[__has_uuid]
    GetMetadata --> CheckEntityType[__is_dataset_entity]
    GetMetadata --> CheckTitle[__has_title]
    GetMetadata --> CheckPublished[__is_published]
    GetMetadata --> CheckContributors[__has_contributors]
    GetMetadata --> CheckContacts[__has_contacts]
    
    CheckNoError --> CollectScores[Collect all scores]
    CheckAntibodies --> CollectScores
    CheckUUID --> CollectScores
    CheckEntityType --> CollectScores
    CheckTitle --> CollectScores
    CheckPublished --> CollectScores
    CheckContributors --> CollectScores
    CheckContacts --> CollectScores
    
    CollectScores --> CalcMean[Calculate mean score]
    CalcMean --> ReturnResult[Return result and score list]
    ReturnResult --> End([Complete])
    
    subgraph "Antibody Validation"
        CheckAntibodies --> LoopAntibodies[Loop through antibodies]
        LoopAntibodies --> CheckUniprot[Check UNIPROT accession]
        CheckUniprot --> ValidateURL[Validate UNIPROT URL]
        ValidateURL --> AllValid{All valid?}
    end
    
    subgraph "ORCID Validation"
        CheckContributors --> ExtractORCID[Extract ORCID ID]
        CheckContacts --> ExtractORCID
        ExtractORCID --> ValidateORCID[check_orcid]
        ValidateORCID --> ORCIDAPI[ORCID API request]
    end
    
    subgraph "Metadata Helpers"
        CheckPublished --> GetStatus[Get status field]
        CheckUUID --> HasKey[Check key exists]
        CheckEntityType --> CheckValue[Check entity_type == Dataset]
        CheckTitle --> HasKey
    end
    
    style Start fill:#e1f5ff
    style End fill:#e1f5ff
    style CollectScores fill:#fff4e1
    style CalcMean fill:#e1ffe1
```

## Key Components

- **findable()**: Main function that calculates findability score (0-1)
- **__get_metadata()**: Retrieves metadata from HuBMAP Entity API and caches to JSON
- **__no_error()**: Checks if metadata retrieval was successful (no error field)
- **__has_antibodies()**: Validates antibodies against UNIPROT database
- **__has_uuid()**: Verifies UUID exists in metadata
- **__is_dataset_entity()**: Verifies entity_type is "Dataset"
- **__has_title()**: Verifies title exists in metadata
- **__is_published()**: Checks if dataset status is "Published"
- **__has_contributors()**: Validates contributors exist and have valid ORCID
- **__has_contacts()**: Validates contacts exist and have valid ORCID
- **check_orcid()**: Validates ORCID ID against ORCID API
- **Score calculation**: Returns mean of all 8 findability criteria checks
