# FAIR Assessment Filtering Examples

## Description
Demonstration of various filtering strategies for exploring FAIR compliance patterns across HuBMAP datasets by Tissue Mapping Center and assay type.

## Filtering Workflow

```mermaid
flowchart TD
    Start([Load Assessments]) --> LoadFAIRScores[Load FAIR assessment results]
    LoadFAIRScores --> TestFilters[Test filtering strategies]
    TestFilters --> ComputeAggregate[Compute aggregate metrics]
    ComputeAggregate --> GenerateHeatmaps[Generate FAIR heatmaps]
    GenerateHeatmaps --> End([Complete])
    
    subgraph "Filtering Strategies"
        TestFilters --> ByTMC[By Tissue Mapping Center]
        TestFilters --> ByAssay[By assay type]
        TestFilters --> ByCombined[By TMC and assay]
    end
    
    style Start fill:#e1f5ff
    style End fill:#e1ffe1
    style TestFilters fill:#fff4e1
    style GenerateHeatmaps fill:#e1ffe1
```

## Filtering Process

1. **Load**: Load precomputed FAIR assessment results
2. **Test Filters**: Apply different filtering criteria (TMC, assay type, combinations)
3. **Compute Aggregate**: Calculate mean FAIR scores for filtered subsets
4. **Visualize**: Generate comparative FAIR heatmap visualizations
