# streamlit_test.py - Diagram

## Description
Advanced Streamlit application with filtering capabilities. Loads pre-computed FAIR results from JSON, allows filtering by Lab, Assay type, Lab+Assay, or HuBMAP ID, and displays aggregated results.

## Flow Diagram

```mermaid
flowchart TD
    Start([App Start]) --> CheckFile[Check fair_results.json exists]
    CheckFile -->|Not found| Error[Display error and stop]
    CheckFile -->|Found| ReadJSON[read_json_fair]
    ReadJSON --> ValidateData[Validate data loaded]
    ValidateData -->|Invalid| Error
    ValidateData -->|Valid| ExtractLists[Extract lab_list and assay_list]
    ExtractLists --> RenderUI[Render Streamlit UI]
    RenderUI --> UserSelect[User selects search type]
    UserSelect --> RadioSelect{Search type?}
    
    RadioSelect -->|Lab| SelectLab[Select lab from dropdown]
    RadioSelect -->|Assay| SelectAssay[Select assay from dropdown]
    RadioSelect -->|Lab+Assay| SelectBoth[Select both lab and assay]
    RadioSelect -->|Hubmap ID| EnterID[Enter hubmap_id]
    RadioSelect -->|All datasets| SelectAll[Select all]
    
    SelectLab --> ButtonClick[Button clicked]
    SelectAssay --> ButtonClick
    SelectBoth --> ButtonClick
    EnterID --> ButtonClick
    SelectAll --> ButtonClick
    
    ButtonClick --> RouteSearch{Route to search function}
    RouteSearch -->|Lab| SearchLab[search_by_lab]
    RouteSearch -->|Assay| SearchAssay[search_by_assay]
    RouteSearch -->|Lab+Assay| SearchBoth[search_by_lab_assay]
    RouteSearch -->|ID| SearchID[search_by_id]
    RouteSearch -->|All| SearchAll[search_all_id]
    
    SearchLab --> CalcMean[mean_fair_results]
    SearchAssay --> CalcMean
    SearchBoth --> CalcMean
    SearchID --> CalcMean
    SearchAll --> CalcMean
    
    CalcMean --> CreateHeatmap[create_heatmap_for]
    CreateHeatmap --> DisplayScores[Display scores]
    CreateHeatmap --> DisplayPlot[Display heatmap]
    DisplayPlot --> Wait[Wait for next action]
    Wait --> UserSelect
    
    subgraph "Data Loading"
        ReadJSON --> ParseJSON[Parse JSON to DataFrame]
        ParseJSON --> ExtractLists
    end
    
    subgraph "Search Functions"
        SearchLab
        SearchAssay
        SearchBoth
        SearchID
        SearchAll
    end
    
    style Start fill:#e1f5ff
    style ReadJSON fill:#fff4e1
    style CalcMean fill:#e1ffe1
    style CreateHeatmap fill:#ffe1f5
```

## Key Components

- **Data loading**: Reads and validates fair_results.json file at startup
- **Filter extraction**: Extracts unique lab names and assay types for dropdown menus
- **Search routing**: Routes user selection to appropriate search function
- **Aggregation**: Calculates mean FAIR scores for filtered results
- **Visualization**: Creates and displays heatmap with aggregated scores
- **Error handling**: Validates file existence and data integrity before processing
