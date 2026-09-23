# Issues observed in the initial descriptive scoring (NOT fixed - preserved for audit)

Scoring used the repository's frozen parser (PARSER_VERSION 1.0.0) and MetricPolicy 1.0.0 unchanged.

1. Phi-4 / GoEmotions / one-shot-cot / run5: 271 of 622 attributable records invalid
   (229 fail_unparseable, 32 fail_truncated) vs 49-66 in runs 1-4. Not an infrastructure
   window: all served by DeepInfra, normal latency, spread across every decile of the run.
   Most run5 fail_unparseable raws are an empty JSON object "{}" instead of {"emotions": []};
   197 of those 229 samples were ok_empty_list (non_distress) in run4. accuracy_effective
   0.4486 for that run; conditional macro-F1 RISES to 0.6231 (selection effect).
2. GoEmotions empty-object "{}" responses are scored MODEL_BEHAVIOUR/unparseable by the
   frozen parser: Phi-4 314, Mistral 22, Gemma 6 across the grid.
3. Dreaddit "unparseable" records frequently contain a human-readable risk_level inside
   malformed JSON: Qwen 280 (moderate 220 / low 45 / urgent 15; 269 of 280 in zero-shot-cot),
   Llama 127 of 166, Phi-4 ~20 of 151. Frozen parser rejects them by design.
4. Refusals: Phi-4 Dreaddit ~98, Llama Dreaddit ~33, Llama/Phi/Mistral GoEmotions some
   "I can't assist" / "Please provide the text" responses.
5. Out-of-vocabulary GoEmotions predictions (outside ANXIOSENSE_TO_EVAL_CLASS): Llama 418
   (joy, excitement, happiness, love, nostalgia, ...), Phi-4 314 (happiness, panic, ...),
   Mistral 21, Qwen 10, Gemma 0.
6. Qwen outputs are near-deterministic across the 5 runs (emotion-agent raw byte-identical
   for 581/596/610 of 623 samples in ZS/ZS-CoT/1S-CoT); GoEmotions 1S-CoT metrics identical
   in all five runs (sd 0.0000). Each run was a genuine separate call (623 distinct Mastra
   run ids per run, distinct time windows) - not caching. Run-to-run sd understates
   sampling uncertainty for Qwen.
7. macro_f1 and accuracy_conditional are computed over VALID predictions only; invalid
   predictions do not count as wrong. accuracy_effective counts them in the denominator.
   These diverge where invalid rates are high (Qwen Dreaddit ZS-CoT, Phi-4 GoEmotions).
8. GoEmotions majority baseline 0.781701 (non_distress). Several cells are below it on
   accuracy; macro-F1 includes the 'anxiety' class with support 6 per cell.
9. GoEmotions ok_empty_list (valid empty emotions list -> non_distress, per DATA_PREPROCESSING
   Step 3) dominates valid predictions for every model (e.g. Gemma ~550/622 per run).
