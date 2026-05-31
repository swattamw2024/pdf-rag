# PDF RAG — Ask Questions to Your Documents (Offline)

A simple tool that lets you **upload PDF or Word files** and **ask questions** about them — all running on your computer with **no internet needed** (after initial setup).

Two ways to use it:
- **Web App** — a browser-based chat interface (easiest)
- **Command Line** — for terminal users

---

## How It Works

1. You upload a PDF or Word document
2. The tool reads and indexes the content locally
3. You ask questions in plain English
4. A local AI model reads the relevant parts and gives you an answer

Everything stays on your machine. No data is sent to the cloud.

---

## Setup Instructions

### Step 1: Install Python

You need Python 3.10 or newer.

**Mac:**
```
Open Terminal and run:
brew install python
```

**Windows:**
```
1. Go to https://www.python.org/downloads/
2. Download the latest Python (3.12 or newer)
3. Run the installer
4. IMPORTANT: Check the box that says "Add Python to PATH" before clicking Install
5. Click "Install Now"
```

To verify Python is installed, open Terminal (Mac) or Command Prompt (Windows) and type:
```
python --version
```
You should see something like `Python 3.12.x`.

---

### Step 2: Install Ollama (the local AI engine)

Ollama runs the AI model on your computer.

**Mac:**
```
Open Terminal and run:
brew install ollama
```

**Windows:**
```
1. Go to https://ollama.com/download
2. Click "Download for Windows"
3. Run the installer and follow the prompts
```

---

### Step 3: Download an AI Model (one-time, needs internet)

This downloads the AI brain to your computer (~2-4 GB). You only need to do this once.

Open Terminal (Mac) or Command Prompt (Windows) and run:
```
ollama pull llama3.2
```

Wait for it to finish downloading.

---

### Step 4: Start the Ollama Server

Before using the tool, Ollama needs to be running in the background.

**Mac:**
```
ollama serve
```

**Windows:**
```
Ollama usually starts automatically after installation.
If not, open Command Prompt and run:
ollama serve
```

Leave this running. Open a **new** Terminal/Command Prompt window for the next steps.

---

### Step 5: Download This Project

**Option A — If you have Git installed:**
```
git clone https://github.com/swattamw2024/pdf-rag.git
cd pdf-rag
```

**Option B — Download as ZIP:**
```
1. Go to https://github.com/swattamw2024/pdf-rag
2. Click the green "Code" button
3. Click "Download ZIP"
4. Extract the ZIP file
5. Open Terminal/Command Prompt and navigate to the extracted folder
```

---

### Step 6: Create a Virtual Environment (Recommended)

A virtual environment keeps this project's libraries separate from your other Python projects. This avoids conflicts.

Make sure you are inside the `pdf-rag` folder, then run:

**Mac:**
```
python3 -m venv venv
source venv/bin/activate
```

**Windows (Command Prompt):**
```
python -m venv venv
venv\Scripts\activate
```

**Windows (PowerShell):**
```
python -m venv venv
venv\Scripts\Activate.ps1
```

After activating, you should see `(venv)` at the beginning of your terminal line. This means the virtual environment is active.

> **Note:** Every time you open a new Terminal/Command Prompt to use this tool, you need to activate the virtual environment again by running the `activate` command above.

---

### Step 7: Install Project Dependencies

Run this command inside the `pdf-rag` folder (with the virtual environment activated):

**Mac:**
```
pip install -r requirements.txt
```

**Windows:**
```
pip install -r requirements.txt
```

This will download the required Python libraries. It may take a few minutes.

---

## Using the Web App (Recommended for Beginners)

This opens a chat interface in your browser.

> **Remember:** Always activate the virtual environment first before running any commands.

**Mac:**
```
cd pdf-rag
source venv/bin/activate
streamlit run src/web_app.py
```

**Windows (Command Prompt):**
```
cd pdf-rag
venv\Scripts\activate
streamlit run src/web_app.py
```

**Windows (PowerShell):**
```
cd pdf-rag
venv\Scripts\Activate.ps1
streamlit run src/web_app.py
```

Your browser will open automatically with the app. If it doesn't, go to `http://localhost:8501`.

### How to use the Web App:
1. **Upload files** — Use the sidebar on the left to upload your PDF or Word files
2. **Click "Ingest"** — This processes your documents (wait for it to finish)
3. **Ask questions** — Type your question in the chat box at the bottom
4. **View sources** — Click "Sources" under each answer to see where it came from

---

## Using the Command Line

> **Remember:** Always activate the virtual environment first before running any commands.
>
> **Mac:** `source venv/bin/activate`
> **Windows CMD:** `venv\Scripts\activate`
> **Windows PowerShell:** `venv\Scripts\Activate.ps1`

### Ingest (load) a document:
```
python -m src.cli ingest /path/to/your/document.pdf
```

### Ingest all documents in a folder:
```
python -m src.cli ingest /path/to/folder/
```

### Ask a question:
```
python -m src.cli ask "What is this document about?"
```

### Start interactive chat:
```
python -m src.cli chat
```
Type your questions one by one. Type `quit` to exit.

### List all document collections:
```
python -m src.cli list
```

### Delete a collection:
```
python -m src.cli clear
```

---

## Supported File Types

| Format | Extension |
|--------|-----------|
| PDF    | `.pdf`    |
| Word   | `.docx`   |

---

## Troubleshooting

### "No module named 'streamlit'" or "No module named 'click'" (after install)
You probably forgot to activate the virtual environment. Run the activate command first:

**Mac:**
```
source venv/bin/activate
```

**Windows (Command Prompt):**
```
venv\Scripts\activate
```

**Windows (PowerShell):**
```
venv\Scripts\Activate.ps1
```

If you want to **leave** the virtual environment when you're done, just type:
```
deactivate
```

---

### "Cannot connect to Ollama"
Make sure Ollama is running. Open a Terminal/Command Prompt and run:
```
ollama serve
```

### "No module named 'src'"
Make sure you are inside the `pdf-rag` folder before running commands:
```
cd pdf-rag
```

### Python command not found (Windows)
If `python` doesn't work, try `python3`. If neither works, reinstall Python and make sure to check **"Add Python to PATH"** during installation.

### Slow responses
The first question after starting may take 30-60 seconds as the AI model loads into memory. Subsequent questions will be faster.

### Out of memory errors
If your computer has less than 8 GB of RAM, use a smaller model:
```
ollama pull phi3
```
Then set the environment variable before running:

**Mac:**
```
export PDF_RAG_MODEL=phi3
```

**Windows (Command Prompt):**
```
set PDF_RAG_MODEL=phi3
```

---

## Configuration (Optional)

You can customize behavior with environment variables:

| Variable | Default | Description |
|----------|---------|-------------|
| `PDF_RAG_MODEL` | `llama3.2` | Ollama model to use |
| `PDF_RAG_DB_PATH` | `./data/chroma_db` | Where to store the vector database |

---

## Requirements

- **Python** 3.10 or newer
- **Ollama** installed and running
- **8 GB RAM** minimum (16 GB recommended)
- **4 GB disk space** for the AI model
- **No internet** needed after initial setup
