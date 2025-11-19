# 🎤 Voice to Databricks Genie

Speak your data questions and automatically send them to Databricks Genie!

---

## 🚀 Quick Start

```bash
cd /Users/sumit.saraswat/Documents/whisper
./start_interactive.sh
```

Then:
1. Choose option **[1]** (5 seconds)
2. Speak your question when prompted
3. Question is **automatically sent to Genie** - no copy/paste!
4. Check your Genie room for the answer

---

## 📁 Project Files

- **`interactive_voice_auto.py`** - Main script (automatic Genie sending)
- **`start_interactive.sh`** - Launcher script
- **`databricks_connector.py`** - Databricks utilities
- **`requirements.txt`** - Python dependencies
- **`.env`** - Configuration (API keys, Genie Space ID)
- **`venv/`** - Python virtual environment

---

## ⚙️ Configuration

All settings in `.env`:
- ✅ OpenAI API Key (Whisper)
- ✅ Genie Space ID  
- ✅ Databricks Token (from ~/.databrickscfg)

---

## 🔧 Changing Configuration

Need to use a different Genie room or OpenAI key? All configuration is in **one file**: `.env`

### **Configuration File Location**
```
<project-directory>/.env
```
(Default: `/Users/sumit.saraswat/Documents/whisper/.env`)

### **How to Edit**

**Option 1: Using a text editor**
```bash
cd /Users/sumit.saraswat/Documents/whisper
nano .env
```

Or use:
```bash
open -e .env    # TextEdit
code .env       # VS Code
vim .env        # Vim
```

**Option 2: Recreate the file**
```bash
cd /Users/sumit.saraswat/Documents/whisper
cat > .env << 'EOF'
# OpenAI Configuration
OPENAI_API_KEY=your_openai_key_here

# Databricks Configuration
DATABRICKS_HOST=https://your-workspace.azuredatabricks.net
GENIE_SPACE_ID=your_genie_room_id_here
EOF
```

### **What to Change**

#### **1. Change Genie Room**

Find your Genie Room ID from the URL:
- URL format: `https://...databricks.net/genie/rooms/01f0b508373f18e7...`
- Copy the ID after `/rooms/`

Update in `.env`:
```bash
GENIE_SPACE_ID=your_new_genie_room_id
```

#### **2. Change OpenAI API Key**

Get a new key:
- Visit: https://platform.openai.com/api-keys
- Click "Create new secret key"
- Copy the key (starts with `sk-proj-...`)

Update in `.env`:
```bash
OPENAI_API_KEY=sk-proj-your_new_key_here
```

#### **3. Change Databricks Workspace**

**Recommended: Update in `.env`**
```bash
DATABRICKS_HOST=https://your-new-workspace.azuredatabricks.net
```

**Alternative: Edit Python code** (`interactive_voice_auto.py` at line 24):
```python
self.databricks_host = os.getenv('DATABRICKS_HOST', 'https://your-workspace.azuredatabricks.net')
```

#### **4. Change Databricks Token**

Edit `~/.databrickscfg` in your home directory:
```ini
[DEFAULT]
host = https://your-workspace.azuredatabricks.net
token = dapi_your_token_here
```

### **Complete .env Template**

```bash
# OpenAI Configuration
OPENAI_API_KEY=sk-proj-your_api_key_here

# Databricks Configuration
DATABRICKS_HOST=https://your-workspace.azuredatabricks.net
GENIE_SPACE_ID=your_genie_room_id_here
```

### **After Making Changes**

**If script is not running:** Changes take effect immediately

**If script is running:**
1. Press `Ctrl+C` or type `q` to quit
2. Run `./start_interactive.sh` again

### **Verify Your Changes**

```bash
cd /Users/sumit.saraswat/Documents/whisper
source venv/bin/activate
python3 << 'EOF'
import os
from dotenv import load_dotenv
load_dotenv()
print(f"✅ API Key: {os.getenv('OPENAI_API_KEY')[:20]}...")
print(f"✅ Genie Room: {os.getenv('GENIE_SPACE_ID')}")
EOF
```

### **Configuration Summary Table**

| What to Change | File to Edit | Location |
|----------------|--------------|----------|
| **Genie Room ID** | `.env` | Project directory |
| **OpenAI API Key** | `.env` | Project directory |
| **Databricks Workspace** | `.env` | Project directory |
| **Databricks Token** | `.databrickscfg` | Home directory (`~`) |

### **Security Tips**

- 🔒 Keep `.env` file secure - it contains sensitive API keys
- 🚫 Never commit `.env` to git (already in `.gitignore`)
- 🔄 You can switch between Genie rooms anytime by updating the ID
- 🔑 OpenAI keys can be rotated without code changes

---

## 🎯 How It Works

```
You speak → Whisper transcribes → Auto-sent to Genie → Done!
```

**Total time: ~5 seconds from question to Genie**

---

## 🎤 Example Questions

- "What were total sales last month"
- "Show me top 10 customers by revenue"
- "How many users signed up yesterday"
- "Compare Q3 and Q4 revenue"

---

## 🔗 Your Genie Room

Access your configured Genie room:
- The URL is: `https://<your-workspace>.azuredatabricks.net/genie/rooms/<your-genie-space-id>`
- Press **[o]** in the interactive menu to open automatically
- Or check the console output when the script starts



---

## 🛠️ Maintenance

### Update Dependencies
```bash
source venv/bin/activate
pip install --upgrade openai databricks-sdk
```

### Regenerate API Key
1. Get new key: https://platform.openai.com/api-keys
2. Update `.env` file

---

## ✨ That's It!

Simple, clean, and fully automatic. Just run `./start_interactive.sh` and start asking questions!
