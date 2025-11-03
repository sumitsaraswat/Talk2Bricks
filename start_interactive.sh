#!/bin/bash
# Launcher for FULLY AUTOMATIC voice-to-Genie interface

cd /Users/sumit.saraswat/Documents/whisper
source venv/bin/activate

clear
echo "🎤 Starting FULLY AUTOMATIC Voice to Genie..."
echo "   Questions will be sent automatically - NO copy/paste needed!"
echo ""

python interactive_voice_auto.py
