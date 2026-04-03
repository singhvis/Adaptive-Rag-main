# ⚡ Windows Quick-Start Guide

**TL;DR**: Get Adaptive RAG running in 5 minutes on Windows.

---

## 📦 Prerequisites (5 minutes)

```powershell
# 1. Install Python 3.9+ https://www.python.org/downloads/
python --version
# Output: Python 3.x.x

# 2. Clone repository
cd C:\Projects
git clone https://github.com/dhruvsinghal09/Adaptive-Rag.git
cd Adaptive-Rag-main
```

---

## ⚙️ Setup (2 minutes)

```powershell
# 3. Create & activate virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1

# 4. Install dependencies (first time: ~2-3 min)
pip install -r requirements.txt
```

---

## 🔑 Configure (1 minute)

Create `.env` file in project root with:

```env
OPENAI_API_KEY=your_key_here
OPENAI_BASE_URL=http://localhost:1234/v1
MODEL_NAME=google/gemma-3-4b
```

Get OpenAI key: https://platform.openai.com/api-keys

---

## 🚀 Launch (30 seconds)

### Terminal 1: Backend
```powershell
python -m uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

### Terminal 2: Frontend
```powershell
.\venv\Scripts\Activate.ps1
streamlit run streamlit_app/home.py --server.port 8501
```

### Terminal 3 (Optional): Test API
```powershell
$body = @{ query = "Hello!"; session_id = "test" } | ConvertTo-Json
Invoke-RestMethod -Method Post -Uri "http://localhost:8000/rag/query" `
    -ContentType "application/json" -Body $body
```

---

## 🌐 Access

| Service | URL |
|---------|-----|
| **Chat UI** | http://localhost:8501 |
| **API Docs** | http://localhost:8000/docs |

---

## ✅ Verify It Works

### UI Test
1. Open http://localhost:8501
2. Type: "Hello, what's your name?"
3. Click Send
4. Should see AI response ✓

### API Test
```powershell
$response = Invoke-RestMethod -Method Post -Uri "http://localhost:8000/rag/query" `
    -ContentType "application/json" `
    -Body (@{ query = "Test"; session_id = "quick-test" } | ConvertTo-Json)

$response.result.content  # Should see AI response
```

---

## 📝 Upload & Query Demo

### via UI (Web Browser)
1. Go to http://localhost:8501
2. Click upload button in sidebar
3. Select a `.txt` or `.pdf` file
4. Enter document description
5. Ask questions about it in chat ✓

### via API (PowerShell)
```powershell
# Upload document
$file_path = "C:\path\to\document.txt"
$headers = @{ "X-Description" = "My document" }
Invoke-RestMethod -Method Post -Uri "http://localhost:8000/rag/documents/upload" `
    -Form @{ file = Get-Item $file_path } -Headers $headers

# Query about it
$query_body = @{ 
    query = "What's in this document?"; 
    session_id = "demo" 
} | ConvertTo-Json

Invoke-RestMethod -Method Post -Uri "http://localhost:8000/rag/query" `
    -ContentType "application/json" -Body $query_body
```

---

## 🆘 Troubleshooting (30 seconds)

### Port 8000 already in use?
```powershell
# Kill Python processes
Get-Process python | Stop-Process -Force
# Retry with different port: --port 8002
```

### venv not found?
```powershell
# Recreate it
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### Import errors?
```powershell
# Ensure dependencies are installed
pip install -r requirements.txt --force-reinstall
```

### API returns error?
```powershell
# Check if OPENAI_API_KEY is set
Get-Content .env | Select-String OPENAI_API_KEY
# Should show: OPENAI_API_KEY=sk-...
```

---

## 📚 Next Steps

- **Full Setup**: Read [WINDOWS_INSTALLATION_GUIDE.md](WINDOWS_INSTALLATION_GUIDE.md)
- **Code Standards**: Read [CODE_STYLE_GUIDE.md](CODE_STYLE_GUIDE.md)
- **API Reference**: Go to http://localhost:8000/docs
- **Advanced Setup**: Read [QUICK_REFERENCE.md](QUICK_REFERENCE.md)

---

## 💡 Pro Tips

✓ Use `--reload` flag on uvicorn for auto-refresh  
✓ Check http://localhost:8000/docs for interactive API testing  
✓ Keep both terminal windows visible for easy debugging  
✓ Chat history works without MongoDB (in-memory fallback)  
✓ Document upload works with FAISS (built-in, no setup needed)  

---

**⏱️ Total Setup Time: ~10 minutes** (first run, includes downloads)

**Subsequent Runs: ~30 seconds** (just launch the 2 terminals)

---

For detailed troubleshooting, see: **[WINDOWS_INSTALLATION_GUIDE.md](WINDOWS_INSTALLATION_GUIDE.md)**
