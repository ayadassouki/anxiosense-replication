| Model | Prompt Strategy | Conditional Accuracy (mean ± SD) | Effective Accuracy (mean ± SD) | Macro-Precision (mean ± SD) | Macro-Recall (mean ± SD) | Macro-F1 (mean ± SD) | Invalid Outputs (Σ 5 runs) | Invalid Output Rate (mean ± SD) | Total System Response Time (s, mean ± SD) |
|---|---|---|---|---|---|---|---|---|---|
| Gemma 4 31B | zero-shot | **0.8196 ± 0.0038** | **0.8196 ± 0.0038** | 0.7110 ± 0.0147 | 0.5515 ± 0.0036 | 0.5932 ± 0.0071 | **0** | 0.0000 ± 0.0000 | 11.54 ± 1.38 |
| Gemma 4 31B | zero-shot-CoT | 0.8174 ± 0.0037 | 0.8174 ± 0.0037 | 0.7090 ± 0.0112 | 0.5432 ± 0.0034 | 0.5832 ± 0.0082 | 0 | 0.0000 ± 0.0000 | 14.17 ± 3.54 |
| Gemma 4 31B | one-shot-CoT | 0.8150 ± 0.0041 | 0.8132 ± 0.0029 | 0.6947 ± 0.0100 | 0.5514 ± 0.0021 | 0.5852 ± 0.0055 | 7 | 0.0023 ± 0.0027 | 10.09 ± 2.75 |
| Llama 4 Scout | zero-shot | 0.7267 ± 0.0071 | 0.7003 ± 0.0084 | 0.4968 ± 0.0170 | 0.6316 ± 0.0144 | 0.5202 ± 0.0175 | 113 | 0.0363 ± 0.0035 | 10.78 ± 1.26 |
| Llama 4 Scout | zero-shot-CoT | 0.7278 ± 0.0103 | 0.6826 ± 0.0092 | 0.5169 ± 0.0126 | 0.6192 ± 0.0267 | 0.5296 ± 0.0134 | 193 | 0.0621 ± 0.0018 | 11.02 ± 2.20 |
| Llama 4 Scout | one-shot-CoT | 0.7671 ± 0.0084 | 0.7318 ± 0.0092 | 0.5356 ± 0.0117 | 0.6222 ± 0.0097 | 0.5443 ± 0.0126 | 143 | 0.0460 ± 0.0024 | 10.00 ± 1.34 |
| Mistral Small 4 | zero-shot | 0.7698 ± 0.0076 | 0.7656 ± 0.0053 | 0.5418 ± 0.0181 | 0.6229 ± 0.0122 | 0.5615 ± 0.0106 | 17 | 0.0055 ± 0.0033 | 3.98 ± 0.48 |
| Mistral Small 4 | zero-shot-CoT | 0.7457 ± 0.0072 | 0.7412 ± 0.0078 | 0.4995 ± 0.0068 | 0.6328 ± 0.0157 | 0.5357 ± 0.0104 | 19 | 0.0061 ± 0.0013 | 3.43 ± 0.11 |
| Mistral Small 4 | one-shot-CoT | 0.7860 ± 0.0046 | 0.7830 ± 0.0047 | 0.5924 ± 0.0109 | 0.6168 ± 0.0055 | 0.5940 ± 0.0079 | 12 | 0.0039 ± 0.0018 | **3.32 ± 0.16** |
| Phi-4 | zero-shot | 0.7845 ± 0.0076 | 0.7363 ± 0.0164 | 0.5829 ± 0.0255 | 0.5511 ± 0.0129 | 0.5342 ± 0.0161 | 191 | 0.0614 ± 0.0148 | 13.07 ± 0.35 |
| Phi-4 | zero-shot-CoT | 0.8094 ± 0.0035 | 0.7617 ± 0.0090 | 0.6355 ± 0.0187 | 0.5767 ± 0.0129 | 0.5634 ± 0.0105 | 183 | 0.0588 ± 0.0140 | 13.09 ± 1.89 |
| Phi-4 | one-shot-CoT | **0.8011 ± 0.0044** | **0.6730 ± 0.1258** | 0.6473 ± 0.0298 | 0.5498 ± 0.0562 | 0.5406 ± 0.0494 | **499** | **0.1605 ± 0.1543** | 10.63 ± 2.23 |
| Qwen3.5 27B | zero-shot | 0.7862 ± 0.0011 | 0.7862 ± 0.0011 | 0.5941 ± 0.0074 | 0.5652 ± 0.0071 | 0.5723 ± 0.0071 | 0 | 0.0000 ± 0.0000 | 7.27 ± 0.56 |
| Qwen3.5 27B | zero-shot-CoT | 0.7897 ± 0.0021 | 0.7897 ± 0.0021 | 0.6074 ± 0.0042 | 0.5661 ± 0.0079 | 0.5793 ± 0.0060 | 0 | 0.0000 ± 0.0000 | 7.32 ± 0.37 |
| Qwen3.5 27B | one-shot-CoT | 0.7726 ± 0.0000 | 0.7701 ± 0.0000 | 0.5590 ± 0.0000 | 0.5854 ± 0.0000 | 0.5673 ± 0.0000 | 10 | 0.0032 ± 0.0000 | 7.32 ± 0.33 |

Key observations. Gemma 4 31B zero-shot achieved the highest effective accuracy (0.8196) with 0 invalid outputs. Phi-4 one-shot-CoT illustrates the importance of accounting for invalid outputs: its conditional accuracy was 0.8011, but effective accuracy fell to 0.6730, alongside 499 invalid outputs and substantial run-to-run variability. Mistral Small 4 one-shot-CoT had the lowest mean response time (3.32 s). These values are descriptive; statistical comparisons are reported separately in the inferential analyses.
