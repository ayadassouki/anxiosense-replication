# AnxioSense — Experimental Replication Package

This repository contains the experimental results, statistical analyses, validation artifacts, and reproducibility materials for the AnxioSense evaluation study.

AnxioSense is a multi-agent LLM-based system with retrieval-augmented generation (RAG) designed to support early anxiety-related screening in young adults.

## Experimental Evaluation

The evaluation compares five open-weight large language models:

- Gemma 4 31B IT
- Llama 4 Scout
- Mistral Small 4
- Phi-4
- Qwen 3.5 27B

Three prompting strategies were evaluated:

- Zero-shot
- Zero-shot Chain-of-Thought
- One-shot Chain-of-Thought

Experiments were conducted using two datasets:

- **Dreaddit** — binary distress classification
- **GoEmotions subset** — five-class emotion classification

Each model × prompting-strategy configuration was executed five times.

Classification performance was evaluated using accuracy and macro-averaged precision, recall, and F1. Total system response time was also recorded.

Results are reported as mean ± standard deviation across the five experimental runs where applicable.

---

## Research Questions

### RQ1 — Model Performance

**How does classification performance differ across the evaluated LLMs?**

RQ1 compares the classification performance of the five evaluated models separately for Dreaddit and GoEmotions.

The analysis considers effective accuracy and macro-F1 as primary performance measures, with additional descriptive classification metrics reported in the unified results tables.

Model comparisons and corresponding statistical analyses are available in:

`results/final_rq_results_2026-09-25/RQ1_MODEL_COMPARISON.md`

---

### RQ2 — Performance Relative to Baseline

**How do the evaluated LLM configurations perform relative to dataset baselines?**

RQ2 evaluates whether model configurations perform differently from predefined baseline classifiers.

Baseline comparisons and the corresponding statistical analyses are available in:

`results/final_rq_results_2026-09-25/RQ2_BENCHMARK_PERFORMANCE.md`

---

### RQ3 — Prompting Strategy

**How does prompting strategy affect classification performance?**

RQ3 compares:

- Zero-shot
- Zero-shot Chain-of-Thought
- One-shot Chain-of-Thought

within each model and dataset.

The prompting-strategy inferential analysis is reported as **post-hoc/exploratory**.

The analysis uses paired item-level permutation testing for effective accuracy and macro-F1, item-cluster bootstrap confidence intervals, and Holm correction for multiple comparisons. McNemar testing on majority-vote correctness is included as a secondary accuracy analysis.

The complete RQ3 statistical analysis is available in:

`results/rq3_strategy_inference_2026-09-25/RQ3_STRATEGY_INFERENCE_REPORT.md`

The analysis design and statistical decisions are documented in:

`results/rq3_strategy_inference_2026-09-25/RQ3_SAP_ADDENDUM.md`

Latency is reported descriptively and is not used for inferential claims about prompting-strategy efficiency.

---

## Main Descriptive Results Tables

The primary descriptive tables combine classification performance and total system response time so that model quality and efficiency can be examined together.

### Dreaddit

`results/unified_results_tables_2026-09-25/tables/unified_dreaddit.csv`

### GoEmotions

`results/unified_results_tables_2026-09-25/tables/unified_goemotions.csv`

Each table contains 15 configurations:

**5 models × 3 prompting strategies**

The tables report the available configuration-level classification metrics and total system response time using five-run summaries.

Additional per-class precision, recall, and F1 results are provided in:

`results/unified_results_tables_2026-09-25/tables/per_class_supplement.csv`

Metric definitions and provenance are documented in:

`results/unified_results_tables_2026-09-25/METRIC_AUDIT.md`

---

## Invalid-Output Audit

Model outputs that could not be evaluated by the production parsing and scoring pipeline were examined separately.

The audit investigates the frequency and characteristics of invalid outputs while preserving the original experimental results.

Invalid outputs were not repaired and substituted into the original evaluation results.

The complete audit is available in:

`results/invalid_output_audit_2026-09-25/invalid_output_audit_report.md`

Additional audit materials include:

- failure-taxonomy summaries
- configuration-level invalid-output summaries
- recurrence analysis
- validation documentation
- reproducible audit scripts

The invalid-output analysis helps distinguish failures in classification from failures in structured-output generation or serialization.

---

## Repository Structure

```text
anxiosense-replication/
│
└── results/
    │
    ├── unified_results_tables_2026-09-25/
    │   ├── tables/
    │   ├── code/
    │   ├── README.md
    │   └── METRIC_AUDIT.md
    │
    ├── final_rq_results_2026-09-25/
    │   ├── RQ1_MODEL_COMPARISON.md
    │   ├── RQ2_BENCHMARK_PERFORMANCE.md
    │   ├── RQ3_PROMPTING_STRATEGIES.md
    │   ├── LATENCY_ANALYSIS.md
    │   ├── INVALID_OUTPUT_SELECTION_EFFECT.md
    │   ├── FINAL_RESULTS_SUMMARY.md
    │   ├── VALIDATION.md
    │   ├── tables/
    │   └── code/
    │
    ├── rq3_strategy_inference_2026-09-25/
    │   ├── RQ3_STRATEGY_INFERENCE_REPORT.md
    │   ├── RQ3_SAP_ADDENDUM.md
    │   ├── PREREGISTRATION_FREEZE.json
    │   ├── VALIDATION.md
    │   ├── tables/
    │   ├── replicates/
    │   └── code/
    │
    └── invalid_output_audit_2026-09-25/
        ├── invalid_output_audit_report.md
        ├── VALIDATION.md
        ├── failure_taxonomy_summary.csv
        ├── cell_level_invalid_vs_quality.csv
        ├── unique_sample_recurrence.csv
        └── code/
```

