import os
import openai
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings
from llama_index.embeddings.openai import OpenAIEmbedding

# ✅ Load OpenAI API Key from Environment Variables
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("❌ OPENAI_API_KEY is not set. Please add it to your environment variables.")

openai.api_key = api_key

# ✅ Load documents from BOTH directories
documents = []
for directory in ["./pagerduty_docs", "./best_practices"]:
    documents.extend(SimpleDirectoryReader(directory).load_data())

# ✅ Use OpenAI's Embedding Model for Better Retrieval
Settings.embed_model = OpenAIEmbedding(model="text-embedding-ada-002")

# ✅ Create an index using embeddings
index = VectorStoreIndex.from_documents(documents)

# ✅ Save the index
index.storage_context.persist("index_store")

print("✅ Successfully created and saved the document index with improved embeddings!")
