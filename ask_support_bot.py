import os
import re
from collections import deque
from llama_index.core import StorageContext, load_index_from_storage
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.core.response_synthesizers import Refine

# ✅ Load OpenAI API Key from Environment Variables
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("❌ OPENAI_API_KEY is not set. Please add it to your environment variables.")

# ✅ Load the Indexed Documents
storage_context = StorageContext.from_defaults(persist_dir="index_store")
index = load_index_from_storage(storage_context)

# ✅ Chain-of-Thought Prompting + RAG (Injects Retrieved Docs into Prompt)
rag_prompt = """
You are a highly knowledgeable PagerDuty expert with deep understanding of best practices.
Use the **retrieved documentation below** to generate an accurate answer.

📖 **Retrieved Documentation:**
{retrieved_docs}

---

📝 **Conversation History:**
{chat_history}

---

Now answer the following question **using both retrieved docs and conversation context**:

Question: {query}
"""

# ✅ Initialize Memory (Stores last 5 exchanges)
chat_history = deque(maxlen=5)

# ✅ Fine-Tune the Query Engine with RAG (No More "Refine Context" Logs)
query_engine = RetrieverQueryEngine(
    retriever=index.as_retriever(similarity_top_k=5),  # Retrieve top 5 relevant docs
    response_synthesizer=Refine(verbose=False)  # Suppresses refine context logs
)

# ✅ List of Keywords Indicating a Setup/Configuration Question
setup_keywords = ["configure", "set up", "install", "create", "setup", "initialize"]

# ✅ Function to Detect Setup/Configuration Questions
def is_setup_question(query):
    return any(keyword in query.lower() for keyword in setup_keywords)

# ✅ Function to Ask Questions with Improved Formatting
def ask_bot(query):
    # Retrieve relevant docs
    retrieved_docs = query_engine.retriever.retrieve(query)
    doc_texts = "\n\n".join([doc.text for doc in retrieved_docs])

    # Include retrieved docs + chat history in the prompt
    history_text = "\n".join(chat_history)
    formatted_query = rag_prompt.format(retrieved_docs=doc_texts, chat_history=history_text, query=query)

    response = query_engine.query(formatted_query)

    # Store latest question & answer in memory
    chat_history.append(f"Q: {query}\nA: {response.response}")

    # ✅ Format response based on question type
    if is_setup_question(query):
        return format_as_steps(response.response)
    else:
        return response.response  # General response for non-setup questions

# ✅ Function to Format Answers as Steps
def format_as_steps(text):
    # Split the response into sentences
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())

    # Convert into a numbered list
    formatted_response = "\n".join([f"{i+1}. {sentence}" for i, sentence in enumerate(sentences)])

    return f"**Here are the steps:**\n{formatted_response}"

# ✅ Interactive Chat Loop
print("🚀 Ask the PagerDuty AI Bot anything! (Type 'exit' to quit)")
while True:
    query = input("\n🟢 You: ")
    if query.lower() in ["exit", "quit"]:
        print("👋 Exiting...")
        break
    response = ask_bot(query)
    print(f"\n🤖 PagerDuty Bot: {response}")
