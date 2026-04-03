# Windows Installation & Setup Guide - Adaptive RAG

Complete step-by-step instructions to run the Adaptive RAG application on Windows machines with demo examples and verification steps.

---

## 📋 Prerequisites

### System Requirements
- **OS**: Windows 10 or Windows 11 (64-bit)
- **Python**: 3.9 or higher (3.13+ recommended)
- **RAM**: 8GB minimum (16GB recommended for LLM operations)
- **Disk Space**: 10GB for dependencies and models
- **Network**: Internet connection for API calls and model downloads

### Required Services (Optional but Recommended)
- **MongoDB**: For persistent chat history storage
- **Docker**: For MongoDB containerization (alternative to local installation)

### Required API Keys
- **OpenAI API Key**: For gpt/gemma LLM access
- **Tavily API Key**: For web search functionality (optional)

---

## 🔧 Step 1: Clone and Setup Project

### 1.1 Clone the Repository

```powershell
# Navigate to your desired workspace
cd C:\Projects\Automations\adaptive_rag

# Clone the repository
git clone https://github.com/dhruvsinghal09/Adaptive-Rag.git
cd Adaptive-Rag-main
```

**Expected Output:**
```
Cloning into 'Adaptive-Rag-main'...
remote: Enumerating objects: 150, done.
remote: Counting objects: 100% (150/150), done.
Receiving objects: 100% [================================>] 150/150 (1.2 MiB)
Resolving deltas: 100% [================================>] 45/45, done.
```

### 1.2 Create Python Virtual Environment

```powershell
# Create virtual environment
python -m venv venv

# Activate virtual environment (Windows)
.\venv\Scripts\Activate.ps1
```

**Expected Output:**
```
(venv) PS C:\Projects\Automations\adaptive_rag\Adaptive-Rag-main>
```

If you get an execution policy error, run:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### 1.3 Install Dependencies

```powershell
# Upgrade pip
python -m pip install --upgrade pip

# Install all required packages
pip install -r requirements.txt
```

**Expected Output:**
```
Requirement already satisfied: langchain~=0.3.27 in c:\projects\automations\adaptive_rag\...
[... package installation logs ...]
Successfully installed [XX packages]
```

---

## 🔐 Step 2: Configure Environment Variables

### 2.1 Create .env File

Create a `.env` file in the project root directory:

```powershell
# Create .env file
New-Item -Path . -Name ".env" -ItemType "file" -Force
```

### 2.2 Add Configuration Values

Open `.env` in your editor and add:

```env
# ============================================================================
# OPENAI CONFIGURATION (Required)
# ============================================================================
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_BASE_URL=http://localhost:1234/v1
MODEL_NAME=google/gemma-3-4b

# ============================================================================
# TAVILY SEARCH CONFIGURATION (Optional - for web search)
# ============================================================================
TAVILY_API_KEY=your_tavily_api_key_here

# ============================================================================
# QDRANT CONFIGURATION (Optional - defaults to FAISS)
# ============================================================================
QDRANT_URL=http://localhost:6333
QDRANT_API_KEY=your_qdrant_api_key
QDRANT_CODE_COLLECTION=code_documents
QDRANT_DOCS_COLLECTION=documents

# ============================================================================
# MONGODB CONFIGURATION (Optional - for persistent chat history)
# ============================================================================
MONGODB_URL=mongodb://localhost:27017
MONGODB_DB_NAME=adaptive_rag
```

### 2.3 Verify Configuration

```powershell
# Check if .env exists
Test-Path .env

# Verify required keys are set
$env_content = Get-Content .env | Select-String "OPENAI_API_KEY|OPENAI_BASE_URL|MODEL_NAME"
Write-Output "Configuration keys found:"
$env_content
```

**Expected Output:**
```
True

Configuration keys found:
OPENAI_API_KEY=sk-...
OPENAI_BASE_URL=http://localhost:1234/v1
MODEL_NAME=google/gemma-3-4b
```

---

## 🗄️ Step 3: Setup MongoDB (Optional - For Chat History Persistence)

### Option A: MongoDB Local Installation

#### Download and Install

1. Download from: https://www.mongodb.com/try/download/community
2. Choose Windows MSI installer
3. Run the installer and select:
   - Custom installation
   - Install MongoDB as a Windows Service
   - Data path: `C:\data\db`
   - Log path: `C:\data\log`

#### Start MongoDB Service

```powershell
# Start MongoDB service
Start-Service MongoDB

# Verify MongoDB is running
Get-Service MongoDB | Select-Object Name,Status,StartType

# Test connection
$connection = Test-NetConnection -ComputerName localhost -Port 27017
if ($connection.TcpTestSucceeded) {
    Write-Output "MongoDB is running on port 27017 ✓"
} else {
    Write-Output "MongoDB is NOT running ✗"
}
```

