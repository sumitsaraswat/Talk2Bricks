#!/usr/bin/env python3
"""
Interactive Voice to Genie - FULLY AUTOMATIC
Questions are automatically sent to Genie via REST API!
"""

import os
import sys
import tempfile
import sounddevice as sd
import scipy.io.wavfile as wav
import numpy as np
import requests
from openai import OpenAI
from dotenv import load_dotenv

# Load environment
load_dotenv()

class AutoGenieVoice:
    def __init__(self):
        self.api_key = os.getenv('OPENAI_API_KEY')
        self.genie_space_id = os.getenv('GENIE_SPACE_ID')
        self.databricks_host = os.getenv('DATABRICKS_HOST', 'https://your-workspace.azuredatabricks.net')
        
        if not self.api_key:
            print("❌ OPENAI_API_KEY not found in .env file")
            sys.exit(1)
        
        if not self.genie_space_id:
            print("❌ GENIE_SPACE_ID not found in .env file")
            sys.exit(1)
        
        # Get Databricks token
        self.databricks_token = self.get_databricks_token()
        if not self.databricks_token:
            print("❌ Could not find Databricks token in ~/.databrickscfg")
            sys.exit(1)
        
        self.openai_client = OpenAI(api_key=self.api_key)
        self.sample_rate = 16000
        
        self.print_header()
    
    def get_databricks_token(self):
        """Read Databricks token from ~/.databrickscfg"""
        try:
            with open(os.path.expanduser('~/.databrickscfg'), 'r') as f:
                for line in f:
                    if 'token' in line.lower():
                        parts = line.split('=')
                        if len(parts) > 1:
                            return parts[1].strip()
        except:
            pass
        return None
    
    def print_header(self):
        print("\n" + "=" * 70)
        print("🎤 Interactive Voice to Genie - FULLY AUTOMATIC!")
        print("=" * 70)
        print("\n✅ Ready:")
        print(f"   • OpenAI Whisper: Connected")
        print(f"   • Databricks: {self.databricks_host}")
        print(f"   • Genie Space: {self.genie_space_id}")
        print(f"   • Auto-send: ENABLED ✨")
        print("\n💡 Workflow: Speak → Transcribe → Auto-send to Genie → Done!")
        print("=" * 70)
    
    def record_audio(self, duration=5):
        """Record audio from microphone"""
        print(f"\n🎤 Recording for {duration} seconds...")
        print("   💬 Speak your question now!\n")
        
        # Countdown
        for i in range(3, 0, -1):
            print(f"   {i}...")
            import time
            time.sleep(0.8)
        
        print("   🔴 RECORDING!\n")
        
        try:
            recording = sd.rec(
                int(duration * self.sample_rate),
                samplerate=self.sample_rate,
                channels=1,
                dtype=np.int16
            )
            sd.wait()
            print("   ✅ Recording complete!\n")
            return recording
        except Exception as e:
            print(f"   ❌ Recording error: {e}")
            return None
    
    def transcribe(self, recording):
        """Transcribe audio with Whisper"""
        print("🔄 Transcribing with Whisper...\n")
        
        try:
            with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as f:
                temp_path = f.name
                wav.write(temp_path, self.sample_rate, recording)
            
            with open(temp_path, 'rb') as audio_file:
                transcript = self.openai_client.audio.transcriptions.create(
                    model='whisper-1',
                    file=audio_file,
                    language='en'
                )
            
            os.unlink(temp_path)
            return transcript.text
        except Exception as e:
            print(f"❌ Transcription error: {e}")
            return None
    
    def send_to_genie(self, question):
        """Send question to Genie using REST API"""
        print("🤖 Sending to Genie...\n")
        
        url = f"{self.databricks_host}/api/2.0/genie/spaces/{self.genie_space_id}/start-conversation"
        
        headers = {
            "Authorization": f"Bearer {self.databricks_token}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "content": question
        }
        
        try:
            response = requests.post(url, json=payload, headers=headers, timeout=10)
            
            if response.status_code == 200:
                print("✅ SUCCESS! Question sent to Genie!")
                return True
            else:
                print(f"⚠️  API returned status {response.status_code}")
                print(f"   Response: {response.text[:200]}")
                return False
                
        except Exception as e:
            print(f"⚠️  Error sending to Genie: {e}")
            return False
    
    def run_interactive(self):
        """Main interactive loop"""
        
        while True:
            print("\n" + "-" * 70)
            print("\n🎙️  Ready to record!")
            print("\nOptions:")
            print("  [1] Quick question (5 seconds)")
            print("  [2] Medium question (10 seconds)")
            print("  [3] Long question (15 seconds)")
            print("  [4] Custom duration")
            print("  [o] Open Genie room in browser")
            print("  [q] Quit")
            
            choice = input("\n👉 Choose: ").strip().lower()
            
            if choice == 'q':
                print("\n👋 Goodbye!\n")
                break
            
            if choice == 'o':
                genie_url = f"{self.databricks_host}/genie/rooms/{self.genie_space_id}"
                import subprocess
                try:
                    subprocess.run(['open', genie_url], check=True)
                    print(f"\n✅ Opened Genie room in browser!")
                except:
                    print(f"\n⚠️  Visit: {genie_url}")
                continue
            
            # Get duration
            if choice == '1':
                duration = 5
            elif choice == '2':
                duration = 10
            elif choice == '3':
                duration = 15
            elif choice == '4':
                try:
                    duration = int(input("Enter duration (1-30 seconds): "))
                    duration = max(1, min(30, duration))
                except:
                    print("Invalid duration, using 5 seconds")
                    duration = 5
            else:
                print("❌ Invalid choice")
                continue
            
            # Record and transcribe
            print("\n" + "=" * 70)
            recording = self.record_audio(duration)
            
            if recording is None:
                continue
            
            text = self.transcribe(recording)
            
            if text:
                print("=" * 70)
                print("📝 YOUR QUESTION:")
                print("=" * 70)
                print(f"\n   \"{text}\"\n")
                print("=" * 70)
                
                # Automatically send to Genie
                if self.send_to_genie(text):
                    print("\n" + "=" * 70)
                    print("🎉 COMPLETE!")
                    print("=" * 70)
                    print("\n✨ Your question has been sent to Genie!")
                    print(f"📊 Check your Genie room for the answer:")
                    print(f"   {self.databricks_host}/genie/rooms/{self.genie_space_id}")
                    print("\n🤖 Genie is processing your question now...")
                    print("=" * 70)
                else:
                    print("\n⚠️  Could not auto-send. Question shown above for manual entry.")
                
                print("\n✨ Ready for next question!")


if __name__ == "__main__":
    print("\n🎙️  Starting Fully Automatic Voice to Genie...")
    
    try:
        app = AutoGenieVoice()
        app.run_interactive()
    except KeyboardInterrupt:
        print("\n\n👋 Interrupted. Goodbye!\n")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


