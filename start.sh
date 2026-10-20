#!/bin/bash

# Start FastAPI backend in the background
uvicorn main:app --host 0.0.0.0 --port 8000 &

# Start Streamlit frontend on Render's dynamic PORT (default 10000)
streamlit run app.py --server.port=${PORT:-10000} --server.address=0.0.0.0