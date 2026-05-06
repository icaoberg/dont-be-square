# Bullet Points: Writing & Reviewing the Application Note

## Bioinformatics Application Note Constraints

- **Word limit:** ~1,300 words (body text only; abstract, references, and figure legends are separate)
- **Page limit:** 2 printed pages
- **Figures:** Up to 2 figures (can include subfigures/panels)
- **Abstract:** ~150 words, structured or unstructured
- **Structure:** Title, Authors/Affiliations, Abstract, Introduction, Methods (or Implementation), Results, Discussion/Conclusion, References
- **Software availability:** Must state the URL where the software is freely available (GitHub repo link)
- **Submission:** Format-free initial submission accepted; use ScholarOne at http://mc.manuscriptcentral.com/bioinformatics
- **Open Access:** All articles since 2023 are open access; Article Processing Charge (APC) applies
- **License:** Typically CC-BY for open access

## Key Points to Emphasize Per Section

### Abstract
- Problem: No standardized, measurable FAIR metrics for HuBMAP datasets
- Solution: Developed tailored FAIR metrics + interactive Streamlit dashboard
- Impact: Enables multi-stakeholder assessment (users, uploaders, curators, administrators)

### Introduction
- Cite FAIR principles origin (Wilkinson et al. 2016)
- HuBMAP as a large-scale biomedical data consortium (HuBMAP Consortium 2019)
- Gap: existing FAIR frameworks are generic; no project-specific measurable metrics for HuBMAP
- Contribution: first tool to compute and visualize FAIR compliance per-dataset for HuBMAP

### Methods / Implementation
- Five-phase metric design: (1) literature review, (2) version comparison, (3) cross-assay analysis, (4) FAIR categorization, (5) scoring criteria
- Python implementation with Streamlit, HuBMAP SDK, Entity API
- Findable: 8 checks (UUID, title, publication status, contributors with ORCID, contacts with ORCID, antibody UniProt validation, entity type, error-free metadata)
- Accessible: 7 checks (DOI URL accessibility, group name/UUID, HuBMAP ID, registered DOI, protocols.io DOI, reagent prep protocols DOI)
- Interoperable: 7 checks (genetic sequences, assay category/type validation, contributors path, version, direct ancestors, antibody version)
- Reproducible: 11 checks (metadata retrieval consistency, resolution x/y/z unit+value, dataset type, analyte class, preparation kit, acquisition model)
- Scoring: binary (0/1) per check, averaged per FAIR category, displayed as 2x2 heatmap (blue-white-red colormap)
- Two modes: live single-dataset scoring; batch pre-computed explorer with filtering

### Results
- Dashboard supports 5 filter modes: by Lab (TMC), Assay Type, Lab+Assay, HuBMAP ID, All Datasets
- Pre-computed results stored as JSON for fast retrieval
- Covers all 22 TMCs in HuBMAP
- Heatmap visualization provides instant quality assessment

### Discussion / Conclusion
- Transforms FAIR from abstract principles to measurable, actionable metrics
- Multi-stakeholder utility
- Limitations: metrics are binary; some checks default to pass when metadata fields are absent
- Future work: automated scheduled re-computation, Croissant file generation, MCP server for FAIR-passing datasets

## What Reviewers Look For in Application Notes

1. **Novelty:** Does this tool fill a real gap? (Yes -- no existing FAIR dashboard for HuBMAP)
2. **Usability:** Is it easy to use? (Yes -- Streamlit web interface, no installation needed for end users)
3. **Availability:** Is the code freely available with documentation? (Ensure GitHub repo is public with README and license)
4. **Correctness:** Are the methods sound? (Binary scoring is simple but defensible; averaging is standard)
5. **Presentation:** Is the paper clear and well-structured? (Follow the template precisely)
6. **Figures:** Are they informative and publication-quality? (High-res diagrams at 4x scale)

## Pre-Submission Checklist

- [ ] Paper is within ~1,300 words (body)
- [ ] Abstract is ~150 words
- [ ] No more than 2 figures
- [ ] All figures have captions with adequate detail
- [ ] Software availability statement with GitHub URL
- [ ] All references cited in text
- [ ] Author names and affiliations are correct
- [ ] ORCID IDs for all authors
- [ ] Supplementary materials (if any) are referenced
- [ ] Ensure GitHub repo has: README, LICENSE, requirements.txt, clear run instructions
- [ ] Conflict of interest statement
- [ ] Funding acknowledgment (PSC/CMU internship)
