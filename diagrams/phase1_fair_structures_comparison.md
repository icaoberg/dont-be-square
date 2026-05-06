# Phase I: FAIR Structures Different Guidelines

## Description
Comparison phase for evaluating and consolidating all existing FAIR guidelines, frameworks, workflows, and toolkits to create a unified structure.

## Phase I Workflow

```mermaid
flowchart TD
    Start([Phase I: FAIR Structures Comparison]) --> P1Focus[Focus: Comparing and creating final file<br/>with end results - compare all and store similarities]
    
    P1Focus --> P1Branches[Branches - Different Files]
    
    P1Branches --> P1Framework[Frameworks]
    P1Branches --> P1Guidelines[FAIR Guidelines]
    P1Branches --> P1Workflows[Workflows]
    P1Branches --> P1Toolkits[Toolkits]
    P1Branches --> P1Comparative[Comparative Different Methods/Evaluations]
    P1Branches --> P1Evaluating[Evaluating Tool]
    
    P1Framework --> P1Compare[Comparison Process]
    P1Guidelines --> P1Compare
    P1Workflows --> P1Compare
    P1Toolkits --> P1Compare
    P1Comparative --> P1Compare
    P1Evaluating --> P1Compare
    
    P1Compare --> P1Result[Result File:<br/>All things in common]
    P1Result --> End([Phase I Complete])
    
    style Start fill:#e1f5ff
    style End fill:#e1ffe1
    style P1Focus fill:#fff4e1
    style P1Compare fill:#ffe1f5
    style P1Result fill:#e1ffe1
```

## Phase I Components

**Focus**: Compare all existing FAIR guidelines and create a final file storing all similarities and common elements.

**Branches** (Different Files):
- Frameworks
- FAIR Guidelines
- Workflows
- Toolkits
- Comparative Different Methods/Evaluations
- Evaluating Tool

**Output**: Result file containing all common elements identified across all sources.
