# HuBMAP FAIR Score Visualization Interface

## Description
Interactive web application for exploring and visualizing FAIR compliance scores across HuBMAP datasets with filtering by Tissue Mapping Center, assay type, and dataset identifiers.

## FAIR Score Explorer Interface

```mermaid
flowchart TD
    Start([Launch FAIR Explorer]) --> LoadAssessments[Load FAIR assessment results]
    LoadAssessments --> DisplayFilters[Display filtering options]
    
    DisplayFilters --> UserSelection[User selects filter criteria]
    UserSelection --> FilterCriteria{Filter by?}
    
    FilterCriteria -->|TMC| FilterTMC[Filter by Tissue Mapping Center]
    FilterCriteria -->|Assay| FilterAssay[Filter by assay type]
    FilterCriteria -->|Both| FilterCombined[Filter by TMC and assay]
    FilterCriteria -->|Dataset| FilterDataset[Filter by HuBMAP ID]
    FilterCriteria -->|All| ShowAllDatasets[Show all datasets]
    
    FilterTMC --> ComputeAggregate[Compute aggregate FAIR scores]
    FilterAssay --> ComputeAggregate
    FilterCombined --> ComputeAggregate
    FilterDataset --> ComputeAggregate
    ShowAllDatasets --> ComputeAggregate
    
    ComputeAggregate --> GenerateHeatmap[Generate FAIR heatmap]
    GenerateHeatmap --> DisplayVisualization[Display results]
    DisplayVisualization --> UserSelection
    
    subgraph "Filtering Criteria"
        FilterTMC
        FilterAssay
        FilterCombined
        FilterDataset
        ShowAllDatasets
    end
    
    subgraph "FAIR Visualization"
        GenerateHeatmap --> HeatmapDisplay[2x2 FAIR matrix layout]
        HeatmapDisplay --> ScoreBreakdown[Individual metric scores]
    end
    
    style Start fill:#e1f5ff
    style LoadAssessments fill:#fff4e1
    style ComputeAggregate fill:#e1ffe1
    style GenerateHeatmap fill:#ffe1f5
```

## Interface Features

- **Multi-criteria Filtering**: Filter by Tissue Mapping Center, assay type, or specific HuBMAP dataset ID
- **Aggregate Analysis**: Compute mean FAIR scores across filtered datasets
- **FAIR Heatmap Visualization**: Generate 2x2 matrix showing Findable, Accessible, Interoperable, and Reproducible scores
- **Interactive Exploration**: Dynamically adjust filters to compare FAIR compliance across different dataset subsets
