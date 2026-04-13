import time
import re
import numpy as np
import google.generativeai as genai
from .config import GEMINI_API_KEY, EMBEDDING_MODEL, GENERATION_MODEL

# Configure GenAI client
genai.configure(api_key=GEMINI_API_KEY)
gen_model = genai.GenerativeModel(GENERATION_MODEL)

LABEL_PROMPT_TEMPLATE = ("You are a sentiment analysis expert. For EACH tweet below, output ONLY ONE label:\n"
                         "Positive | Neutral | Negative\n\n"
                         "Rules:\n- One label per line, same order as input.\n- No explanations, no numbering, no extra text.\n\n"
                         "Tweets:\n{tweets}")


def label_batch(texts, batch_size=10, timeout=120):
    labels_out = []
    for start in range(0, len(texts), batch_size):
        batch = texts[start:start+batch_size]
        numbered = "\n".join(f"{i+1}. {t}" for i, t in enumerate(batch))
        prompt = LABEL_PROMPT_TEMPLATE.format(tweets=numbered)
        for attempt in range(3):
            try:
                resp = gen_model.generate_content(prompt, request_options={"timeout": timeout})
                lines = [l.strip() for l in resp.text.strip().splitlines() if l.strip()]
                parsed = []
                for line in lines:
                    clean = re.sub(r'^[\d\.\)\-\s]+', '', line)
                    if 'positive' in clean.lower():
                        parsed.append('Positive')
                    elif 'negative' in clean.lower():
                        parsed.append('Negative')
                    else:
                        parsed.append('Neutral')
                if len(parsed) < len(batch):
                    parsed += ['Neutral'] * (len(batch) - len(parsed))
                labels_out.extend(parsed[:len(batch)])
                break
            except Exception:
                time.sleep(15)
                if attempt == 2:
                    labels_out.extend(['Neutral'] * len(batch))
    return labels_out


def embed_texts(texts, model=EMBEDDING_MODEL):
    try:
        res = genai.embed_content(model=model, content=texts, task_type="classification")
        return [e for e in res['embedding']]
    except Exception:
        # Fallback: zero vectors
        return [[0.0]*768 for _ in texts]
