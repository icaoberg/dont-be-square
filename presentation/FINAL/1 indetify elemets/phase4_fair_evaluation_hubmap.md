flowchart TD
    Start([Phase IV: FAIR Evaluation to HuBMAP]) --> |General metadata elements| ExistingFile[Creating metrics]

    ExistingFile --> P4ExistingDOI[Existing DOI]
    ExistingFile --> P4WorkingDOI[Working DOI Link]
    ExistingFile --> P4PatientID[Patient ID]
    ExistingFile --> P4SampleID[Sample ID]
    ExistingFile --> P4Organism[Organism]
    ExistingFile --> P4Other[etc]
    
    P4ExistingDOI --> P4Category{Oganize by<br> FAIR Category}
    P4WorkingDOI --> P4Category
    P4PatientID --> P4Category
    P4SampleID --> P4Category
    P4Organism --> P4Category
    P4Other --> P4Category

    P4Category --> |Fair| f[Fair Elements]
    P4Category --> |Accessable| a[Accessable Elements]
    P4Category --> |Interoperable| i[Interoperable Elements]
    P4Category --> |Reusable| r[Reusable Elements]


    f --> result[Result file]
    a --> result
    i --> result
    r --> result

    style Start fill:#e1f5ff