**Expected Output:**
```
Status   StartType
------   ---------
Running  Automatic

MongoDB is running on port 27017 ✓
```

### Option B: MongoDB with Docker

If Docker is installed:

```powershell
# Pull MongoDB image
docker pull mongo:latest

# Run MongoDB container
docker run -d `
  --name mongodb-adaptive-rag `
  -p 27017:27017 `
  -e MONGO_INITDB_ROOT_USERNAME=admin `
  -e MONGO_INITDB_ROOT_PASSWORD=password `
  mongo:latest

# Verify container is running
docker ps --filter "name=mongodb"

# View logs
docker logs mongodb-adaptive-rag
```

**Expected Output:**
```
CONTAINER ID   IMAGE    PORTS                      NAMES
abc123def456   mongo    0.0.0.0:27017->27017/tcp   mongodb-adaptive-rag
```

---

## 🚀 Step 4: Launch Application

### 4.1 Terminal 1 - Start FastAPI Backend

```powershell
# Ensure you're in the project directory and venv is activated
cd C:\Projects\Automations\adaptive_rag\Adaptive-Rag-main
.\venv\Scripts\Activate.ps1

# Start the FastAPI server
python -m uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

**Expected Output:**
```
INFO:     Will watch for changes in these directories: ['C:\Projects\Automations\adaptive_rag\Adaptive-Rag-main']
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Application startup complete.
⚠️ No documents uploaded → creating dummy vectorstore
✅ Using existing FAISS vectorstore
```

### 4.2 Terminal 2 - Start Streamlit Frontend

Open a new PowerShell terminal and run:

```powershell
# Navigate to project
cd C:\Projects\Automations\adaptive_rag\Adaptive-Rag-main

# Activate venv
.\venv\Scripts\Activate.ps1

# Start Streamlit
streamlit run streamlit_app/home.py --server.port 8501
```

**Expected Output:**
```
  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://10.177.182.120:8501
```

---

## 🌐 Step 5: Access the Application

### Web Interface

Open your browser and navigate to:

| Service | URL | Purpose |
|---------|-----|---------|
| **Streamlit Chat UI** | http://localhost:8501 | Chat interface & document upload |
| **FastAPI Docs** | http://localhost:8000/docs | Interactive API documentation |
| **ReDoc** | http://localhost:8000/redoc | Alternative API documentation |

### API Root Endpoint

Test the API is running:

```powershell
# Test root endpoint
$response = Invoke-RestMethod -Uri "http://localhost:8000/" -UseBasicParsing
$response | ConvertTo-Json
```

**Expected Output:**
```json
{
  "message": "Adaptive RAG API is running"
}
```

---

## 📝 Step 6: Demo - Complete End-to-End Test

### Demo 1: Simple Query via API

```powershell
# Send a simple query to the backend
$query_body = @{
    query = "Hello, give me a one-line greeting."
    session_id = "demo-session-001"
} | ConvertTo-Json

$response = Invoke-RestMethod `
    -Method Post `
    -Uri "http://localhost:8000/rag/query" `
    -ContentType "application/json" `
    -Body $query_body

Write-Output "Query Response:"
$response.result.content
Write-Output ""
Write-Output "Full Response:"
$response | ConvertTo-Json -Depth 4
```

**Expected Output:**
```
Query Response:
Hi there! 😊 Would you like to chat?

Full Response:
{
  "result": {
    "content": "Hi there! 😊 Would you like to chat?",
    "type": "ai",
    "response_metadata": {
      "token_usage": {
        "completion_tokens": 13,
        "prompt_tokens": 19,
        "total_tokens": 32
      },
      "model_name": "google/gemma-3-4b",
      "finish_reason": "stop"
    }
  }
}
```

### Demo 2: Multi-Turn Conversation

```powershell
# First turn
$turn1_body = @{
    query = "What is machine learning?"
    session_id = "demo-session-002"
} | ConvertTo-Json

$turn1_response = Invoke-RestMethod `
    -Method Post `
    -Uri "http://localhost:8000/rag/query" `
    -ContentType "application/json" `
    -Body $turn1_body

Write-Output "Turn 1 Response:"
Write-Output $turn1_response.result.content

# Second turn (same session)
Start-Sleep -Seconds 2
$turn2_body = @{
    query = "Can you explain neural networks specifically?"
    session_id = "demo-session-002"
} | ConvertTo-Json

$turn2_response = Invoke-RestMethod `
    -Method Post `
    -Uri "http://localhost:8000/rag/query" `
    -ContentType "application/json" `
    -Body $turn2_body

Write-Output ""
Write-Output "Turn 2 Response:"
Write-Output $turn2_response.result.content
```

