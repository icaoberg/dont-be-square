# HuBMAP FAIR Score Comparative Explorer

## Description
Advanced interactive interface for comparative analysis of FAIR compliance scores across HuBMAP datasets with multi-criteria filtering and aggregate visualization.

## Comparative Explorer

```mermaid
flowchart TD
    Start([Launch Explorer]) --> LoadAssessments[Load FAIR assessments]
    LoadAssessments --> SelectCriteria[Select filter criteria]
    SelectCriteria --> ApplyFilter[Apply filter]
    ApplyFilter --> ComputeAggregate[Compute aggregate FAIR scores]
    ComputeAggregate --> GenerateVisualization[Generate FAIR heatmap]
    GenerateVisualization --> DisplayResults[Display comparative results]
    DisplayResults --> SelectCriteria
    
    subgraph "Filtering Criteria"
        SelectCriteria --> ByTMC[By Tissue Mapping Center]
        SelectCriteria --> ByAssay[By assay type]
        SelectCriteria --> ByCombined[By TMC and assay]
        SelectCriteria --> ByHuBMAPID[By HuBMAP dataset ID]
        SelectCriteria --> AllDatasets[All datasets]
    end
    
    style Start fill:#e1f5ff
    style LoadAssessments fill:#fff4e1
    style ComputeAggregate fill:#e1ffe1
    style GenerateVisualization fill:#ffe1f5
```

## Explorer Features

- **Multi-criteria Filtering**: Filter by Tissue Mapping Center, assay type, or specific HuBMAP dataset
- **Aggregate Analysis**: Compute mean FAIR scores across filtered dataset subsets
- **Comparative Visualization**: Generate FAIR heatmaps for comparative analysis
- **Interactive Exploration**: Dynamically adjust filters to compare compliance patterns
