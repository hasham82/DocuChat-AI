Complete Installation Guide - 100% FREE RAG Chatbot
This guide will help you set up the RAG chatbot with completely free tools. No API costs!

🎯 What You'll Install
Python 3.12 - Programming language
Ollama - FREE local LLM (runs on your computer)
HuggingFace Models - FREE embeddings (auto-downloaded)
Python Packages - All free libraries
Step 1: Install Python 3.12
Windows:
Download from python.org/downloads
IMPORTANT: Check "Add Python to PATH" during installation
Verify: Open Command Prompt and type:
bash
   python --version
Should show: Python 3.12.x

Step 2: Install Ollama (FREE Local LLM)
What is Ollama?
Ollama runs AI models locally on your computer - no internet needed after setup, completely free!

Windows Installation:
Download Ollama:
Go to ollama.ai
Click "Download for Windows"
Run the installer (OllamaSetup.exe)
Install and Verify:
Ollama will start automatically after installation
You'll see an Ollama icon in your system tray (bottom-right corner)
Open Command Prompt and verify:
bash
     ollama --version
Download a Model (Choose ONE): Option A: Llama 3.1 (Recommended)
Best quality, 8B parameters
Size: ~4.7 GB
Speed: 2-5 seconds per response
bash
   ollama pull llama3.1
Option B: Mistral

Good balance, 7B parameters
Size: ~4.1 GB
Speed: 1-3 seconds per response
bash
   ollama pull mistral
Option C: Phi-3 (Fastest)

Lightest, 3.8B parameters
Size: ~2.3 GB
Speed: 0.5-2 seconds per response
bash
   ollama pull phi3
Test the Model:
bash
   ollama run llama3.1
Type: "Hello, how are you?"

If you get a response, it's working! Type /bye to exit.

Step 3: Setup the Project
3.1 Download/Clone the Project
bash
# Create project folder
mkdir rag-chatbot
cd rag-chatbot

# If using git:
git clone https://github.com/hasham82/DocuChat-AI .

# Or manually: Extract the project files here
3.2 Create Virtual Environment
bash
# Create virtual environment
python -m venv venv

# Activate it
venv\Scripts\activate

# You should see (venv) in your terminal now
3.3 Install Python Packages
bash
pip install -r requirements.txt
First-time installation takes 2-5 minutes as it downloads:

LangChain libraries
ChromaDB
Streamlit
HuggingFace sentence-transformers (~80MB)
Other dependencies
Step 4: Configuration
4.1 Create Folder Structure
Make sure these folders exist:

bash
mkdir data\raw
mkdir data\processed
4.2 Verify Configuration
Open config.yaml and make sure it has:

yaml
embeddings:
  provider: "huggingface"
  model: "all-MiniLM-L6-v2"

llm:
  provider: "ollama"
  model: "llama3.1"  # Or the model you downloaded
  base_url: "http://localhost:11434"
Change the model name if you downloaded a different one (mistral or phi3).

Step 5: Add Sample Documents
5.1 Create Test Documents
Create a file data/raw/sample.txt:

text
Introduction to Python Programming

Python is a high-level, interpreted programming language created by Guido van Rossum. 
It was first released in 1991 and has become one of the most popular programming languages.

Key Features:
1. Easy to learn and read
2. Extensive standard library
3. Cross-platform compatibility
4. Large community support

Python is widely used in:
- Web development
- Data science and machine learning
- Automation and scripting
- Scientific computing

Popular Python frameworks include Django, Flask, TensorFlow, and PyTorch.
5.2 Add Your Own Documents
You can add:

PDF files (.pdf)
Text files (.txt)
Word documents (.docx)
Just place them in the data/raw/ folder.

Step 6: Run the Application
6.1 First Time Test (Optional)
Test each component:

bash
# Test document ingestion
python src/ingestion.py

# Test embeddings (will download model first time)
python src/embeddings.py

# Test complete pipeline
python src/chatbot.py
6.2 Launch Web Interface
bash
streamlit run app/streamlit_app.py
The app will open automatically at: http://localhost:8501

