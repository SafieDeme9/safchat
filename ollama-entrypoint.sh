#!/bin/bash

# Start Ollama in background
ollama serve &

# Wait for Ollama to be ready
echo "⏳ Waiting for Ollama to start..."
for i in $(seq 1 60); do
    if ollama list &>/dev/null; then
        echo "✅ Ollama is ready!"
        break
    fi
    sleep 5
done

# Pull the model (only if not already present)
# qwen2.5:0.5b = ultra-lightweight, ~400MB, works great on RPi 4
MODEL="${OLLAMA_MODEL:-qwen2.5:0.5b}"
echo "📦 Using model: $MODEL"
if ! ollama list | grep -q "$MODEL"; then
    echo "📥 Pulling $MODEL (this may take a few minutes on first run)..."
    ollama pull "$MODEL"
    echo "✅ Model $MODEL pulled!"
fi

# Keep container running
wait
