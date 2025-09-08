# Real-Time Story Generation via LLMs & Prompt Engineering

## Project Overview
This project implements a real-time story generation system using **GPT-2**, **prompt engineering**, and **MLOps practices**.  
Users can enter a short "story seed" and receive interactive, evolving narratives in real-time.

## Features
- Real-time story generation via **Streamlit** frontend + **FastAPI** backend  
- Fine-tuned **GPT-2** model on a custom fairytale dataset  
- **Prompt engineering** for controlling genre, POV, and style  
- **Dockerized** deployment with CI/CD integration  
- Evaluation with **Perplexity, BLEU, ROUGE**, and human feedback  

## Tech Stack
- **Frontend:** Streamlit  
- **Backend:** FastAPI  
- **Model:** GPT-2 (fine-tuned on fairy tales)  
- **Deployment:** Docker, GitHub Actions  
- **Evaluation:** Hugging Face `evaluate`

## Methodology 
1. Data Preprocessing
   - File Handling and Reading
   - Whitespace cleanup
   - Title and Metadata Removal
   - Normalization of Punctuation and Special Characters
   - Concatenation of Story Text
   - Story Delimiter Addition
   - Dataset Saving
2. Model Selection
   - GPT-2 (fine-tuned on fairy tales): Local lightweight experiments
3. Prompt Engineering
    - Instruction: You are an award-winning storyteller.
    - Style: classic fairytale. POV: third-person. Length: short. Genre: fantasy. Constraints: avoid explicit content.
    - Story seed: A lighthouse keeper who hears mysterious music from the sea...

## Implementation

- Backend (FastAPI): API endpoint /generate, builds enriched prompt, calls model, streams results.
- Frontend (Streamlit): Web UI for entering seeds, selecting controls, and displaying real-time story output.
- MLOps: Dockerized deployment, .env configs, GitHub Actions for linting, testing, container builds.

<p align="center">
  <img width="360" height="472" alt="System Architecture" src="https://github.com/user-attachments/assets/d93e40f4-32c3-4ed8-b2a4-7ebb6cfb1689" />
  <br/>
  <em>Figure 1: Implementation View of the System</em>
</p>

## System Architecture

### Workflow :
1. User inputs → Streamlit frontend.
2. FastAPI backend constructs final prompt.
3. Hugging Face model (local GPT-2) generates text.
4. Output streamed back to frontend.

<p align="center">
   <img width="765" height="393" alt="image" src="https://github.com/user-attachments/assets/966dcae4-6f12-4fa0-93e7-2168930ab8bc" />
  <br/>
  <em>Figure 2: Sequence Diagram of the Story Generation</em>
</p>

## Model Evaluation

The **GPT-2 model** fine-tuned on the fairy tale dataset was evaluated for both **predictive performance** and **story generation quality**.

### Perplexity
- **Dataset**: First 500 stories from cleaned fairy tale dataset  
- **Batch Size**: 8  
- **Precision**: Mixed (fp16)  
- **Tool**: Hugging Face Trainer  

**Result:**  
- Perplexity = **1.76**  

_Interpretation:_  
Low perplexity indicates the model is highly confident in predicting the next token and has effectively captured fairy-tale style patterns.

<p align="center">
  <img width="1280" height="218" alt="image" src="https://github.com/user-attachments/assets/7a866bd8-6218-4b08-a908-71acd8e7ce99" />
  <br/>
  <em>Figure 3: Perplexity results</em>
</p>

---

### BLEU Score
- **Score**: **0.008** (low, expected for creative tasks)  
- **n-gram precisions**:  
  - 1-gram: 43.8%  
  - 2-gram: 5.8%  
  - 3-gram: 2.1%  
  - 4-gram: 1.9%  
- **Brevity Penalty**: 0.142  
- **Length Ratio**: 0.339  

_Interpretation:_  
BLEU is low since story generation allows multiple valid variations. Model tends to produce shorter but coherent stories.

<p align="center">
  <img width="1280" height="218" alt="image" src="https://github.com/user-attachments/assets/d8749000-20c2-4166-8159-3ae44f3716cc" />
  <br/>
  <em>Figure 4: BLEU and ROUGE scores</em>
</p>

---

### ROUGE Score
- **ROUGE-1**: 0.219 (~22%)  
- **ROUGE-2**: 0.035 (~3%)  
- **ROUGE-L**: 0.090 (~9%)  

_Interpretation:_  
Low overlap is natural in creative storytelling. Despite low n-gram matches, generated stories remain coherent and imaginative.

---

## Overall Analysis
- **Perplexity** → Very low (**good predictive confidence**)  
- **BLEU / ROUGE** → Low (**expected, since multiple creative outputs exist**)  
- **Conclusion** → Fine-tuned GPT-2 effectively adapts to fairy-tale style, producing fluent and imaginative stories even if metrics underrate them.

## Demonstration

<p align="center">
  <img width="787" height="442" alt="image" src="https://github.com/user-attachments/assets/29dc225a-db5e-44fb-9aec-3d7a3fd9e35f" />
  <br/>
  <em>Figure 5: Demonstration of Generated Story Example 1</em>
</p>

<p align="center">
  <img width="776" height="436" alt="image" src="https://github.com/user-attachments/assets/060d91bc-4b57-4ee0-abdc-6bb718fb3a4a" />
  <br/>
  <em>Figure 6: Demonstration of Generated Story Example 2</em>
</p>


  
