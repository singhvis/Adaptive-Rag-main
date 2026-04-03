"""
LLM initialization using local LLM Studio (OpenAI-compatible API)
"""

import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

# Load environment variables
load_dotenv()

llm = ChatOpenAI(
    model=os.getenv("MODEL_NAME"),                 # google/gemma-3-4b
    base_url=os.getenv("OPENAI_BASE_URL"),         # http://localhost:1234/v1
    openai_api_key=os.getenv("OPENAI_API_KEY"),    # dummy
    temperature=0.7
)