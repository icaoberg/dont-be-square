// dont-be-square: FAIR Score Visualizer for HuBMAP Datasets
// Application Note — Bioinformatics (Oxford)
// Compact draft: ~2 pages; references only in supplementary/references-list.md

#set document(
  title: "dont-be-square: Developing, Assessing, and Visualizing FAIR Metrics for Biomedical Datasets in HuBMAP",
  author: ("Eduardo J. Figueroa Santiago", "Ivan Cao-Berg"),
)

#set page(
  paper: "us-letter",
  margin: (top: 1.45cm, bottom: 1.45cm, left: 1.25cm, right: 1.25cm),
  numbering: "1",
  columns: 2,
)

#set text(font: "New Computer Modern", size: 8.5pt)
#set par(justify: true, leading: 0.44em)
#set heading(numbering: none)
#set list(indent: 0.4em, body-indent: 0.3em, spacing: 0.36em)

#show heading.where(level: 1): set text(size: 10pt, weight: "bold")
#show heading.where(level: 2): set text(size: 9pt, weight: "bold")
#show figure.caption: set text(size: 7.5pt)

// ─── Title + Abstract (span both columns) ───

#place(top + center, scope: "parent", float: true)[
  #block(width: 100%, above: 0pt, below: 0.55em)[
    #align(center)[
      #text(size: 12.5pt, weight: "bold")[
        dont-be-square: Developing, Assessing, and Visualizing FAIR Metrics for Biomedical Datasets in HuBMAP
      ]
      #v(0.22em)
      #text(size: 9pt)[
        Eduardo J. Figueroa Santiago#super[1,3] and Ivan Cao-Berg#super[1,2,]\*
      ]
      #v(0.1em)
      #text(size: 7.5pt, style: "italic")[
        #super[1]Carnegie Mellon University, Pittsburgh, PA, USA;
        #super[2]Pittsburgh Supercomputing Center, Pittsburgh, PA, USA;
        #super[3]University of Puerto Rico, Río Piedras Campus, San Juan, PR
      ]
      #v(0.08em)
      #text(size: 7.5pt)[
        \*Correspondence: icaoberg\@psc.edu
      ]
      #v(0.18em)
      #line(length: 52%, stroke: 0.4pt)
      #v(0.1em)
      #block(width: 91%, inset: 0pt)[
        #set text(size: 7.5pt)
        #set par(justify: true)
        *Abstract* \
        *Motivation:* HuBMAP generates large-scale biological datasets, yet no tool assesses FAIR compliance at the dataset level with metrics grounded in HuBMAP's metadata model and assay diversity. \
        *Results:* _dont-be-square_ is an open-source Python/Streamlit application. We derived 33 binary metrics in five phases---literature framing; intra-assay version comparison; cross-assay baseline with requirement classes; FAIR category mapping; binary rule definition---then pre-compute scores via the Entity API into JSON and visualize a $2 times 2$ heatmap with five explorer filters (TMC, assay type, combined, HuBMAP ID, all datasets). \
        *Availability:* https://github.com/ejfigueroa/dont-be-square. Citations: supplementary `references-list.md`.
      ]
      #v(0.06em)
      #line(length: 52%, stroke: 0.4pt)
    ]
  ]
]

// ─── Body ───

= Introduction

The FAIR principles---Findable, Accessible, Interoperable, Reusable---maximize reuse of scientific data (Wilkinson et al., 2016). They are intentionally high level and do not prescribe a fixed metric set (Wilkinson et al., 2018); each community must operationalize them against its schemas, APIs, and curation practices (Krans et al., 2022). The Human BioMolecular Atlas Program (HuBMAP) (HuBMAP Consortium, 2019) maps healthy human tissues at single-cell resolution; the Data Portal aggregates datasets from 22 tissue mapping centers (TMCs) and diverse modalities (Turner et al., 2025). Metadata are rich but heterogeneous: assay types evolve across schema versions, and generic FAIR rubrics cannot say which fields are universally required, required only for certain assays, or optional.

We therefore built a *HuBMAP-grounded baseline* before scoring: comparing metadata *within* each assay type across versions, then *across* assay types, then assigning each element to Findable, Accessible, Interoperable, or Reproducible with explicit binary tests.

_dont-be-square_ implements the full pipeline. Published FAIR workflow and training guidance (De Visser et al., 2023; Garcia et al., 2020) informed how we structured traceable checks; the HuBMAP Entity API and SDK supply live and batch metadata. Four independent Python modules implement 33 binary checks; pre-computed JSON powers an interactive Streamlit dashboard so users, uploaders, curators, and administrators can move from cohort views to single-dataset diagnosis.

= Methods

== Metric design (five phases)

