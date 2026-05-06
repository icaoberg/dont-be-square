flowchart TD
    Start([Launch FAIR Explorer]) --> LoadAssessments[Load FAIR assessment results]
    LoadAssessments --> UserSelection[Display filtering options]
    UserSelection --> |User selects filter criteria| FilterCriteria{Filter by}
    
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

    subgraph "Filtering Criteria"
        FilterTMC
        FilterAssay
        FilterCombined
        FilterDataset
        ShowAllDatasets
    end
    
    subgraph "FAIR Evaluation"
    ComputeAggregate --> GenerateHeatmap[Generate FAIR heatmap]
        GenerateHeatmap --> HeatmapDisplay[2x2 FAIR matrix layout]
    end
    HeatmapDisplay --> d[Display Heatmap]
    style Start fill:#e1f5ff
    style LoadAssessments fill:#fff4e1
    style ComputeAggregate fill:#e1ffe1
    style GenerateHeatmap fill:#ffe1f5