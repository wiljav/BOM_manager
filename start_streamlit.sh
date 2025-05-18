#!/bin/sh
set -e

# Use environment variables
STREAMLIT_PORT=${STREAMLIT_SERVER_PORT} #:-8501
STREAMLIT_ADDR=${STREAMLIT_SERVER_ADDRESS} #:-0.0.0.0

streamlit run app/main.py \
    --server.port $STREAMLIT_PORT \
    --server.address $STREAMLIT_ADDR