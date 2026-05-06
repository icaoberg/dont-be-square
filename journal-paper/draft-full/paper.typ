// dont-be-square: FAIR Score Visualizer for HuBMAP Datasets
// Application Note for Bioinformatics (Oxford) — full draft (two-column, inline figures, no in-PDF references)

#set document(
  title: "dont-be-square: Developing, Assessing, and Visualizing FAIR Metrics for Biomedical Datasets in HuBMAP",
  author: ("Eduardo J. Figueroa Santiago", "Ivan Cao-Berg"),
)

#set page(
  paper: "us-letter",
  margin: (top: 1.9cm, bottom: 1.9cm, left: 1.6cm, right: 1.6cm),
  numbering: "1",
  columns: 2,
)

#set text(font: "New Computer Modern", size: 10pt)
#set par(justify: true, leading: 0.52em)
#set heading(numbering: none)
#set list(indent: 0.45em, body-indent: 0.35em, spacing: 0.42em)

#show heading.where(level: 1): set text(size: 11pt, weight: "bold")
#show heading.where(level: 2): set text(size: 10pt, weight: "bold")

#show figure.caption: set text(size: 8.5pt)

// ─── Title + Abstract (span both columns) ───

#place(top + center, scope: "parent", float: true)[
  #block(width: 100%, above: 0pt, below: 0.65em)[
    #align(center)[
      #text(size: 13pt, weight: "bold")[
        dont-be-square: Developing, Assessing, and Visualizing FAIR Metrics for Biomedical Datasets in HuBMAP
      ]
      #v(0.35em)
      #text(size: 10pt)[
        Eduardo J. Figueroa Santiago#super[1,3], Ivan Cao-Berg#super[1,2]
      ]
      #v(0.2em)
      #text(size: 9pt, style: "italic")[
        #super[1]Carnegie Mellon University, Pittsburgh, PA, USA;
        #super[2]Pittsburgh Supercomputing Center, Pittsburgh, PA, USA;
        #super[3]University of Puerto Rico, Río Piedras Campus, San Juan, PR, USA
      ]
      #v(0.15em)
      #text(size: 9pt)[
        Correspondence: Ivan Cao-Berg (icaoberg\@psc.edu)
      ]
      #v(0.35em)
      #line(length: 55%, stroke: 0.4pt)
      #v(0.25em)
      #block(width: 92%, inset: 0pt)[
        #set text(size: 9pt)
        #set par(justify: true)
        *Abstract* \
        *Motivation:* The Human BioMolecular Atlas Program (HuBMAP) generates large-scale biological datasets, yet no tool quantitatively assesses FAIR (Findable, Accessible, Interoperable, Reusable) compliance at the individual-dataset level using metrics grounded in HuBMAP's metadata model and assay diversity. \
        *Results:* We present _dont-be-square_, an open-source Python/Streamlit application. We derived 33 binary metrics through five phases: synthesizing published FAIR guidance, comparing metadata across assay versions and across assay types, mapping fields to FAIR categories, and defining pass/fail rules. Scores are aggregated per category and displayed as a $2 times 2$ heatmap. Batch pre-computation via the HuBMAP Entity API feeds a JSON archive; an interactive explorer offers five filter views (TMC, assay type, combined, HuBMAP ID, all datasets). \
        *Availability:* https://github.com/ejfigueroa/dont-be-square. Full citations: supplementary `references-list.md`.
      ]
      #v(0.15em)
      #line(length: 55%, stroke: 0.4pt)
    ]
  ]
]

// ─── Body (two columns) ───

= Introduction

Biomedical repositories hold vast imaging, sequencing, and spatial data. Ensuring assets are findable, accessible, interoperable, and reusable (FAIR) is central to reproducibility (Wilkinson et al., 2016). The principles are high level and do not prescribe a fixed metric set (Wilkinson et al., 2018); each community must operationalize them against its schemas and APIs (Krans et al., 2022). For HuBMAP (HuBMAP Consortium, 2019), heterogeneous assay types, evolving metadata, and multiple stakeholders---generators, curators, users, administrators---require interpretable quality signals.

The HuBMAP Data Portal aggregates datasets from 22 tissue mapping centers (TMCs) (Turner et al., 2025). Generic FAIR checklists cannot capture which fields matter per assay, how version changes affect comparability, or what "good" means for HuBMAP. We needed a *HuBMAP-grounded baseline*: an inventory of metadata elements classified as universally required, conditionally required, or optional---before mapping to FAIR categories and binary metrics.

We present _dont-be-square_, an open-source application that closes this gap. The pipeline is: (1) literature and community guidance to structure the work (De Visser et al., 2023; Garcia et al., 2020); (2) compare metadata *within* each assay type across versions, then *across* assay types; (3) map elements to Findable, Accessible, Interoperable, or Reproducible and define rules; (4) fetch metadata via the Entity API, score with four modules, archive JSON; (5) visualize in a Streamlit dashboard (live and batch). Figure 1 summarizes the system; Methods follow this sequence.

#figure(
  scope: "parent",
  placement: auto,
  image("../diagrams/rendered/fig-system-overview-architecture.png", width: 32%),
  caption: [
    End-to-end architecture. Batch FAIR assessment, JSON archival, and interactive exploration; live scoring uses the Entity API for a single dataset ID.
  ],
) <fig-overview>

= Methods

== Phase I: Literature review and framing

