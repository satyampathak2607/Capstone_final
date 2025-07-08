#!/bin/bash
cd rag-pdf-ai/app
gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app
