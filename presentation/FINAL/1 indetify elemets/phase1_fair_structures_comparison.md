flowchart LR
    Start([Phase I: FAIR Structures Comparison]) --> P1Framework[Frameworks]
    Start --> P1Guidelines[FAIR Guidelines]
    Start --> P1Workflows[Workflows]
    Start --> P1Toolkits[Toolkits]
    Start --> P1Evaluating[Evaluating Tool]

    P1Framework --> P1Compare{Comparing <br>Metadata <br> elements}
    P1Guidelines --> P1Compare
    P1Workflows --> P1Compare
    P1Toolkits --> P1Compare
    P1Evaluating --> P1Compare

    P1Compare --> P1Result[List of <br>metadata elements]
       
    style Start fill:#e1f5ff
    style P1Compare fill:#ffe1f5
    style P1Result fill:#e1ffe1