## Metric Interpretation

### Effective Accuracy

Effective accuracy treats model-attributable invalid outputs as incorrect rather than silently removing them from the denominator. This makes failures to produce evaluable output part of the measured system performance.

### Conditional Accuracy

Conditional accuracy measures accuracy only among outputs that could be evaluated. Because excluding invalid outputs can introduce selection effects, conditional accuracy is reported descriptively and is not used as the primary ranking metric.

### Macro-F1

Macro-F1 is the unweighted mean of the per-class F1 scores over the fixed class set. It is reported alongside accuracy because overall accuracy can obscure differences in performance across classes, particularly when class frequencies are imbalanced.

### Precision and Recall

Configuration-level precision and recall are reported as macro-averaged precision and macro-averaged recall. Per-class precision, recall, and F1 are provided separately in the supplementary table.

### Total System Response Time

Total system response time represents client-side end-to-end wall-clock time around the AnxioSense evaluation request. Latency values are summarized across the five experimental runs.

Latency comparisons are descriptive because the experiments were not designed as controlled latency benchmarks. Provider load, execution timing, machine differences, polling behavior, and other infrastructure factors may influence the recorded response times.

---

## Statistical Analysis

The statistical analyses were designed around the paired structure of the experimental data. Depending on the research question, the analysis includes:

- paired item-level permutation tests
- item-cluster bootstrap confidence intervals
- exact McNemar tests
- Holm correction for multiple comparisons

The statistical unit for paired analyses is the dataset item while retaining its repeated experimental runs, rather than treating every repeated execution as an independent observation.

Detailed statistical procedures, assumptions, comparison families, and validation checks are documented within the corresponding result packages.

### Multiple-Comparison Correction

Multiple statistical comparisons increase the probability of obtaining a small p-value by chance. Holm correction is therefore used within predefined comparison families to control the family-wise error rate while avoiding the unnecessary conservatism of applying one correction across unrelated research questions.

Both raw and Holm-adjusted statistical results are preserved in the corresponding analysis artifacts.

### RQ3 Analysis Status

The prompting-strategy inferential analysis was conducted after the original RQ1/RQ2 inferential analysis plan. It is therefore reported as **post-hoc/exploratory** rather than preregistered confirmatory analysis.

Before the RQ3 inferential tests were executed, the analysis procedure, comparison families, input hashes, and analysis code were frozen and recorded. This provides an auditable record of the analysis decisions while preserving the appropriate post-hoc interpretation.

---

## Reproducibility and Validation

The result packages contain supporting reproducibility materials including:

- analysis scripts
- source/provenance records
- validation reports
- SHA-256 checksum manifests
- statistical output tables
- saved statistical replicates where applicable

The analyses were designed as read-only reporting and audit layers over the frozen experimental artifacts. The original experimental outputs were not repaired or modified to improve reported performance.

Package-specific validation information is available in each package's `VALIDATION.md` and `CHECKSUMS.sha256` files.

---

## Important Interpretation Notes

1. Results are reported separately for Dreaddit and GoEmotions. Performance on one dataset should not be assumed to generalize directly to the other.
2. Model performance depends on both the model and prompting strategy. A single universal model ranking is therefore not assumed.
3. Effective accuracy incorporates invalid model outputs into system-level performance.
4. Macro-F1 is reported alongside accuracy to provide information about performance across classes.
5. GoEmotions contains substantial class imbalance, including very small minority-class support, which limits the precision of some macro-F1 comparisons.
6. Latency results are descriptive and should not be interpreted as controlled causal comparisons between models or prompting strategies.
7. The RQ3 prompting-strategy inferential analysis is **post-hoc/exploratory**.
8. Invalid-output behavior is analyzed explicitly rather than silently removing invalid predictions from the evaluation.

---

## AI-Assistance Disclosure

Generative AI tools were used to assist with portions of code development, validation workflows, organization and classification of analysis artifacts, and drafting and editing documentation.

All quantitative findings reported in the replication package were derived from the experimental artifacts and analysis procedures documented in the repository. AI-generated suggestions were not treated as experimental evidence.

---

## Purpose of This Repository

This repository serves as the replication and audit package for the AnxioSense experimental evaluation. Its purpose is to provide the supporting result tables, statistical outputs, analysis code, provenance records, and validation artifacts required to trace and reproduce the reported experimental findings.
