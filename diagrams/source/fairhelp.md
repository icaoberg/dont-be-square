# fairhelp.py - Diagram

## Description
Helper module providing visualization utilities for FAIR scores. Creates 2x2 heatmap plots using matplotlib and provides Streamlit integration for status display.

## Flow Diagram

```mermaid
flowchart TD
    Start([Function Call]) --> ValidateInput[Validate input shape 2x2]
    ValidateInput --> CheckValues[Check values <= 1]
    CheckValues --> SetupOutput[Setup output file path]
    SetupOutput --> CreateLabels[Create F/A/I/R labels]
    CreateLabels --> MaskData[Mask negative values]
    MaskData --> CreateColormap[Create blue-white-red colormap]
    CreateColormap --> CreateFigure[Create matplotlib figure]
    CreateFigure --> AddSubplot[Add subplot with GridSpec]
    AddSubplot --> DisplayHeatmap[Display heatmap with imshow]
    DisplayHeatmap --> AddLabels[Add text labels F/A/I/R]
    AddLabels --> AddColorbar[Add colorbar]
    AddColorbar --> SavePlot[Save plot to file]
    SavePlot --> End([Return file path])
    
    subgraph "Streamlit Functions"
        ShowLogs[show_logs_in_streamlit]
        ShowStatus[show_status]
    end
    
    subgraph "Plot Configuration"
        CreateColormap --> SetBadColor[Set bad color to white]
        CreateFigure --> SetFigSize[Set figure size with scale]
    end
    
    style Start fill:#e1f5ff
    style End fill:#e1f5ff
    style DisplayHeatmap fill:#fff4e1
    style SavePlot fill:#e1ffe1
```

## Key Components

- **create_fair_plot()**: Main function that creates a 2x2 heatmap visualization
  - Validates input is 2x2 array with values <= 1
  - Creates blue-white-red colormap for score visualization
  - Labels positions as F (Findable), A (Accessible), I (Interoperable), R (Reproducible)
  - Saves plot to output directory with timestamp
  
- **show_logs_in_streamlit()**: Displays execution logs in Streamlit interface
- **show_status()**: Displays labeled status with success/error indicators in Streamlit
- **Logging setup**: Configures file and Streamlit handlers for logging
