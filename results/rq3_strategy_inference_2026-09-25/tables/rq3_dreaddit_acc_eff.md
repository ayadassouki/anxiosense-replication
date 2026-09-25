### Effective accuracy — strategy contrasts, dreaddit (n = 699 items)

| Model | Contrast (A vs B) | A mean ± SD | B mean ± SD | Diff (A−B) | 95% CI | p (unadj.) | p (Holm) | Sig. |
|---|---|---|---|---|---|---|---|---|
| Gemma 4 31B | zero-shot vs zero-shot-CoT | 0.6933 ± 0.0040 | 0.6747 ± 0.0008 | +0.0186 | [+0.0094, +0.0280] | 0.0001 | 0.0030 | **yes** |
| Gemma 4 31B | zero-shot vs one-shot-CoT | 0.6933 ± 0.0040 | 0.6755 ± 0.0064 | +0.0177 | [+0.0089, +0.0278] | 0.0005 | 0.0085 | **yes** |
| Gemma 4 31B | zero-shot-CoT vs one-shot-CoT | 0.6747 ± 0.0008 | 0.6755 ± 0.0064 | −0.0009 | [−0.0074, +0.0057] | 0.8651 | 1.0000 | no |
| Llama 4 Scout | zero-shot vs zero-shot-CoT | 0.7296 ± 0.0027 | 0.7330 ± 0.0049 | −0.0034 | [−0.0166, +0.0103] | 0.6537 | 1.0000 | no |
| Llama 4 Scout | zero-shot vs one-shot-CoT | 0.7296 ± 0.0027 | 0.7502 ± 0.0049 | −0.0206 | [−0.0349, −0.0063] | 0.0061 | 0.0976 | no |
| Llama 4 Scout | zero-shot-CoT vs one-shot-CoT | 0.7330 ± 0.0049 | 0.7502 ± 0.0049 | −0.0172 | [−0.0303, −0.0037] | 0.0129 | 0.1806 | no |
| Mistral Small 4 | zero-shot vs zero-shot-CoT | 0.6861 ± 0.0036 | 0.6609 ± 0.0042 | +0.0252 | [+0.0126, +0.0381] | 0.0002 | 0.0042 | **yes** |
| Mistral Small 4 | zero-shot vs one-shot-CoT | 0.6861 ± 0.0036 | 0.6735 ± 0.0053 | +0.0126 | [+0.0011, +0.0243] | 0.0365 | 0.3650 | no |
| Mistral Small 4 | zero-shot-CoT vs one-shot-CoT | 0.6609 ± 0.0042 | 0.6735 ± 0.0053 | −0.0126 | [−0.0237, −0.0014] | 0.0304 | 0.3344 | no |
| Phi-4 | zero-shot vs zero-shot-CoT | 0.7222 ± 0.0164 | 0.7001 ± 0.0022 | +0.0220 | [+0.0029, +0.0409] | 0.0262 | 0.3144 | no |
| Phi-4 | zero-shot vs one-shot-CoT | 0.7222 ± 0.0164 | 0.7299 ± 0.0101 | −0.0077 | [−0.0235, +0.0083] | 0.3629 | 1.0000 | no |
| Phi-4 | zero-shot-CoT vs one-shot-CoT | 0.7001 ± 0.0022 | 0.7299 ± 0.0101 | −0.0298 | [−0.0455, −0.0137] | 0.0004 | 0.0072 | **yes** |
| Qwen3.5 27B | zero-shot vs zero-shot-CoT | 0.6910 ± 0.0014 | 0.6023 ± 0.0049 | +0.0887 | [+0.0655, +0.1122] | 0.0001 | 0.0030 | **yes** |
| Qwen3.5 27B | zero-shot vs one-shot-CoT | 0.6910 ± 0.0014 | 0.6475 ± 0.0016 | +0.0435 | [+0.0249, +0.0627] | 0.0001 | 0.0030 | **yes** |
| Qwen3.5 27B | zero-shot-CoT vs one-shot-CoT | 0.6023 ± 0.0049 | 0.6475 ± 0.0016 | −0.0452 | [−0.0655, −0.0249] | 0.0001 | 0.0030 | **yes** |
