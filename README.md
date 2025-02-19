# 🛠️ PagerDuty Support Bot

**PagerDuty Support Bot** is an AI-powered chatbot designed to assist users with PagerDuty-related queries. It leverages **LlamaIndex**, **OpenAI embeddings**, and **Retriever-Augmented Generation (RAG)** to provide **accurate** and **context-aware** responses using PagerDuty documentation and best practices.

## 📌 Features

✅ **Natural Language Processing** - Understands and responds to user questions in a conversational format.  
✅ **Retriever-Augmented Generation (RAG)** - Searches documentation to generate precise answers.  
✅ **Memory Support** - Keeps track of previous user interactions for better responses.  
✅ **Flexible Embedding Model** - Uses OpenAI’s embedding model for intelligent document retrieval.  
✅ **Local Indexing** - Pre-processes PagerDuty documentation to improve query performance.  

---

## 📖 Setup & Installation

### 1️⃣ Clone the Repository
```
sh
git clone git@github.com:pdt-ahickmon/pd_support_bot.git
cd pd_support_bot
```

## 2️⃣ Set Up a Virtual Environment
Before installing dependencies, create and activate a virtual environment:
Mac/Linux:
```
python3 -m venv venv
source venv/bin/activate
```

Windows (Command prompt):
```
python -m venv venv
venv\Scripts\activate
```

Windows (PowerShell):
```
python -m venv venv
.\venv\Scripts\Activate
```

### 3️⃣ Install Dependencies
`pip install -r requirements.txt`

If requirements.txt is missing, regenerate it with:
`pip freeze > requirements.txt`

### 4️⃣ Set Up API Key
Create a .env file in the root directory and add your OpenAI API Key:
`echo "OPENAI_API_KEY=sk-your-api-key-here" > .env`

Alternatively, manually create .env and add:
`OPENAI_API_KEY=sk-your-api-key-here`

### 5️⃣ Index Documentation
Before running the bot, index the PagerDuty documentation:
`python index_docs.py`

---

## 🎯 Usage

### Run the Bot
To start the bot, run:
`python ask_support_bot.py`

You will see:
```🚀 Ask the PagerDuty AI Bot anything! (Type 'exit' to quit)
🟢 You:
```

---

## 🛑 Troubleshooting

### 1️⃣ Virtual Environment Not Found
If you see an error like ModuleNotFoundError, ensure the virtual environment is activated:
```
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate      # Windows
```

### 2️⃣ API Key Issues
If the bot fails due to an API key issue, double-check that:

The .env file is properly created.
Your API key is valid and active.

### 3️⃣ SSH Key Issues
If you cannot push to GitHub, ensure the correct SSH key is being used:
`ssh -T git@github.com`

---

## 🔧 Contributing

If you'd like to contribute:

1. Fork the repository.
2. Create a new feature branch (git checkout -b feature-branch).
3. Commit your changes (git commit -m "Added new feature").
4. Push to your branch (git push origin feature-branch).
5. Open a pull request.

---

## 📜 License

This project is licensed under the MIT License.
