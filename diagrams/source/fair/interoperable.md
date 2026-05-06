# fair/interoperable.py - Diagram

## Description
Interoperable scoring module that evaluates dataset interoperability based on 7 criteria including genetic sequences, assay information, versioning, and antibody metadata.

## Flow Diagram

```mermaid
flowchart TD
    Start([interoperable function]) --> GetMetadata[__get_metadata]
    GetMetadata --> CheckGenetic[__has_genetic_sequences]
    GetMetadata --> CheckAssayCategory[__has_assay_category]
    GetMetadata --> CheckAssayType[__has_assay_type]
    GetMetadata --> CheckContributorsPath[__has_contributors_path]
    GetMetadata --> CheckVersion[__has_version]
    GetMetadata --> CheckAncestors[__has_direct_ancestors]
    GetMetadata --> CheckAntibodyVersion[__has_antibody_version]
    
    CheckGenetic --> CollectScores[Collect all scores]
    CheckAssayCategory --> CollectScores
    CheckAssayType --> CollectScores
    CheckContributorsPath --> CollectScores
    CheckVersion --> CollectScores
    CheckAncestors --> CollectScores
    CheckAntibodyVersion --> CollectScores
    
    CollectScores --> CalcMean[Calculate mean score]
    CalcMean --> ReturnResult[Return result and score list]
    ReturnResult --> End([Complete])
    
    subgraph "Assay Validation"
        CheckAssayCategory --> ValidCategories{Valid category?}
        ValidCategories -->|imaging/sequence/None| Pass1[Score = 1]
        CheckAssayType --> ValidTypes{Valid type?}
        ValidTypes -->|CODEX/IMC/etc| Pass2[Score = 1]
    end
    
    subgraph "Metadata Checks"
        CheckContributorsPath --> CheckKey[Check key in metadata]
        CheckVersion --> CheckKey
        CheckGenetic --> CheckKey
    end
    
    subgraph "Relationship Checks"
        CheckAncestors --> CompareIDs[Compare hubmap_ids]
        CheckAntibodyVersion --> CheckAntibodyKey[Check version in antibody]
    end
    
    style Start fill:#e1f5ff
    style End fill:#e1f5ff
    style CollectScores fill:#fff4e1
    style CalcMean fill:#e1ffe1
```

## Key Components

- **interoperable()**: Main function that calculates interoperability score (0-1)
- **__has_genetic_sequences()**: Checks if contains_human_genetic_sequences field exists
- **__has_assay_category()**: Validates assay_category is one of: imaging, sequence, or None
- **__has_assay_type()**: Validates assay_type against predefined list of valid types
- **__has_contributors_path()**: Verifies contributors_path exists in metadata
- **__has_version()**: Verifies version field exists in metadata
- **__has_direct_ancestors()**: Validates direct_ancestors relationship consistency
- **__has_antibody_version()**: Checks if antibodies have version information
- **Score calculation**: Returns mean of all 7 interoperability criteria checks
