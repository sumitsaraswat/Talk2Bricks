# 🔄 Complete Request Flow - Voice to Databricks Genie

## Visual Flow Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│  1. USER RUNS SCRIPT                                            │
│     $ ./start_interactive.sh                                    │
└──────────────────┬──────────────────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────────────────┐
│  2. SCRIPT INITIALIZATION (Lines 20-43)                         │
│     • Loads .env file                                           │
│     • Reads OPENAI_API_KEY                                      │
│     • Reads GENIE_SPACE_ID                                      │
│     • Reads ~/.databrickscfg for Databricks token              │
│     • Creates OpenAI client                                     │
│     • Prints header "Ready"                                     │
└──────────────────┬──────────────────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────────────────┐
│  3. INTERACTIVE LOOP STARTS (Line 149)                          │
│     • Shows menu: [1] 5 sec, [2] 10 sec, [3] 15 sec           │
│     • Waits for user input                                      │
└──────────────────┬──────────────────────────────────────────────┘
                   │
                   ▼ (User presses 1)
┌─────────────────────────────────────────────────────────────────┐
│  4. AUDIO RECORDING (Lines 70-95)                               │
│                                                                  │
│     4a. COUNTDOWN                                               │
│         • Prints "3... 2... 1... RECORDING!"                   │
│         • Uses time.sleep() for pauses                          │
│                                                                  │
│     4b. MICROPHONE CAPTURE (Line 84-89)                        │
│         • sounddevice.rec() accesses Mac microphone             │
│         • Records at 16000 Hz sample rate                       │
│         • Captures mono audio (1 channel)                       │
│         • Stores as numpy array (int16 format)                  │
│         • Records for 5 seconds                                 │
│         • sd.wait() blocks until recording complete             │
│                                                                  │
│     4c. RETURNS: numpy array with audio data                    │
└──────────────────┬──────────────────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────────────────┐
│  5. AUDIO PROCESSING (Lines 97-117)                             │
│                                                                  │
│     5a. SAVE TO TEMP FILE (Lines 102-104)                      │
│         • Creates temporary file: /tmp/tmpXXXXXX.wav            │
│         • Writes numpy array as WAV file                        │
│         • Uses scipy.io.wavfile.write()                         │
│                                                                  │
│     5b. PREPARE FOR API (Line 106)                             │
│         • Opens WAV file in binary read mode                    │
│         • File ready for upload to OpenAI                       │
└──────────────────┬──────────────────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────────────────┐
│  6. WHISPER API CALL (Lines 107-111)                            │
│                                                                  │
│     YOUR MAC                                                     │
│         ↓ HTTPS POST                                            │
│     [Audio File (WAV)]                                          │
│         ↓                                                        │
│     ════════════════════════════════════════                    │
│         ↓                                                        │
│     OPENAI WHISPER API                                          │
│     (api.openai.com)                                            │
│         • Receives WAV file                                     │
│         • Runs Whisper-1 model                                  │
│         • Converts speech to text                               │
│         • Processes in ~2-3 seconds                             │
│         ↓                                                        │
│     Returns JSON: {"text": "Show me all catalogs"}             │
│         ↓                                                        │
│     ════════════════════════════════════════                    │
│         ↓                                                        │
│     YOUR MAC                                                     │
│     • Receives transcribed text                                 │
│     • Deletes temp WAV file                                     │
│     • Returns text string                                       │
└──────────────────┬──────────────────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────────────────┐
│  7. DISPLAY TRANSCRIPTION (Lines 206-211)                       │
│     • Prints: "📝 YOUR QUESTION: Show me all catalogs"         │
└──────────────────┬──────────────────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────────────────┐
│  8. SEND TO GENIE (Lines 119-147)                               │
│                                                                  │
│     8a. BUILD REQUEST (Lines 123-132)                          │
│         • URL: databricks.net/api/2.0/genie/spaces/ID/...      │
│         • Headers:                                              │
│           - Authorization: Bearer <databricks_token>            │
│           - Content-Type: application/json                      │
│         • Payload:                                              │
│           {"content": "Show me all catalogs"}                   │
│                                                                  │
│     8b. HTTP POST REQUEST (Line 135)                           │
│         YOUR MAC                                                 │
│             ↓ HTTPS POST                                        │
│         [JSON Payload]                                          │
│             ↓                                                    │
│         ════════════════════════════════════════                │
│             ↓                                                    │
│         DATABRICKS API                                          │
│         (<your-workspace>.azuredatabricks.net)                 │
│             • Validates Bearer token                            │
│             • Checks Genie space permissions                    │
│             • Routes to Genie service                           │
│             ↓                                                    │
│         DATABRICKS GENIE                                        │
│             • Receives question                                 │
│             • Creates new conversation message                  │
│             • Starts AI processing                              │
│             • Returns HTTP 200 OK                               │
│             ↓                                                    │
│         ════════════════════════════════════════                │
│             ↓                                                    │
│         YOUR MAC                                                 │
│             • Receives 200 response                             │
│             • Prints "✅ SUCCESS!"                              │
└──────────────────┬──────────────────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────────────────┐
│  9. COMPLETE (Lines 215-222)                                    │
│     • Prints success message                                    │
│     • Shows Genie room URL                                      │
│     • Returns to menu                                           │
└──────────────────┬──────────────────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────────────────┐
│  10. GENIE PROCESSES (In Databricks)                            │
│      • Genie analyzes question                                  │
│      • Generates SQL queries                                    │
│      • Runs queries on your data                                │
│      • Creates visualizations                                   │
│      • Prepares natural language response                       │
│      • Updates Genie room UI                                    │
└─────────────────────────────────────────────────────────────────┘
```

---

## Detailed Step-by-Step Breakdown

### 🚀 STEP 1: Script Startup
**File:** `start_interactive.sh`
```bash
cd /Users/sumit.saraswat/Documents/whisper
source venv/bin/activate
python interactive_voice_auto.py
```

**What happens:**
- Changes to project directory
- Activates Python virtual environment
- Runs main Python script

---

### 🔧 STEP 2: Initialization (Lines 20-43)

**What loads:**
```python
# Load environment variables
load_dotenv()  # Reads .env file

