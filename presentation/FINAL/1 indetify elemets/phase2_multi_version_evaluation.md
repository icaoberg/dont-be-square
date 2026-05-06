flowchart TD
    Start([Phase II: Multi-Version Evaluation])
    
    Start --> P2AssayTypes[Selected Assay Type]

    P2AssayTypes --> P2Version1[Version 1]
    P2AssayTypes --> P2Version2[Version 2]
    P2AssayTypes --> P2Version3[Version 3]
    
    P2Version1 --> P2Compare{Filtering <br> elements <br>}
    P2Version2 --> P2Compare
    P2Version3 --> P2Compare
    
    P2Compare --> P2Result[List of <br>Common elements in metadata <br/> by Assay Type]
    P2Result --> store[(Files for each <br> Assay Type)]
    P2Result --> EvalAssay{More Assay Types?}

    EvalAssay --> |Yes|P2AssayTypes
    EvalAssay --> |No| End
    
    style Start fill:#e1f5ff
    style P2Compare fill:#ffe1f5
    style P2Result fill:#e1ffe1