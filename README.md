# Diting Benchmark

At this stage, we will open-source our data and testing code, and later we will open-source our complete data construction code.

## DataSet

All of the current data is available in this GitHub repository and can be found under the `\data` folder.

You can also download our dataset from [Hugging Face](https://huggingface.co/datasets/FreedomIntelligence/DitingBench).

Meanwhile, to help you further understand our data sources, we have uploaded the code used to process these data in `data_process`.


## Test
You can test your model by modifying the template code (`\test_script\test_your_model.py`) we provided, or you can contact us (contact information will be shared after the review process is complete) and we can perform the testing on your behalf. Alternatively, you can also reach out to us via the issue tracker.

To make rewriting our template easier, you can refer to the example we provided. (`\test_script\test_qwen2-audio.py`)
## Metric
We have also made our Metric publicly available in `/metric`. Specifically:

`metric/classifier` is for various classification tasks, the metric calculated is accuracy.

`metric/gpt_judge` is for various classification tasks, the metric calculated is the GPT score.

`metric/knowledge` is for various proper noun transcription tasks, the metric calculated is accuracy.

`metric/wer` is for various transcription tasks, such as ASR (Automatic Speech Recognition), ALR (Automatic Lyrics Recognition), the metric calculated is WER (Word Error Rate).


## Result

| **Level** | **Task**                     | **Human Baseline** | **GPT-4o** | **MuLLaMA** | **GAMA** | **SALMONN** | **Qwen2-Audio** |
|-----------|------------------------------|--------------------|------------|-------------|----------|-------------|-----------------|
| **L1**    | Language Identification       | ✘                  | 88.50%     | 8.48%       | ✘        | 35.17%      | 96.44%          |
|           | Auto-Speech Recognition       | 15.49*         | 10.24*  | ✘           | ✘        | 5.45*    | 4.63*        |
|           | ASR for Legal Terms           | 98.50%             | 26.47%     | ✘           | ✘        | ✘           | 81.04%          |
|           | ASR for Medical Terms         | 97.50%             | 41.87%     | ✘           | ✘        | ✘           | 53.86%          |
|           | Auto-Lyrics Transcription     | 26.88*          | ✘          | ✘           | ✘        | 77.12*   | 32.48*       |
|           | - Hallucination Rate          | 3.00%              | ✘          | ✘           | ✘        | 29.26%      | 38.21%          |
| **L2**    | Volume Perception             | 100.00%            | ✘          | 50.00%      | 11.98%   | 53.22%      | 48.96%          |
|           | Pitch Perception              | 96.25%             | 29.33%     | 33.78%      | 41.50%   | 50.00%      | 50.00%          |
|           | Binaural Effect Perception    | 100.00%            | 41.38%     | ✘           | ✘        | 49.88%      | ✘               |
|           | Loudness Assessment           | 85.63%             | ✘          | 49.77%      | ✘        | ✘           | 50.13%          |
|           | Speech Rate Assessment        | 76.25%             | ✘          | 50.00%      | ✘        | ✘           | 44.93%          |
|           | Speech Pause Detection        | 91.88%             | ✘          | 50.00%      | 49.97%   | ✘           | 51.70%          |
| **L3**    | Ambient Noise Detection       | 91.88%             | 45.27%     | 50.00%      | 60.17%   | 49.88%      | 50.00%          |
|           | Acoustic Scene Classification | 90.28%             | 16.36%     | 5.07%       | 12.05%   | 20.74%      | 27.67%          |
|           | Speaker’s Age Prediction      | 52.59%             | 13.43%     | 33.60%      | ✘        | 36.87%      | 38.55%          |
|           | Speaker’s Gender Recognition  | 97.50%             | ✘          | 50.00%      | ✘        | 48.12%      | 79.60%          |
|           | Speech Emotion Recognition    | 50.71%             | 16.77%     | 9.20%       | 3.68%    | 10.93%      | 79.51%          |
|           | Cappella Emotion Recognition  | 62.25%             | 21.50%     | 12.42%      | 7.08%    | 14.62%      | 62.38%          |
|           | Emotion Intensity Perception  | 97.50%             | 72.67%     | 50.00%      | 50.00%   | 49.29%      | 50.00%          |
|           | Emotion Translation | 3.68               | 0.32       | ✘           | ✘        | 0.27        | 0.31            |
|           | Singing Detection             | 99.38%             | 53.11%     | 50.00%      | 64.82%   | 56.47%      | 50.22%          |
| **L4**    | COVID-19 Risk Detection       | 60.63%             | ✘          | ✘           | ✘        | 50.00%      | 14.17%          |
|           | Cough Type Classification     | 52.50%             | 40.33%     | 50.16%      | 44.17%   | 49.17%      | 43.39%          |
|           | Cough Origin Diagnosis        | 32.19%             | ✘          | ✘           | ✘        | 4.01%       | 25.65%          |
|           | Cough Severity Assessment     | 45.42%             | 24.12%     | 30.85%      | 28.50%   | 38.24%      | 33.86%          |
|           | Lung Risk Screening           | 49.38%             | ✘          | 47.62%      | ✘        | ✘           | 50.16%          |
| **L5**    | Spoken English Coach| 1.39               | 0.15       | 1.29        | 0.44     | 0.48        | 0.54            |
|           | Voice Detective    | 1.20               | ✘          | 0.84        | 0.83     | 0.86        | 1.24            |

**Note**:
- "`✘`" indicates that the model fails to follow the instruction.
- "`*`" denotes that the metric is Word Error Rate (WER) and similar metrics, for which lower values indicate better performance.

