#!/usr/bin/env bash
cd "$(dirname "$0")"
export STREAMLIT_CONFIG_DIR="$PWD/.streamlit"
"$PWD/venv/bin/streamlit" run app/app.py