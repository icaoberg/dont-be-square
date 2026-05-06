# streamlit_app.py - Diagram

## Description
Basic Streamlit web application for FAIR score visualization. Allows users to input a HuBMAP dataset ID and displays calculated FAIR scores with a heatmap visualization.

## Flow Diagram

```mermaid
flowchart TD
    Start([App Start]) --> RenderUI[Render Streamlit UI]
    RenderUI --> UserInput[User enters hubmap_id]
    UserInput --> ButtonClick{Button clicked?}
    ButtonClick -->|No| Wait[Wait for input]
    ButtonClick -->|Yes| CalcFindable[findable]
    ButtonClick -->|Yes| CalcAccessible[accessible]
    ButtonClick -->|Yes| CalcInteroperable[interoperable]
    ButtonClick -->|Yes| CalcReproducible[reproducible]
    
    CalcFindable --> CollectScores[Collect FAIR scores]
    CalcAccessible --> CollectScores
    CalcInteroperable --> CollectScores
    CalcReproducible --> CollectScores
    
    CollectScores --> DisplayScores[Display individual scores]
    CollectScores --> ReshapeArray[Reshape to 2x2 array]
    ReshapeArray --> CreatePlot[create_fair_plot]
    CreatePlot --> DisplayImage[Display image in Streamlit]
    DisplayImage --> Wait
    
    Wait --> ButtonClick
    
    subgraph "FAIR Scoring"
        CalcFindable
        CalcAccessible
        CalcInteroperable
        CalcReproducible
    end
    
    subgraph "UI Components"
        RenderUI --> Title[Title]
        RenderUI --> TextInput[Text input field]
        RenderUI --> Button[Calculate button]
    end
    
    style Start fill:#e1f5ff
    style DisplayImage fill:#e1ffe1
    style CollectScores fill:#fff4e1
```

## Key Components

- **Streamlit UI**: Simple interface with text input and button
- **FAIR score calculation**: Calls all four FAIR scoring functions (findable, accessible, interoperable, reproducible)
- **Score display**: Shows individual scores as markdown list
- **Heatmap visualization**: Creates and displays 2x2 FAIR heatmap using fairhelp.create_fair_plot()
- **Error handling**: Try-except block for graceful error handling
