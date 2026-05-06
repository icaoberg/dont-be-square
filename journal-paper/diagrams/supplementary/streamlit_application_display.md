# Streamlit Application Display System

## Description
This diagram shows how the Streamlit application (`streamlit_test.py`) loads precomputed FAIR data, provides filtering capabilities, and displays aggregated results with visualizations. This is the main user-facing application.

## Streamlit Application Flow Diagram

```mermaid
flowchart TD
    Start([Streamlit App Launch]) --> CheckFile[Check fair_results.json exists]
    CheckFile -->|Not Found| ErrorDisplay[Display error and stop]
    CheckFile -->|Found| ReadJSON[read_json_fair]
    
    ReadJSON --> ParseJSON[Parse JSON to DataFrame]
    ParseJSON --> ValidateData[Validate DataFrame]
    ValidateData -->|Invalid| ErrorDisplay
    ValidateData -->|Valid| ExtractLists[Extract unique values]
    
    ExtractLists --> GroupList[group_list: Extract labs]
    ExtractLists --> TypeList[type_list: Extract assay types]
    
    GroupList --> RenderUI[Render Streamlit UI]
    TypeList --> RenderUI
    
    RenderUI --> DisplayTitle[Display App Title]
    RenderUI --> DisplayCount[Display total datasets count]
    RenderUI --> RenderRadio[Render search type radio buttons]
    
    RenderRadio --> UserSelect[User selects search type]
    UserSelect --> RouteSelection{Search Type?}
    
    RouteSelection -->|Lab| ShowLabDropdown[Show lab selectbox]
    RouteSelection -->|Assay type| ShowAssayDropdown[Show assay selectbox]
    RouteSelection -->|Lab and Assay| ShowBothDropdowns[Show both selectboxes]
    RouteSelection -->|Hubmap id| ShowTextInput[Show text input field]
    RouteSelection -->|All datasets| ShowAllOption[No additional input]
    
    ShowLabDropdown --> WaitButton[Wait for Calculate button]
    ShowAssayDropdown --> WaitButton
    ShowBothDropdowns --> WaitButton
    ShowTextInput --> WaitButton
    ShowAllOption --> WaitButton
    
    WaitButton --> ButtonClicked{Button clicked?}
    ButtonClicked -->|No| WaitButton
    ButtonClicked -->|Yes| RouteSearch{Route to search function}
    
    RouteSearch -->|Lab| SearchLab[search_by_lab]
    RouteSearch -->|Assay| SearchAssay[search_by_assay]
    RouteSearch -->|Both| SearchBoth[search_by_lab_assay]
    RouteSearch -->|ID| SearchID[search_by_id]
    RouteSearch -->|All| SearchAll[search_all_id]
    
    SearchLab --> FilterDF1[Filter DataFrame by group_name]
    SearchAssay --> FilterDF2[Filter DataFrame by dataset_type]
    SearchBoth --> FilterDF3[Filter by group_name AND dataset_type]
    SearchID --> FilterDF4[Filter DataFrame by hubmap_id]
    SearchAll --> NoFilter[No filtering needed]
    
    FilterDF1 --> ExtractFAIR[find_fair_results]
    FilterDF2 --> ExtractFAIR
    FilterDF3 --> ExtractFAIR
    FilterDF4 --> ExtractFAIR
    NoFilter --> ExtractFAIR
    
    ExtractFAIR --> CheckResults{Results empty?}
    CheckResults -->|Yes| ErrorNoResults[Display error: No results found]
    CheckResults -->|No| CalcMean[mean_fair_results]
    
    CalcMean --> SeparateScores[Separate F/A/I/R scores]
    SeparateScores --> CalcFMean[Calculate mean of Findable]
    SeparateScores --> CalcAMean[Calculate mean of Accessible]
    SeparateScores --> CalcIMean[Calculate mean of Interoperable]
    SeparateScores --> CalcRMean[Calculate mean of Reproducible]
    
    CalcFMean --> AggregateScores[Create result array: [F, A, I, R]]
    CalcAMean --> AggregateScores
    CalcIMean --> AggregateScores
    CalcRMean --> AggregateScores
    
    AggregateScores --> CreateHeatmap[create_heatmap_for]
    CreateHeatmap --> DisplayScores[Display individual scores as markdown]
    CreateHeatmap --> ReshapeArray[Reshape to 2x2 array]
    ReshapeArray --> CallPlot[fairhelp.create_fair_plot]
    CallPlot --> GenerateImage[Generate PNG heatmap]
    GenerateImage --> DisplayImage[Display image in Streamlit]
    DisplayImage --> DisplayLabel[Display search label]
    DisplayLabel --> SuccessMessage[Display success message]
    SuccessMessage --> WaitButton
    
    subgraph "Data Loading"
        ReadJSON --> FileIO[File I/O operations]
        ParseJSON --> DataFrameOps[DataFrame operations]
    end
    
    subgraph "User Interface"
        RenderUI --> StreamlitComponents[Streamlit UI components]
        StreamlitComponents --> RadioButtons[Radio buttons]
        StreamlitComponents --> SelectBoxes[Select boxes]
        StreamlitComponents --> TextInputs[Text inputs]
        StreamlitComponents --> Buttons[Action buttons]
    end
    
    subgraph "Search and Filter"
        SearchLab
        SearchAssay
        SearchBoth
        SearchID
        SearchAll
    end
    
    subgraph "Visualization"
        CallPlot --> Matplotlib[matplotlib backend]
        Matplotlib --> HeatmapGen[2x2 heatmap generation]
        HeatmapGen --> ColorMap[Blue-white-red colormap]
        ColorMap --> Labels[F/A/I/R labels]
    end
    
    style Start fill:#e1f5ff
    style ReadJSON fill:#fff4e1
    style CalcMean fill:#e1ffe1
    style CreateHeatmap fill:#ffe1f5
    style DisplayImage fill:#e1ffe1
    style ErrorDisplay fill:#ffe1e1
    style ErrorNoResults fill:#ffe1e1
```