**Expected Output:**
```
Turn 1 Response:
Machine learning is a subset of artificial intelligence that enables systems to learn and 
improve from experience without being explicitly programmed. It uses algorithms to analyze 
data, identify patterns, and make predictions...

Turn 2 Response:
Neural networks are computing systems inspired by biological neural networks in animal brains. 
They consist of interconnected nodes (neurons) organized in layers that process information...
```

### Demo 3: Document Upload via API

```powershell
# Create a test document
$test_doc_content = @"
# Python Programming Guide

Python is a high-level, interpreted programming language known for its simplicity
and readability. It supports multiple programming paradigms including object-oriented,
functional, and procedural programming.

## Key Features
- Easy to learn and read
- Powerful standard library
- Cross-platform compatibility
- Large ecosystem of third-party libraries

## Installation
Visit python.org and download the latest version (3.9+)
"@

# Save to temporary file
$test_doc_path = "C:\temp\python_guide.txt"
Set-Content -Path $test_doc_path -Value $test_doc_content

# Upload document
$file_upload = @{
    file = Get-Item $test_doc_path
}

$headers = @{
    "X-Description" = "Python programming guide and best practices"
}

$upload_response = Invoke-RestMethod `
    -Method Post `
    -Uri "http://localhost:8000/rag/documents/upload" `
    -Form $file_upload `
    -Headers $headers

Write-Output "Document Upload Response:"
$upload_response | ConvertTo-Json
```

**Expected Output:**
```json
{
  "status": true
}
```

### Demo 4: Query After Document Upload

```powershell
# Query about the uploaded document
$doc_query_body = @{
    query = "What are the key features of Python?"
    session_id = "demo-session-003"
} | ConvertTo-Json

$doc_response = Invoke-RestMethod `
    -Method Post `
    -Uri "http://localhost:8000/rag/query" `
    -ContentType "application/json" `
    -Body $doc_query_body

Write-Output "Response (should reference uploaded document):"
Write-Output $doc_response.result.content
```

**Expected Output:**
```
Response (should reference uploaded document):
Based on the Python programming guide provided, the key features of Python are:

1. Easy to learn and read - Python's syntax is simple and intuitive
2. Powerful standard library - Comes with extensive built-in functions and modules
3. Cross-platform compatibility - Runs on Windows, Linux, Mac, and other systems
4. Large ecosystem of third-party libraries - Extensive third-party packages available via pip
```

### Demo 5: Streamlit UI Workflow

#### Step 1: Access the UI
```
Browser URL: http://localhost:8501
```

#### Step 2: Upload Document via Sidebar
1. Click "Upload a PDF or TXT file" button
2. Select a document (`.txt` or `.pdf`)
3. Enter document description in the text field
4. Confirm upload

#### Step 3: Chat with Document
1. Enter question in chat input: "What is the main topic of this document?"
2. Press Enter or click Send
3. Wait for assistant response

#### Step 4: Multi-turn Conversation
- Continue asking follow-up questions
- Chat history is maintained in the session
- Context is preserved across messages

---

## ✅ Verification Checklist

### Services Running

```powershell
# Check all services
Write-Output "=== Service Status ==="

# API Status
$api = Invoke-WebRequest -Uri http://localhost:8000/ -UseBasicParsing
Write-Output "FastAPI Backend: $($api.StatusCode) OK"

# UI Status
$ui = Invoke-WebRequest -Uri http://localhost:8501/ -UseBasicParsing
Write-Output "Streamlit Frontend: $($ui.StatusCode) OK"

# MongoDB Status (if installed)
$mongo = Test-NetConnection -ComputerName localhost -Port 27017 -WarningAction SilentlyContinue
Write-Output "MongoDB: $(if($mongo.TcpTestSucceeded) {'OK'} else {'NOT RUNNING (optional)'})"

# Environment Variables
Write-Output ""
Write-Output "=== Environment Configuration ==="
$required_keys = @('OPENAI_API_KEY', 'OPENAI_BASE_URL', 'MODEL_NAME')
foreach ($key in $required_keys) {
    $value = [System.Environment]::GetEnvironmentVariable($key)
    $status = if ([string]::IsNullOrEmpty($value)) { "MISSING" } else { "OK" }
    Write-Output "$key`: $status"
}
```

**Expected Output:**
```
=== Service Status ===
FastAPI Backend: 200 OK
Streamlit Frontend: 200 OK
MongoDB: OK

=== Environment Configuration ===
OPENAI_API_KEY: OK
OPENAI_BASE_URL: OK
MODEL_NAME: OK
```

---

## 🔧 Troubleshooting

### Issue 1: "ModuleNotFoundError: No module named 'src'"

**Solution:**
```powershell
# Ensure you're in the correct directory
cd C:\Projects\Automations\adaptive_rag\Adaptive-Rag-main