# Get credentials
self.api_key = os.getenv('OPENAI_API_KEY')           # Your OpenAI key
self.genie_space_id = os.getenv('GENIE_SPACE_ID')    # Your Genie room ID
self.databricks_token = self.get_databricks_token()  # From ~/.databrickscfg
```

**Where data comes from:**
- `.env` file → OpenAI API key & Genie Space ID
- `~/.databrickscfg` → Databricks authentication token

**What's created:**
```python
self.openai_client = OpenAI(api_key=self.api_key)  # OpenAI SDK client
self.sample_rate = 16000                           # Audio sample rate (Hz)
```

---

### 🎙️ STEP 3: User Selects Duration (Line 163)

**User interaction:**
```
Options:
  [1] Quick question (5 seconds)
  [2] Medium question (10 seconds)
  [3] Long question (15 seconds)

👉 Choose: 1
```

**Processing:**
```python
choice = input("\n👉 Choose: ").strip().lower()
if choice == '1':
    duration = 5  # Sets recording duration to 5 seconds
```

---

### 🎤 STEP 4: Audio Recording (Lines 70-95)

**4a. Countdown:**
```python
for i in range(3, 0, -1):
    print(f"   {i}...")
    time.sleep(0.8)  # Waits 0.8 seconds between counts
```
Output: `3... 2... 1... RECORDING!`

**4b. Microphone Capture:**
```python
recording = sd.rec(
    int(duration * self.sample_rate),  # 5 * 16000 = 80,000 samples
    samplerate=self.sample_rate,       # 16,000 Hz (CD quality)
    channels=1,                        # Mono audio
    dtype=np.int16                     # 16-bit integer format
)
sd.wait()  # Blocks until recording complete
```

**What happens under the hood:**
- `sounddevice` library accesses macOS Core Audio framework
- Your Mac's microphone is accessed (built-in or external)
- Audio is sampled 16,000 times per second
- Each sample is stored as a 16-bit integer
- For 5 seconds: 80,000 samples = ~160KB of data
- Returns numpy array: `[sample1, sample2, ..., sample80000]`

---

### 💾 STEP 5: Save to Temp File (Lines 102-104)

**File creation:**
```python
with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as f:
    temp_path = f.name  # e.g., /tmp/tmp8k3j2h1s.wav
    wav.write(temp_path, self.sample_rate, recording)