*Phase I* reviewed FAIR literature and tool discussions to establish a reusable structure for checks and traceability. *Phase II* compared metadata across versions of each assay type to identify version-stable fields. *Phase III* extended comparison across all assay types, tagging each element as always required, conditionally required, or optional---producing the baseline of what HuBMAP metadata can satisfy. *Phase IV* mapped consolidated elements to Findable, Accessible, Interoperable, or Reproducible. *Phase V* defined binary pass/fail rules; the per-category score is the arithmetic mean of its checks in $[0, 1]$, displayed as a $2 times 2$ heatmap (blue--white--red within each category).

== Implementation and modes

The application is implemented in Python with Streamlit. Metadata are retrieved via the HuBMAP SDK and Entity API. *Findable* (8 checks): UUID, title, publication status, entity type, error-free metadata, antibody validation against UniProt, contributor and contact ORCID. *Accessible* (7): DOI URL resolution, group name and UUID, HuBMAP ID, registered DOI, protocols.io and reagent-prep protocol DOIs. *Interoperable* (7): genetic sequence declarations, assay category and type against controlled vocabularies, contributors path, dataset version, ancestor linkage, antibody version. *Reproducible* (11): metadata retrieval consistency, spatial resolution x/y/z (units and values), dataset type, analyte class, preparation kit, acquisition instrument. *Live mode:* one dataset ID yields real-time scores and a heatmap. *Batch mode:* scores are pre-computed across 22 TMCs, written to JSON, and loaded into an explorer with five filter views (Figure 1).

#figure(
  placement: none,
  image("../diagrams/rendered/fig-precomputation-pipeline.png", width: 100%),
  caption: [
    Batch pre-computation: Entity API #sym.arrow parallel FAIR modules #sym.arrow JSON for the explorer.
  ],
) <fig-system>

= Results

The dashboard evaluates FAIR compliance across all 22 TMCs. Pre-computed JSON enables instant filtering without repeated API calls for bulk views. Figure 2 shows the *All datasets* view: each row is a dataset; columns report aggregate scores for Findable, Accessible, Interoperable, and Reproducible; cell color encodes relative compliance on a blue (low) to white to red (high) scale within each category. Users scan thousands of rows for patterns---for example, a TMC or assay type with weak Accessible scores---before opening a single identifier for the underlying binary checks. The five filter modes (TMC, assay type, TMC+assay combined, HuBMAP ID, all datasets) align with institutional review, modality-specific QA, cross-tabs, single-dataset lookup, and global ranking. Failures are actionable: missing DOIs surface under Accessible; inconsistent assay typing under Interoperable.

#figure(
  placement: none,
  image("../supplementary/screenshots/screenshot-all-datasets-view.png", width: 100%),
  caption: [
    *All datasets* view: tabular heatmap; other filters share the same layout.
  ],
) <fig-explorer>

= Discussion

_dont-be-square_ turns FAIR from a passive checklist into a measurable property tied to HuBMAP's metadata contracts. The scientific contribution is the end-to-end methodology: there is no universal FAIR metric list, so we built a baseline from literature, versions, and cross-assay comparison before scoring. Binary checks pass or fail transparently, which supports administrators and curators. A limitation is that when a field does not apply to an assay type, some checks may default to pass, inflating compliance for sparse records; metrics also reflect our interpretation of HuBMAP and FAIR, and other consortia would repeat the phased process for their schemas.

= Future work

Near-term work includes automated scheduled re-computation as the portal evolves, and Croissant metadata files for datasets that meet agreed FAIR thresholds. We intend to expose assessments via Model Context Protocol (MCP) servers so that different AI systems can query FAIR scores alongside HuBMAP entities---supporting search and retrieval over clean, structured, reviewable data for research workflows. AI-assisted validation can flag anomalies and suggest fixes; human curators remain the authority for approving changes, which simplifies stewardship without removing accountability. Because phases I--V are documented explicitly, the same process can guide semi-automated metric discovery and dashboard-style monitoring not only for HuBMAP updates but, with domain adaptation, for *other* biomedical databases. The long-term vision is a reusable playbook---how to derive a baseline from a portal's schemas, map to FAIR, quantify checks, and ship a monitoring UI---so that clear definitions of *what* we measure and *how* we evaluate it can eventually be mirrored by models while humans validate outcomes. A further step is to generalize the rule set: once metric definitions and evaluation logic are machine-readable, the same pipeline could propose new checks when schemas change, subject to human review, and surface them in dashboards similar to _dont-be-square_, reducing manual rework when new assay types or metadata fields appear.

#v(0.28em)

*Acknowledgments.* Carnegie Mellon University and PSC Summer Internship Program.

*Funding.* Pittsburgh Supercomputing Center at Carnegie Mellon University.

*Software availability.* https://github.com/ejfigueroa/dont-be-square. Supplementary: diagrams, screenshots, source code, `references-list.md`.
