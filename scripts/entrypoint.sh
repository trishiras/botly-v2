#!/bin/bash

# Start Ollama server in the background
ollama serve &
OLLAMA_PID=$!

# Wait for Ollama to be ready
/usr/src/app/scripts/wait-for-it.sh

# Pull the model
ollama pull qwen2.5:1.5b

# Wait for Ollama server to complete (if needed)
wait $OLLAMA_PID &

# Start Open WebUI
python3 /usr/src/app/botly.py