```

**What's written:**
- WAV file format (uncompressed)
- Header: sample rate, channels, bit depth
- Data: raw audio samples
- Size: ~160KB for 5 seconds

**Why needed:**
- OpenAI API requires file upload
- Can't send numpy array directly
- WAV is universal audio format

---

### 🌐 STEP 6: Whisper API Call (Lines 107-111)

**The API request:**
```python
with open(temp_path, 'rb') as audio_file:
    transcript = self.openai_client.audio.transcriptions.create(
        model='whisper-1',
        file=audio_file,
        language='en'
    )
```

**Under the hood (OpenAI SDK):**
```
1. Opens WAV file in binary mode
2. Creates multipart/form-data HTTP request
3. Builds request:
   POST https://api.openai.com/v1/audio/transcriptions
   Headers:
     Authorization: Bearer sk-proj-1NHz...
     Content-Type: multipart/form-data
   Body:
     model: whisper-1
     file: [binary WAV data]
     language: en

4. Sends HTTPS request to OpenAI
5. OpenAI receives and validates
6. Whisper model processes audio (2-3 seconds)
7. Returns JSON response:
   {
     "text": "Show me all catalogs"
   }

8. SDK parses JSON
9. Returns transcript object
```

**Network details:**
- Protocol: HTTPS (encrypted)
- Method: POST
- Endpoint: api.openai.com
- Upload size: ~160KB
- Download size: ~100 bytes
- Latency: 2-3 seconds

---

### 📝 STEP 7: Display Result (Lines 206-211)

**Simple display:**
```python
text = transcript.text  # "Show me all catalogs"
print(f"\n   \"{text}\"\n")
```

**Cleanup:**
```python
os.unlink(temp_path)  # Deletes /tmp/tmp8k3j2h1s.wav
```

---

### 🚀 STEP 8: Send to Genie (Lines 119-147)

**8a. Build Request:**
```python
url = f"{self.databricks_host}/api/2.0/genie/spaces/{self.genie_space_id}/start-conversation"
# https://<your-workspace>.azuredatabricks.net/api/2.0/genie/spaces/<genie-space-id>/start-conversation

headers = {
    "Authorization": f"Bearer {self.databricks_token}",  # dapic558037...
    "Content-Type": "application/json"
}

payload = {
    "content": "Show me all catalogs"
}
```

**8b. HTTP Request:**
```python
response = requests.post(url, json=payload, headers=headers, timeout=10)
```

**Network details:**
```
POST /api/2.0/genie/spaces/<genie-space-id>/start-conversation
Host: <your-workspace>.azuredatabricks.net
Authorization: Bearer <your-databricks-token>
Content-Type: application/json

{"content": "Show me all catalogs"}
```

**What Databricks does:**
1. **Authentication Layer:**
   - Receives request
   - Validates Bearer token
   - Checks user permissions
   - Verifies Genie space access

2. **API Gateway:**
   - Routes to Genie service
   - Logs request
   - Rate limiting checks

3. **Genie Service:**
   - Creates conversation message
   - Queues for AI processing
   - Returns 200 OK immediately
   - Processes asynchronously

4. **Response:**
```json
HTTP/1.1 200 OK
Content-Type: application/json

{
  "message_id": "msg_abc123...",
  "status": "pending"
}
```

---

### 🤖 STEP 9: Genie Processing (Asynchronous in Databricks)

**Happens in background after API returns:**

```
1. Genie AI analyzes question
   • Natural language understanding
   • Intent detection: "User wants to list catalogs"
   • Entity extraction: None needed

2. Query Generation
   • Determines: Need to call Unity Catalog API
   • Generates: SHOW CATALOGS or equivalent API call

