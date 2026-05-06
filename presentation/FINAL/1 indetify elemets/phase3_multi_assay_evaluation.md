flowchart TD
    Start([Phase III: Multi-Assay Evaluation]) --> P3CompareFormats[Common metadata elements by Assay Type]
    
    P3CompareFormats --> P3ATACRNA[ATAC RNA]
    P3CompareFormats --> P3RNASeq[RNA Seq]
    P3CompareFormats --> P3SingleCell[Single Cell]
    P3CompareFormats --> P3BulkRNA[Bulk RNA]
    P3CompareFormats --> P3Other[etc] 
    
    P3ATACRNA --> P3Compare{Compare <br> metadata elements}
    P3RNASeq --> P3Compare
    P3SingleCell --> P3Compare
    P3BulkRNA --> P3Compare
    P3Other --> P3Compare
    
    P3Compare --> P3Result["General <br>metadata elements <br/> (all assay types)"]
    
    style Start fill:#e1f5ff
    style P3Compare fill:#ffe1f5