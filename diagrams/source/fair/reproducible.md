# fair/reproducible.py - Diagram

## Description
Reproducible scoring module that evaluates dataset reproducibility based on 11 criteria including metadata consistency, resolution information, dataset type, and instrument details.

## Flow Diagram

```mermaid
flowchart TD
    Start([reproducible function]) --> GetMetadata[__get_metadata]
    GetMetadata --> CheckMetadataSuccess[__average_metadata_success]
    GetMetadata --> CheckResXUnit[__has_resolution_x_unit]
    GetMetadata --> CheckResXValue[__has_resolution_x_value]
    GetMetadata --> CheckResYUnit[__has_resolution_y_unit]
    GetMetadata --> CheckResYValue[__has_resolution_y_value]
    GetMetadata --> CheckResZUnit[__has_resolution_z_unit]
    GetMetadata --> CheckResZValue[__has_resolution_z_value]
    GetMetadata --> CheckDatasetType[__has_dataset_type]
    GetMetadata --> CheckAnalyteClass[__has_analyte_class]
    GetMetadata --> CheckPrepKit[__has_preparation_instrument_kit]
    GetMetadata --> CheckAcqModel[__has_acquisition_instrument_model]
    
    CheckMetadataSuccess --> CollectScores[Collect all scores]
    CheckResXUnit --> CollectScores
    CheckResXValue --> CollectScores
    CheckResYUnit --> CollectScores
    CheckResYValue --> CollectScores
    CheckResZUnit --> CollectScores
    CheckResZValue --> CollectScores
    CheckDatasetType --> CollectScores
    CheckAnalyteClass --> CollectScores
    CheckPrepKit --> CollectScores
    CheckAcqModel --> CollectScores
    
    CollectScores --> CalcMean[Calculate mean score]
    CalcMean --> ReturnResult[Return result and score list]
    ReturnResult --> End([Complete])
    
    subgraph "Metadata Consistency"
        CheckMetadataSuccess --> MultipleTrials[Multiple API calls 3-10]
        MultipleTrials --> CheckSuccess{All successful?}
        CheckSuccess --> SuccessRate[Calculate success rate]
    end
    
    subgraph "Resolution Validation"
        CheckResXUnit --> ValidateUnit[Check unit is string]
        CheckResXValue --> ValidateValue[Check value is numeric]
        CheckResYUnit --> ValidateUnit
        CheckResYValue --> ValidateValue
        CheckResZUnit --> ValidateUnit
        CheckResZValue --> ValidateValue
    end
    
    subgraph "Type Validation"
        CheckDatasetType --> ValidTypes{Valid dataset type?}
        CheckAnalyteClass --> ValidClasses{Valid analyte class?}
        ValidTypes -->|CODEX/IMC/etc| Pass1[Score = 1]
        ValidClasses -->|Protein/RNA/DNA/None| Pass2[Score = 1]
    end
    
    subgraph "Instrument Checks"
        CheckPrepKit --> IsString1[Check is string]
        CheckAcqModel --> IsString2[Check is string]
    end
    
    style Start fill:#e1f5ff
    style End fill:#e1f5ff
    style CollectScores fill:#fff4e1
    style CalcMean fill:#e1ffe1
```

## Key Components

- **reproducible()**: Main function that calculates reproducibility score (0-1)
- **__average_metadata_success()**: Tests metadata retrieval consistency with multiple API calls (3-10 trials)
- **Resolution checks**: Validates X, Y, Z resolution units (strings) and values (numeric)
  - **__has_resolution_x/y/z_unit()**: Checks unit is valid string type
  - **__has_resolution_x/y/z_value()**: Checks value is numeric (float-convertible)
- **__has_dataset_type()**: Validates dataset_type against extensive list of valid types
- **__has_analyte_class()**: Validates analyte_class is one of: Protein, RNA, DNA, or None
- **__has_preparation_instrument_kit()**: Verifies preparation_instrument_kit is a string
- **__has_acquisition_instrument_model()**: Verifies acquisition_instrument_model is a string
- **Score calculation**: Returns mean of all 11 reproducibility criteria checks