We reviewed FAIR frameworks, assessment discussions, and training materials (De Visser et al., 2023; Garcia et al., 2020) for a reusable structure: clear checks, separation across pillars, traceability from principle to test. General FAIR guidance (Wilkinson et al., 2016; Wilkinson et al., 2018), assessment tools (Krans et al., 2022), and adjacent metric toolkits (Garg et al., 2020; Bird et al., 2020; Johnson and Brun, 2022) informed how to operationalize abstract ideas into auditable checks.

== Phase II: Intra-assay, cross-version comparison

HuBMAP exposes many assay types; several have multiple schema versions. For each assay type we compared metadata across versions to find *version-stable* fields versus those introduced, renamed, or deprecated. We avoid scoring fields that are artifacts of one revision and build a per-assay-type profile before merging modalities.

== Phase III: Cross-assay comparison and requirement classes

We compared across assay types to see which elements appear portal-wide, which are shared by subsets, and which are assay-specific. Each element was tagged:

- *Always required* (e.g., UUID, title, group name where in scope).
- *Conditionally required* when a modality applies (e.g., antibody fields, sequence declarations).
- *Optional:* desirable but not enforced.

This *baseline* is what HuBMAP metadata can be asked to satisfy before FAIR labeling.

== Phase IV: Mapping elements to FAIR categories

We assigned each consolidated element to one FAIR pillar. Figure 2 shows Phase IV: concepts map to Findable, Accessible, Interoperable, or Reproducible by primary function (discovery, access, interoperability, interpret/repeat). Ambiguous elements get a single primary category for independent, auditable scoring.

#figure(
  placement: none,
  image("../diagrams/rendered/fig-phase4-fair-category-mapping.png", width: 100%),
  caption: [
    Phase IV: mapping baseline elements to FAIR pillars.
  ],
) <fig-phase4>

== Phase V: Binary scoring criteria

Each retained element has a binary check (0/1) with explicit rules. Totals: *Findable* (8), *Accessible* (7), *Interoperable* (7), *Reproducible* (11). Category score is the mean in $[0, 1]$; presentation is a $2 times 2$ heatmap (blue--white--red per category).

- *Findable:* UUID, title, publication status, entity type, clean metadata, UniProt/ORCID checks.
- *Accessible:* DOI resolution, group IDs, registered and protocol DOIs.
- *Interoperable:* sequences, controlled assay type, lineage/version.
- *Reproducible:* retrieval consistency, x/y/z resolution, dataset type, analyte class, instruments/kits.

== Implementation

Python/Streamlit; HuBMAP SDK and Entity API. Four modules (`findable.py`, `accessible.py`, `interoperable.py`, `reproducible.py`) score independently; shared utilities handle API calls and normalization.

== Operation modes and pre-computation

*Live mode:* one dataset ID, real-time scores and heatmap. *Batch mode:* pre-compute across 22 TMCs, JSON archive, explorer with five filters. Figure 3 shows batch flow: Entity API #sym.arrow parallel FAIR evaluation #sym.arrow aggregation #sym.arrow JSON.

#figure(
  placement: none,
  image("../diagrams/rendered/fig-precomputation-pipeline.png", width: 100%),
  caption: [
    Pre-computation: Entity API ingestion, parallel scoring per FAIR pillar, aggregation, JSON for the explorer.
  ],
) <fig-pipeline>

= Results

The dashboard evaluates compliance across all 22 TMCs; pre-computed JSON avoids repeated API calls for bulk views. Figure 4 is the *All datasets* view: rows are datasets; columns are Findable, Accessible, Interoperable, Reproducible; color encodes relative compliance (blue--white--red). Users scan cohort patterns, then drill into binary checks. Filter modes: TMC, assay type, combined, HuBMAP ID, all datasets.

#figure(
  placement: none,
  image("../supplementary/screenshots/screenshot-all-datasets-view.png", width: 100%),
  caption: [
    *All datasets* view: tabular heatmap of aggregate scores; other filters use the same layout.
  ],
) <fig-app>

= Discussion

_dont-be-square_ makes FAIR compliance *measurable* against HuBMAP's metadata contracts. The contribution is the phased methodology---no static FAIR metric list exists; we built a baseline from versions and assays, then scored. Binary checks are transparent for administrators and curators. Conditional fields may default to pass when absent for an assay type, which can inflate sparse records; metrics reflect our interpretation---other consortia need their own baselines.

= Future work and vision

*Infrastructure and review.* Scheduled re-computation as metadata evolve, and Croissant metadata export for datasets that meet agreed FAIR thresholds.

*MCP and AI consumers.* Expose assessments via Model Context Protocol (MCP) servers so different AI systems can consume FAIR scores alongside HuBMAP entities---supporting search and retrieval over clean, structured, FAIR-aligned data for research.

*Human--AI validation.* AI-assisted checks can flag anomalies and suggest fixes; human curators approve changes and adapt rules, simplifying stewardship while preserving accountability.

*Automating the methodology.* Phases I--V are explicit: a template for semi-automated metric discovery and dashboard-style monitoring for HuBMAP and, with domain adaptation, other repositories.

*Generalizable playbook.* Derive a baseline from portal schemas, map to FAIR, quantify checks, ship a monitoring UI---so definitions of *what* we measure and *how* we evaluate can be mirrored by models with human validation.

= Acknowledgments

We acknowledge Carnegie Mellon University and the Pittsburgh Supercomputing Center for the Summer Internship Program.

*Funding:* Pittsburgh Supercomputing Center at Carnegie Mellon University.

*Software availability:* https://github.com/ejfigueroa/dont-be-square. Supplementary materials include diagrams, screenshots, source code copies, and `references-list.md`.
