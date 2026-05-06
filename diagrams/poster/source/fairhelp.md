# FAIR Heatmap Visualization

## Description
Generation of 2x2 FAIR compliance heatmaps showing Findable, Accessible, Interoperable, and Reproducible metrics for HuBMAP datasets.

## Visualization Generation

```mermaid
flowchart TD
    Start([Receive FAIR Scores]) --> FormatScores[Format FAIR metrics]
    FormatScores --> CreateMatrix[Create 2x2 FAIR matrix]
    CreateMatrix --> ApplyColormap[Apply score colormap]
    ApplyColormap --> AddFAIRLabels[Add F/A/I/R labels]
    AddFAIRLabels --> ExportImage[Export heatmap image]
    ExportImage --> End([Complete])
    
    subgraph "FAIR Matrix Layout"
        CreateMatrix --> MatrixLayout["2x2 FAIR matrix layout"]
        ApplyColormap --> ScoreColors[Color-coded by score]
        AddFAIRLabels --> MetricLabels[FAIR principle labels]
    end
    
    style Start fill:#e1f5ff
    style End fill:#e1ffe1
    style CreateMatrix fill:#fff4e1
    style ExportImage fill:#e1ffe1
```

## Visualization Process

1. **Format Scores**: Prepare FAIR metrics for visualization
2. **Create Matrix**: Generate 2x2 layout with FAIR dimensions
3. **Apply Colormap**: Color-code by compliance score
4. **Export**: Save as publication-ready image
