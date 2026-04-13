from dotenv import load_dotenv
import os
from pathlib import Path

load_dotenv()

GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
if not GEMINI_API_KEY:
    raise RuntimeError('GEMINI_API_KEY not set. Copy .env.example to .env and set the key.')

EMBEDDING_MODEL = os.getenv('EMBEDDING_MODEL', 'models/text-embedding-004')
GENERATION_MODEL = os.getenv('GENERATION_MODEL', 'gemini-pro')
DATASET_URL = os.getenv('DATASET_URL', 'https://nkb-backend-ccbp-media-static.s3-ap-south-1.amazonaws.com/ccbp_beta/media/content_loading/uploads/070be49c-5f5d-4030-bedc-53fc7582a602_Tweets_1.csv')
