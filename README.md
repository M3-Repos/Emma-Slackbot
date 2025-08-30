# Slackbot

A Slack bot that integrates with Ollama for AI-powered responses.

## Status

This is a work in progress.

## Overview

This bot responds to Slack messages and app mentions by forwarding them to an Ollama instance running the `emma-assistant:latest` model.

## Features

- Responds to direct "hello" messages
- Handles app mentions (@bot) with AI-generated responses
- Uses Socket Mode for real-time communication

## Requirements

- Python 3.x
- Slack Bot Token
- Socket Mode Token
- Ollama running locally with emma-assistant model

## Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Create `.env` file with your Slack tokens
3. Ensure Ollama is running with the emma-assistant model
4. Run: `python main.py`

## Environment Variables

- `SLACK_BOT_TOKEN`: Your Slack bot token
- `SOCKET_MODE_TOKEN`: Your Slack socket mode token
