---
title: Visual Analyst Agent
emoji: 🚀
colorFrom: red
colorTo: red
sdk: docker
app_port: 8501
tags:
- streamlit
pinned: false
short_description: Upload any chart, table or dashboard , get instant Analysis
license: mit
---

# Visual Analyst Agent

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Gemini](https://img.shields.io/badge/Google-Gemini%202.5%20Flash-4285F4?logo=google&logoColor=white)](https://ai.google.dev/)
[![Plotly](https://img.shields.io/badge/Plotly-Interactive%20Charts-3F4F75?logo=plotly&logoColor=white)](https://plotly.com/python/)

Visual Analyst Agent is an AI-powered Streamlit application that analyzes uploaded chart, table, and dashboard images, identifies the visual type, extracts structured data, produces plain-English business insights, redraws an interactive visualization, supports follow-up Q&A on the same image, and generates a shareable HTML report.

## Features

- Visual type detection
- Data extraction
- Trend analysis
- Redrawn interactive chart
- Follow-up chat
- HTML export

## Tech Stack

- Python
- Streamlit
- Google Gemini 2.5 Flash
- Plotly
- Pandas
- Pillow

## How to Run Locally

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Start the app:

```bash
streamlit run app.py
```

## How It Works

The project follows a focused 5-file architecture with clear responsibilities:

- `analyzer.py`: Sends image + prompt to Gemini and handles analysis/follow-up responses.
- `parser.py`: Parses model output into visual type, structured data, and analysis text.
- `charts.py`: Rebuilds extracted data into a dark-themed interactive Plotly chart.
- `report.py`: Generates a polished standalone HTML report for sharing/export.
- `app.py`: Streamlit UI and orchestration layer that connects upload, analysis, chat, charting, and export.
