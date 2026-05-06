# testing_utils.py - Diagram

## Description
Testing utility script that demonstrates various search and filtering capabilities using the fair.utils module. Tests searching by lab, assay type, and combinations.

## Flow Diagram

```mermaid
flowchart TD
    Start([Script Start]) --> ReadJSON[read_json_fair]
    ReadJSON --> SetParams[Set assay and name variables]
    SetParams --> TestLab[Test search_by_lab]
    TestLab --> MeanLab[mean_fair_results]
    MeanLab --> HeatmapLab[create_heatmap_for]
    HeatmapLab --> TestAssay[Test search_by_assay]
    TestAssay --> MeanAssay[mean_fair_results]
    MeanAssay --> HeatmapAssay[create_heatmap_for]
    HeatmapAssay --> TestBoth[Test search_by_lab_assay]
    TestBoth --> MeanBoth[mean_fair_results]
    MeanBoth --> HeatmapBoth[create_heatmap_for]
    HeatmapBoth --> End([Complete])
    
    subgraph "Search Operations"
        TestLab --> FilterLab[Filter by group_name]
        TestAssay --> FilterAssay[Filter by dataset_type]
        TestBoth --> FilterBoth[Filter by both]
    end
    
    subgraph "Result Processing"
        MeanLab --> CalcMean[Calculate mean scores]
        MeanAssay --> CalcMean
        MeanBoth --> CalcMean
    end
    
    style Start fill:#e1f5ff
    style End fill:#e1f5ff
    style ReadJSON fill:#fff4e1
    style HeatmapLab fill:#e1ffe1
    style HeatmapAssay fill:#e1ffe1
    style HeatmapBoth fill:#e1ffe1
```

## Key Components

- **read_json_fair()**: Loads FAIR results from JSON file
- **search_by_lab()**: Filters datasets by laboratory/group name
- **search_by_assay()**: Filters datasets by assay type
- **search_by_lab_assay()**: Filters by both lab and assay type
- **mean_fair_results()**: Calculates average FAIR scores from filtered results
- **create_heatmap_for()**: Generates and displays heatmap visualization
- **Testing pattern**: Demonstrates usage of utility functions with example parameters