## Key Components

### Initialization Phase
- **File Validation**: Checks if `fair/fair_results.json` exists before proceeding
- **Data Loading**: Reads and parses JSON into pandas DataFrame
- **Data Validation**: Ensures DataFrame is not empty and properly formatted
- **List Extraction**: Extracts unique lab names and assay types for UI dropdowns

### User Interface
- **Search Type Selection**: Radio buttons for 5 search modes:
  - Lab (single selectbox)
  - Assay type (single selectbox)
  - Lab and Assay type (two selectboxes)
  - Hubmap id (text input)
  - All datasets (no input)
- **Dynamic UI**: UI components change based on selected search type
- **Status Messages**: Real-time status updates during processing

### Search and Filtering
- **search_by_lab()**: Filters DataFrame where `group_name == selected_lab`
- **search_by_assay()**: Filters DataFrame where `dataset_type == selected_assay`
- **search_by_lab_assay()**: Filters by both criteria (AND condition)
- **search_by_id()**: Filters DataFrame where `hubmap_id == entered_id`
- **search_all_id()**: Returns all datasets without filtering
- **find_fair_results()**: Extracts FAIR score arrays from filtered DataFrame

### Aggregation
- **mean_fair_results()**: Calculates mean scores across all filtered results
  - Separates Findable, Accessible, Interoperable, Reproducible scores
  - Calculates mean for each dimension
  - Returns array: `[mean_F, mean_A, mean_I, mean_R]`

### Visualization
- **create_heatmap_for()**: Creates and displays FAIR heatmap
  - Displays individual scores as markdown list
  - Reshapes scores to 2x2 array: `[[F, A], [I, R]]`
  - Calls `fairhelp.create_fair_plot()` to generate PNG
  - Displays image in Streamlit with caption
  - Shows search label (lab name, assay type, etc.)

## User Experience Flow
1. **App Launch**: User opens Streamlit app
2. **Data Load**: App loads precomputed FAIR results (fast, local file)
3. **Selection**: User chooses search type and selects filters
4. **Calculation**: User clicks "Calculate FAIR scores" button
5. **Processing**: App filters data, calculates means, generates visualization
6. **Display**: Results shown with scores and heatmap
7. **Iteration**: User can change filters and recalculate

## Performance Characteristics
- **Fast Loading**: Precomputed data loads instantly (no API calls)
- **Real-time Filtering**: DataFrame filtering is immediate
- **Efficient Aggregation**: Mean calculation is O(n) where n = filtered results
- **Cached Visualization**: Heatmap generation is fast (matplotlib)
