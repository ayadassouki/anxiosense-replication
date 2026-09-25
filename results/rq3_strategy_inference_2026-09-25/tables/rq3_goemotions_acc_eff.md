### Effective accuracy — strategy contrasts, goemotions (n = 622 items)

| Model | Contrast (A vs B) | A mean ± SD | B mean ± SD | Diff (A−B) | 95% CI | p (unadj.) | p (Holm) | Sig. |
|---|---|---|---|---|---|---|---|---|
| Gemma 4 31B | zero-shot vs zero-shot-CoT | 0.8196 ± 0.0038 | 0.8174 ± 0.0037 | +0.0023 | [−0.0045, +0.0100] | 0.6032 | 1.0000 | no |
| Gemma 4 31B | zero-shot vs one-shot-CoT | 0.8196 ± 0.0038 | 0.8132 ± 0.0029 | +0.0064 | [+0.0006, +0.0129] | 0.0478 | 0.8125 | no |
| Gemma 4 31B | zero-shot-CoT vs one-shot-CoT | 0.8174 ± 0.0037 | 0.8132 ± 0.0029 | +0.0042 | [−0.0032, +0.0113] | 0.3070 | 1.0000 | no |
| Llama 4 Scout | zero-shot vs zero-shot-CoT | 0.7003 ± 0.0084 | 0.6826 ± 0.0092 | +0.0177 | [−0.0026, +0.0383] | 0.0867 | 1.0000 | no |
| Llama 4 Scout | zero-shot vs one-shot-CoT | 0.7003 ± 0.0084 | 0.7318 ± 0.0092 | −0.0315 | [−0.0550, −0.0077] | 0.0082 | 0.1886 | no |
| Llama 4 Scout | zero-shot-CoT vs one-shot-CoT | 0.6826 ± 0.0092 | 0.7318 ± 0.0092 | −0.0492 | [−0.0714, −0.0264] | 0.0002 | 0.0054 | **yes** |
| Mistral Small 4 | zero-shot vs zero-shot-CoT | 0.7656 ± 0.0053 | 0.7412 ± 0.0078 | +0.0244 | [+0.0116, +0.0386] | 0.0005 | 0.0125 | **yes** |
| Mistral Small 4 | zero-shot vs one-shot-CoT | 0.7656 ± 0.0053 | 0.7830 ± 0.0047 | −0.0174 | [−0.0322, −0.0022] | 0.0265 | 0.5459 | no |
| Mistral Small 4 | zero-shot-CoT vs one-shot-CoT | 0.7412 ± 0.0078 | 0.7830 ± 0.0047 | −0.0418 | [−0.0598, −0.0244] | 0.0001 | 0.0030 | **yes** |
| Phi-4 | zero-shot vs zero-shot-CoT | 0.7363 ± 0.0164 | 0.7617 ± 0.0090 | −0.0254 | [−0.0383, −0.0125] | 0.0002 | 0.0054 | **yes** |
| Phi-4 | zero-shot vs one-shot-CoT | 0.7363 ± 0.0164 | 0.6730 ± 0.1258 | +0.0633 | [+0.0463, +0.0810] | 0.0001 | 0.0030 | **yes** |
| Phi-4 | zero-shot-CoT vs one-shot-CoT | 0.7617 ± 0.0090 | 0.6730 ± 0.1258 | +0.0887 | [+0.0717, +0.1061] | 0.0001 | 0.0030 | **yes** |
| Qwen3.5 27B | zero-shot vs zero-shot-CoT | 0.7862 ± 0.0011 | 0.7897 ± 0.0021 | −0.0035 | [−0.0119, +0.0048] | 0.4572 | 1.0000 | no |
| Qwen3.5 27B | zero-shot vs one-shot-CoT | 0.7862 ± 0.0011 | 0.7701 ± 0.0000 | +0.0161 | [−0.0013, +0.0344] | 0.0854 | 1.0000 | no |
| Qwen3.5 27B | zero-shot-CoT vs one-shot-CoT | 0.7897 ± 0.0021 | 0.7701 ± 0.0000 | +0.0196 | [+0.0032, +0.0370] | 0.0278 | 0.5459 | no |
