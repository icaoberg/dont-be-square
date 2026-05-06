flowchart TD
    Start([Pre-Compute FAIRness Metrics]) --> SearchHuBMAP[Query HuBMAP Portal by internal API]
        
    subgraph "HuBMAP Infrastructure"
        SearchHuBMAP --> |Find<br>Contributors| HuBMAPPortal[HuBMAP Entity API]
        HuBMAPPortal -->  |Datasets by<br> Contributors| RetrieveMetadata[Retrieve Metadata]
        RetrieveMetadata --> ExtractAssayInfo[Extract assay type and identifiers]
    end

    ExtractAssayInfo --> AssessFAIR[Assess FAIR compliance]
    
    AssessFAIR --> EvaluateFindable[Evaluate Findability metrics]
    AssessFAIR --> EvaluateAccessible[Evaluate Accessibility metrics]
    AssessFAIR --> EvaluateInteroperable[Evaluate Interoperability metrics]
    AssessFAIR --> EvaluateReproducible[Evaluate Reproducibility metrics]
        
    subgraph "FAIR Metrics Evaluation"
        EvaluateFindable --> AggregateScores[Aggregate FAIR scores]
    EvaluateAccessible --> AggregateScores
    EvaluateInteroperable --> AggregateScores
    EvaluateReproducible --> AggregateScores
    end

    AggregateScores --> StoreResults[(Store FAIR assessment results)]

    
    style Start fill:#e1f5ff
    style AssessFAIR fill:#fff4e1
    style StoreResults fill:#ffe1f5