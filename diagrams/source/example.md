# example.py - Diagram

## Description
Example script demonstrating single dataset FAIR scoring. Loops through datasets, calculates FAIR scores for each, and generates visualization plots.

## Flow Diagram

```mermaid
flowchart TD
    Start([Script Start]) --> LoopStart[For each assay in data]
    LoopStart --> GetID[Extract hubmap_id]
    GetID --> CalcFindable[findable]
    GetID --> CalcAccessible[accessible]
    GetID --> CalcInteroperable[interoperable]
    GetID --> CalcReproducible[reproducible]
    
    CalcFindable --> CollectScores[Collect scores]
    CalcAccessible --> CollectScores
    CalcInteroperable --> CollectScores
    CalcReproducible --> CollectScores
    
    CollectScores --> CreatePlot[create_fair_plot]
    CreatePlot --> StoreResults[Store in all_assay_results]
    StoreResults --> LoopCheck{More datasets?}
    LoopCheck -->|Yes| LoopStart
    LoopCheck -->|No| PrintResults[Print all results]
    PrintResults --> End([Complete])
    
    subgraph "FAIR Scoring Modules"
        CalcFindable
        CalcAccessible
        CalcInteroperable
        CalcReproducible
    end
    
    subgraph "Visualization"
        CreatePlot --> Matplotlib[matplotlib visualization]
    end
    
    style Start fill:#e1f5ff
    style End fill:#e1f5ff
    style CollectScores fill:#fff4e1
    style CreatePlot fill:#e1ffe1
```

## Key Components

- **Data dictionary**: Contains assay types and their corresponding HuBMAP IDs
- **FAIR scoring functions**: Calls findable, accessible, interoperable, and reproducible from fair modules
- **create_fair_plot()**: Generates 2x2 heatmap visualization of FAIR scores (imported from fairhelp)
- **Result collection**: Stores tuples of (assay, hubmap_id, scores) for all processed datasets