# Verify project structure
Get-ChildItem -Name | Where-Object { $_ -eq 'src' }
# Should show: src

# Try running again
python -m uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

### Issue 2: "Port 8000 is already in use"

```powershell
# Find process using port 8000
$process = Get-Process | Where-Object {
    $_.Name -match "python" -or $_.Name -match "uvicorn"
}
$process | Stop-Process -Force

# Or use a different port
python -m uvicorn src.main:app --reload --host 0.0.0.0 --port 8001
```

### Issue 3: "MongoDB connection refused"

```powershell
# If MongoDB is optional, your app will fallback to in-memory chat history
# This is normal for development. To fix:

# Check if service is installed
Get-Service MongoDB -ErrorAction SilentlyContinue

# Start if installed
if ($?) { Start-Service MongoDB }

# If not installed, follow Step 3 to install MongoDB
```

### Issue 4: "OPENAI_API_KEY is empty"

```powershell
# Edit .env file and add your actual API key
# Get key from: https://platform.openai.com/api-keys

# Verify it's loaded
$env_content = Get-Content .env | Select-String OPENAI_API_KEY
Write-Output $env_content
```

---

## 📊 System Architecture

```
┌─────────────────────────────────────────────────────┐
│         Browser (http://localhost:8501)             │
│              Streamlit Web Interface                │
│         ┌──────────────────────────────────┐        │
│         │  • Chat Interface                │        │
│         │  • Document Upload Sidebar       │        │
│         │  • Session Management            │        │
│         └──────────────────────────────────┘        │
└────────────────────┬────────────────────────────────┘
                     │ HTTP/REST
                     ▼
        ┌──────────────────────────────────┐
        │   FastAPI Backend (port 8000)    │
        │  ┌────────────────────────────┐  │
        │  │  /rag/query endpoint       │  │
        │  │  /rag/documents/upload     │  │
        │  │  /docs (API documentation)│  │
        │  └────────────────────────────┘  │
        └────────┬──────────────────┬──────┘
                 │                  │
        ┌────────▼─────┐   ┌────────▼─────┐
        │ LangGraph    │   │ FAISS Vector │
        │ Orchestration│   │ Store        │
        │ • Query      │   │ (In-Memory)  │
        │ • Routing    │   │              │
        │ • Grading    │   │ OR MongoDB   │
        └──────┬───────┘   │ (Optional)   │
               │           └──────────────┘
        ┌──────▼──────────────────────┐
        │  LLM Inference              │
        │  google/gemma-3-4b          │
        │  (via http://localhost:1234)│
        └─────────────────────────────┘
```

---

## 📚 Additional Resources

### Documentation Files
- [README.md](README.md) - Main project overview
- [CODE_STYLE_GUIDE.md](CODE_STYLE_GUIDE.md) - Code formatting standards
- [QUICK_REFERENCE.md](QUICK_REFERENCE.md) - Quick usage patterns
- [QDRANT_SETUP_GUIDE.md](QDRANT_SETUP_GUIDE.md) - Vector database setup
- [DOCUMENT_UPLOAD_FLOW.md](DOCUMENT_UPLOAD_FLOW.md) - Document processing workflow

### External Links
- [OpenAI API Documentation](https://platform.openai.com/docs)
- [Tavily Search API](https://tavily.com/)
- [MongoDB Community](https://www.mongodb.com/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [LangChain Documentation](https://python.langchain.com/)

---

## 🎯 Next Steps

1. **Customize Prompts**: Edit `src/config/prompts.yaml` for custom system prompts
2. **Add Documents**: Upload your own documents via the web UI or API
3. **Configure Vector Database**: Switch from FAISS to Qdrant for production
4. **Setup Persistent Storage**: Enable MongoDB for chat history persistence
5. **Deploy**: Use Docker or cloud platforms for production deployment

---

## 💡 Tips & Best Practices

### Development
- Use `--reload` flag when running uvicorn for auto-reload on code changes
- Check logs in both terminal windows for debugging
- Use the FastAPI docs at http://localhost:8000/docs for API testing

### Performance
- Keep document chunks small (max 1000 chars) for better retrieval
- Use appropriate embedding models for your use case
- Monitor token usage for cost optimization

### Security
- Never commit `.env` file to version control
- Rotate API keys regularly
- Use HTTPS in production environments
- Implement rate limiting for public APIs

---

## 📞 Support & Issues

For issues or questions:
1. Check the Troubleshooting section above
2. Review application logs in both terminal windows
3. Check [DOCUMENTATION_INDEX.md](DOCUMENTATION_INDEX.md) for additional help
4. Review code examples in [QUICK_REFERENCE.md](QUICK_REFERENCE.md)

---

**Last Updated**: April 2, 2026  
**Version**: 1.0  
**Tested On**: Windows 11 with Python 3.13.7
