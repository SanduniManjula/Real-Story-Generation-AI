# Real-time Story Generation via LLMs and Prompt Engineering

## 1. Problem & Scope

- Real-time story generation for media & entertainment (text-to-story).
- Why real-time? Live authoring, streaming narration, interactive fiction.

## 2. Related Work

- LLM storytelling, controllable generation, prompt programming.

## 3. Methodology

- Model: gpt2-medium (hosted).
- Prompt-engineering: system/style/pov/genre/constraints.
- Safety & content policy.

## 4. System Architecture

- Streamlit UI → FastAPI → HF Client (Inference API / Endpoint).
- Optional SSE streaming with TGI endpoints.
- Dockerized deployment.

## 5. Experiments

- Prompt ablations (style, pov, temperature).
- Few-shot vs zero-shot.
- Latency vs quality.

## 6. Evaluation

- Distinct-n, repetition rate, readability.
- Human eval rubric (coherence, creativity, fluency).

## 7. Results

- Tables/figures summarizing metrics & qualitative samples.

## 8. MLOps

- CI/CD, containerization, environment config, secrets.
- Monitoring: latency, error rate, length.

## 9. Limitations & Ethics

- Hallucinations, bias, style copying, content filtering.

## 10. Conclusion & Future Work

- Branching interactive stories, multimodal narration, user preference conditioning.
