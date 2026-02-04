#!/bin/bash

# Start Ollama in the background
ollama serve &

# Wait for Ollama to start, then pull the model
sleep 5
ollama pull llama3.2:1b

# Start the FastAPI backend
python -m uvicorn app.main:app --host 0.0.0.0 --port 8020 &

# Start the Streamlit frontend
streamlit run ui/app.py --server.port 7860 --server.address 0.0.0.0