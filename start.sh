#!/bin/bash
# Script de inicialização para Render (alternativa ao Dockerfile)
# Use este script se preferir usar buildpacks ao invés de Docker

streamlit run app.py --server.port=$PORT --server.address=0.0.0.0

