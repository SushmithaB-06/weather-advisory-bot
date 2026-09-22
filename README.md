# Weather Advisory Support Bot

A weather-aware outdoor activity advisory chatbot built using LangGraph, Open-Meteo, Streamlit, and YAML-based SOP rules.

## Overview

The system accepts natural-language outdoor activity questions, retrieves live weather data, matches the conditions against predefined Standard Operating Procedures (SOPs), and returns an advisory.

The workflow is orchestrated using LangGraph.

## Architecture

User
↓
Streamlit Chat Interface
↓
LangGraph Workflow
↓
Intent / Location Extraction
↓
Open-Meteo Weather API
↓
Relevant Weather Period Selection
↓
SOP Matching
↓
Advisory / No-SOP / Error Response

## Main Components

### LangGraph

Controls the application workflow and branching logic.

### Open-Meteo

Provides weather information including:

- Temperature
- Wind speed
- Precipitation
- Weather code
- UV index
- Hourly forecast
- Daily forecast

No API key is required for the Open-Meteo endpoint used by this project.

### SOP Rules

SOPs are stored in:

`sops/sops.yaml`

The policy logic is data-driven, so new SOPs can be added without changing the LangGraph control flow.

### Streamlit

Provides the minimal chat interface for interacting with the bot.

## SOP Matching

The system checks the requested activity and relevant weather conditions against the available SOPs.

If multiple SOPs match, the system resolves the match using severity priority.

If no SOP applies, the system explicitly reports that no applicable SOP was found.

## Session Memory

The chatbot maintains the location and activity from the current chat session.

For example:

User:
"Can I go running in Bangalore today?"

Follow-up:
"What about this evening?"

The second question can reuse the location and activity from the previous message.

## Project Structure

```text
weather-advisory-bot/
├── backend/
│   ├── graph.py
│   ├── state.py
│   ├── nodes/
│   └── services/
├── frontend/
│   └── app.py
├── sops/
│   └── sops.yaml
├── requirements.txt
├── README.md
├── .env.example
└── .gitignore