3. Query Execution
   • Runs on Databricks SQL warehouse
   • Retrieves list of all catalogs
   • Gets metadata (owner, creation date, etc.)

4. Result Formatting
   • Creates table view
   • Generates charts if applicable
   • Prepares natural language response

5. Update UI
   • Writes to Genie conversation
   • Updates Genie room in real-time
   • Notifies user (if browser open)
```

---

### 🔄 STEP 10: Loop Back (Line 226)

```python
print("\n✨ Ready for next question!")
# Returns to step 3 (menu)
```

---

## Key Components & Libraries

### Audio Processing
- **sounddevice**: Accesses macOS microphone
- **numpy**: Stores audio as numerical array
- **scipy**: Writes WAV file format

### API Communication
- **openai SDK**: Handles Whisper API calls
- **requests**: Handles Databricks REST API calls
- **dotenv**: Loads environment variables

### System Integration
- **tempfile**: Creates temporary WAV files
- **os**: File operations, environment variables
- **subprocess**: Opens browser (optional)

---

## Data Flow Summary

```
Sound Waves (Your Voice)
    ↓
Mac Microphone (Hardware)
    ↓
sounddevice Library (Captures)
    ↓
Numpy Array [80,000 samples]
    ↓
WAV File (/tmp/tmpXXXX.wav)
    ↓
OpenAI Whisper API (HTTPS POST)
    ↓
Transcribed Text String
    ↓
Databricks Genie API (HTTPS POST)
    ↓
Genie Conversation Message
    ↓
AI Processing & Query Execution
    ↓
Results in Genie Room
```

---

## Network Requests

### Request 1: To OpenAI
```
Source: Your Mac (192.168.x.x)
Destination: api.openai.com (13.107.x.x)
Protocol: HTTPS (TLS 1.3)
Port: 443
Method: POST
Endpoint: /v1/audio/transcriptions
Upload: 160KB (WAV file)
Download: ~100 bytes (JSON)
Time: 2-3 seconds
Cost: ~$0.001
```

### Request 2: To Databricks
```
Source: Your Mac (192.168.x.x)
Destination: <your-workspace>.azuredatabricks.net
Protocol: HTTPS (TLS 1.3)
Port: 443
Method: POST
Endpoint: /api/2.0/genie/spaces/.../start-conversation
Upload: ~50 bytes (JSON)
Download: ~200 bytes (JSON)
Time: 200-500ms
Cost: Free (included in Databricks)
```

---

## Timing Breakdown

```
User presses [1]           : 0.0s
Countdown (3...2...1)      : 2.4s (3 × 0.8s)
Recording                  : 5.0s
Save to WAV                : 0.1s
Upload to OpenAI           : 0.5s
Whisper processing         : 2.5s
Download transcript        : 0.1s
Display text               : 0.1s
Send to Databricks         : 0.3s
Display success            : 0.1s
─────────────────────────────────
TOTAL                      : ~11 seconds
```

---

## Error Handling

### If microphone fails:
```python
except Exception as e:
    print(f"❌ Recording error: {e}")
    return None
```
→ Returns to menu

### If Whisper API fails:
```python
except Exception as e:
    print(f"❌ Transcription error: {e}")
    return None
```
→ Shows error, returns to menu

### If Genie API fails:
```python
if response.status_code != 200:
    print(f"⚠️ API returned status {response.status_code}")
    return False
```
→ Shows transcribed text for manual copy/paste

---

## Security Flow

### Authentication Chain:
```
1. .env file (local)
   → OPENAI_API_KEY (encrypted in transit via HTTPS)
   
2. ~/.databrickscfg (local)
   → DATABRICKS_TOKEN (encrypted in transit via HTTPS)

3. Both tokens validated server-side
   → OpenAI: checks quota, permissions
   → Databricks: checks user access, Genie space permissions
```

### Data Privacy:
- Audio never stored permanently
- Temp files deleted after use
- All transmissions encrypted (HTTPS)
- OpenAI processes audio, doesn't store it permanently
- Databricks stores only the text question

---

This is the complete request flow from start to finish! 🎤✨


