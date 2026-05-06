# Phase II: Creating Multi-Version Evaluation

## Description
Evaluation phase for identifying metadata availability across different versions of the same assay type.

## Phase II Workflow

```mermaid
flowchart TD
    Start([Phase II: Multi-Version Evaluation]) --> P2Focus[Focus: What metadata is available<br/>for the same assay type across<br/>all different versions to that assay type]
    
    P2Focus --> P2Branches[Branches]
    
    P2Branches --> P2AssayTypes[Assay Types]
    P2Branches --> P2Version1[Version 1]
    P2Branches --> P2Version2[Version 2]
    P2Branches --> P2Version3[Version 3]
    
    P2AssayTypes --> P2Compare[Compare data available<br/>across all versions<br/>for each assay type]
    P2Version1 --> P2Compare
    P2Version2 --> P2Compare
    P2Version3 --> P2Compare
    
    P2Compare --> P2Result[Unique elements<br/>across all datasets]
    P2Result --> End([Phase II Complete])
    
    style Start fill:#e1f5ff
    style End fill:#e1ffe1
    style P2Focus fill:#fff4e1
    style P2Compare fill:#ffe1f5
    style P2Result fill:#e1ffe1
```

## Phase II Components

**Focus**: Identify what metadata is available for the same assay type across all different versions of that assay type.

**Branches**:
- Assay Types
- Version 1
- Version 2
- Version 3

**Process**: Compare data available across all versions for each assay type.

**Output**: Unique elements across all datasets.
