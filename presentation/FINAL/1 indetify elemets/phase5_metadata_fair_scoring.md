flowchart TD
    Start([Phase V: Metadata FAIR Scoring]) --> P5Types{Types <br>of<br> Metadata <br>elements}
    
    P5Types --> |Required|P5Required{When is<br> Required?}
        P5Required --> |Always|AR[All datasets <br>used it]
        P5Required --> |Sometimes|OR[Not all<br> datsets use it]

    P5Types --> |Not<br>Required|P5Optional[Optional]
    
    AR --> P5Result[Elements Evaluated]
    OR --> P5Result
    P5Optional --> e[Not used]
        
    style Start fill:#e1f5ff
    style P5Types fill:#ffe1f5
    style P5Result fill:#e1ffe1