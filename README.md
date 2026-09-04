
# ️ Text2Speech

A lightweight, fast, and high-quality Text-to-Speech application powered by Microsoft's Edge-TTS. It features smart auto-naming, batch processing, and a beautiful built-in web interface. 

**No heavy local models. No complex C++ dependencies. Just pure, high-quality audio generation.**

---

## ✨ Features

- ✅ **Zero Local Storage**: No massive model files (~0MB footprint).
- ✅ **High Quality**: Near-human, expressive voice quality (powered by Microsoft Azure).
- ✅ **Smart Auto-Naming**: Automatically names output files based on the first few words (e.g., `Hello_world_I_am.mp3`).
- ✅ **Batch Processing**: Convert entire text files into multiple organized audio clips with one click.
- ✅ **Cross-Platform**: Works flawlessly on Windows, macOS, and Linux.
- ✅ **Dual Interface**: Use the modern Web UI or the Command Line Interface (CLI).

*(Note: An active internet connection is required for synthesis.)*

---

## 🚀 Quick Start (Automated Setup)

### Prerequisites
- [Python 3.8 or higher](https://www.python.org/downloads/) installed.
- `pip` (Python package installer).
- An active internet connection.

### Step 1: Download the Project
Clone the repository or download the ZIP file and extract it.
```bash
git clone https://github.com/your-username/Text2Speech.git
cd Text2Speech
```

### Step 2: Run the Setup Script
Run the setup script for your operating system. This will create the necessary folders and install all dependencies automatically.

**🍎 macOS /  Linux:**
```bash
chmod +x setup.sh
./setup.sh
```

**🪟 Windows:**
```cmd
setup.bat
```
*(If you get a permission error on Windows, right-click `setup.bat` and select "Run as Administrator".)*

---

## 🛡️ Bulletproof Manual Setup (Recommended for Developers)

If the automated script fails, or if you want to use a **Virtual Environment** (highly recommended to avoid system conflicts), follow these exact steps.

### 1. Create a Virtual Environment
**🍎 macOS / 🐧 Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**🪟 Windows (Command Prompt):**
```cmd
python -m venv venv
venv\Scripts\activate.bat
```

** Windows (PowerShell):**
```powershell
python -m venv venv
venv\Scripts\Activate.ps1
```
*(Note: If PowerShell blocks activation, run: `Set-ExecutionPolicy Unrestricted -Scope CurrentUser`)*

### 2. Install Dependencies
Once your virtual environment is active (you will see `(venv)` in your terminal), run:
```bash
pip install -r requirements.txt
```

---

## 💻 Running the Application

### 🌐 Option 1: Web Interface (Recommended)
Start the built-in web server:
```bash
uvicorn app:app --reload
```
Open your browser and go to: **http://127.0.0.1:8000**

### ⌨️ Option 2: Command Line Interface (CLI)

**Interactive Mode:**
```bash
python main.py
```

**Single Text Synthesis:**
```bash
python main.py -t "Hello world, I am finally speaking!" -v en-US-GuyNeural
```

**Batch Mode (from a text file):**
```bash
python main.py -f input.txt -v en-GB-SoniaNeural
```
*(Each line in `input.txt` will be converted to a separate, auto-named MP3 file in the `output/` folder.)*

**Custom Output Filename:**
```bash
python main.py -t "Hello" -o custom_name.mp3
```

---

##  Comprehensive Troubleshooting Guide

If you encounter any issues, find the solution below.

### 1. "python" or "pip" is not recognized as a command
* **Cause:** Python is not added to your system's PATH.
* **Fix (Mac/Linux):** Use `python3` and `pip3` instead of `python` and `pip`.
* **Fix (Windows):** Reinstall Python from python.org and **check the box** that says *"Add Python to PATH"* during installation.

### 2. Permission Denied (Mac/Linux)
* **Cause:** The OS is blocking the execution of downloaded scripts or binaries.
* **Fix:** Run this command in your terminal to grant execute permissions:
  ```bash
  chmod +x setup.sh
  chmod +x main.py
  ```

### 3. Port 8000 is already in use
* **Cause:** Another application (or a previous crashed instance of this app) is using the port.
* **Fix:** Run the server on a different port:
  ```bash
  uvicorn app:app --reload --port 8001
  ```
* **Kill the process manually:**
  * **Mac/Linux:** `lsof -i :8000` then `kill -9 <PID>`
  * **Windows:** `netstat -ano | findstr :8000` then `taskkill /PID <PID> /F`

### 4. ModuleNotFoundError: No module named 'edge_tts' (or 'fastapi')
* **Cause:** The dependencies were not installed, or you are running the script outside your virtual environment.
* **Fix:** 
  1. Ensure your virtual environment is active: `(venv)` should be visible in your terminal.
  2. Run: `pip install -r requirements.txt`

### 5. Voices not loading in the Web UI
* **Cause:** The Edge-TTS API request timed out or was blocked by a firewall.
* **Fix:** The app has a built-in fallback list of voices. If the API fails, it will automatically load 8 default high-quality voices. Check your internet connection and refresh the page.

### 6. Windows Asyncio / Event Loop Errors
* **Cause:** Windows handles asynchronous loops differently than Mac/Linux.
* **Fix:** If you write custom async code and get an event loop error, add this to the very top of your `main.py` or `app.py`:
  ```python
  import asyncio
  import sys
  if sys.platform == 'win32':
      asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
  ```

---

##  Project Structure

```text
Text2Speech/
│
├── output/                 # Generated MP3 files are saved here
├── logs/                   # Log files (if enabled in config)
│
── main.py                 # CLI Entry point
├── tts_engine.py           # Core TTS logic (Edge-TTS)
├── app.py                  # FastAPI Web Server
├── index.html              # Web UI Frontend
├── config.yaml             # Project configuration
├── requirements.txt        # Python dependencies
├── setup.sh                # Mac/Linux setup script
├── setup.bat               # Windows setup script
└── README.md               # This file
```

---

## ⚙️ Configuration

Edit `config.yaml` to adjust project-wide settings:
```yaml
output:
  directory: "./output"
  
logging:
  level: "INFO"            # Options: DEBUG, INFO, WARNING, ERROR
  save_to_file: false      # Set to true to save logs to ./logs/tts.log
```

---

## 📜 License & Credits

- **Engine**: [Edge-TTS](https://github.com/rany2/edge-tts) (Uses Microsoft Azure's free TTS endpoints).
- **Web Framework**: [FastAPI](https://fastapi.tiangolo.com/) & [Uvicorn](https://www.uvicorn.org/).
- **License**: MIT License.
```

***