Step 7: Using the Chatbot
Upload Documents:
Click "Browse files" in the sidebar
Select PDF/TXT/DOCX files
Click "Process Documents"
Wait for "✅ Processed X documents"
Ask Questions:
Type in the chat box at the bottom
Example: "What is Python used for?"
Wait for response (2-5 seconds)
View Sources:
Click "View Sources" to see which documents were used
🔧 Troubleshooting
Problem: "ollama: command not found"
Solution:

Restart your terminal/Command Prompt
Check if Ollama is in system tray
Reinstall from ollama.ai
Problem: "Cannot connect to Ollama"
Solution:

bash
# Check if Ollama is running
ollama list

# If nothing happens, restart Ollama service:
# Look for Ollama icon in system tray, right-click, restart

# Or run manually:
ollama serve
Problem: "Model not found"
Solution:

bash
# List installed models
ollama list

# Pull the model again
ollama pull llama3.1

# Update config.yaml with the correct model name
Problem: "HuggingFace model download stuck"
Solution:

Check internet connection
Try a different model in config.yaml:
yaml
   embeddings:
     model: "paraphrase-MiniLM-L3-v2"  # Smaller, faster
Clear cache and retry:
bash
   # Windows
   rmdir /s %USERPROFILE%\.cache\huggingface
Problem: "Slow responses"
Solution:

Use a faster model:
bash
   ollama pull phi3
Update config.yaml:

yaml
   llm:
     model: "phi3"
Reduce retrieved documents:
In Streamlit sidebar, reduce "Number of Documents" to 2-3
Use GPU (if you have NVIDIA GPU):
In src/embeddings.py, change:
python
     model_kwargs={'device': 'cuda'}
Problem: "Out of memory"
Solution:

Use a smaller model (phi3)
Reduce chunk size in config.yaml:
yaml
   embeddings:
     chunk_size: 500
Process fewer documents at once
Close other applications
📊 System Requirements
Minimum:
CPU: Any modern processor (2+ cores)
RAM: 8 GB
Storage: 10 GB free space
OS: Windows 10+, macOS, Linux
Recommended:
CPU: 4+ cores
RAM: 16 GB
Storage: 20 GB SSD
GPU: NVIDIA GPU (optional, for faster processing)
Model Sizes:
Llama 3.1: ~4.7 GB
Mistral: ~4.1 GB
Phi-3: ~2.3 GB
Embeddings: ~80 MB
ChromaDB: ~10 MB + document size
🎓 Learning More
Recommended Resources:
Ollama Documentation: docs.ollama.ai
LangChain Tutorial: python.langchain.com
RAG Concepts: Search for "Retrieval Augmented Generation tutorial"
Try Different Models:
bash
# List all available models
ollama list

# Try different models
ollama pull codellama    # Good for code questions
ollama pull neural-chat  # Optimized for chat
ollama pull llama2       # Previous version
Experiment with Settings:
In config.yaml, try changing:

temperature: 0.0 (focused) to 1.0 (creative)
chunk_size: 500 (more chunks) to 2000 (fewer chunks)
k: Number of documents retrieved (2-10)
✅ Quick Verification Checklist
Before running, verify:

 Python 3.12 installed: python --version
 Ollama installed: ollama --version
 Model downloaded: ollama list shows your model
 Virtual environment activated: See (venv) in terminal
 Packages installed: pip list shows langchain, streamlit, etc.
 Sample document in data/raw/
 Config.yaml has correct model name
If all checked, you're ready to go! 🚀

🆘 Still Having Issues?
Check Ollama status: Look for icon in system tray
Restart everything: Close terminal, restart Ollama, reopen project
Update packages: pip install --upgrade -r requirements.txt
Clear cache: Delete chroma_db folder and recreate
Start fresh: Delete venv, create new one, reinstall
Remember: Everything runs locally on your computer. No internet needed after setup (except for initial downloads). Completely free! 🎉

