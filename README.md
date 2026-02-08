<div align="center">

# 🤖 News Bot
### Intelligent Daily News & Legal Intelligence Aggregator

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Slack](https://img.shields.io/badge/Slack-API-4A154B?style=for-the-badge&logo=slack&logoColor=white)](https://api.slack.com/)
[![Status](https://img.shields.io/badge/Status-Active-success?style=for-the-badge)]()

*Empowering your day with curated intelligence, filtered by AI, delivered to Slack.*

[Features](#features) • [Architecture](#architecture) • [Installation](#installation) • [Configuration](#configuration) • [Usage](#usage)

</div>

---

## 🚀 Overview

**News Bot** is a sophisticated, AI-driven automation tool designed to curb information overload. It autonomously scrapes high-value RSS feeds—ranging from International Law and Global Politics to Frontier Tech—and synthesizes them into a crisp, readable daily digest.

By leveraging **LLMs (Large Language Models)** and advanced filtering logic, it separates signal from noise, delivering only what matters to your Slack workspace every single day.

## <a name="features"></a>✨ Features

| Feature | Description |
|:---:|:---|
| **🤖 AI-Curation** | Intelligent filtering and summarization using advanced NLP to prioritize high-impact stories. |
| **🌍 Global Scope** | Monitors 20+ sources including *Foreign Policy, Reuters, Dawn, Jurist, and TechCrunch*. |
| **⚖️ specialized Intelligence** | Dedicated modules for **International Law** and **International Relations**. |

| **📅 Cron Scheduling** | Runs automatically at **12:00 PM** (configurable) to match your morning routine. |
| **💬 Beautiful Output** | Formatted Slack messages with blocks, dividers, and emojis for superior readability. |

## <a name="architecture"></a>🛠️ Architecture

The system operates on a linear extraction-transformation-load (ETL) pipeline reinforced by AI agents.

```mermaid
graph TD
    A["⏰ Scheduler (12:00 PM)"] -->|Trigger| B("🚀 Main Process")
    subgraph "Data Ingestion"
        B -->|Fetch| C{"RSS Feeds"}
        C -->|Law| D["Raw Data"]
        C -->|Politics| D
        C -->|Tech| D
    end
    subgraph "Intelligence Layer"
        D -->|Filter| E["Analyst Agent 🕵️"]
        E -->|Summarize| F["Content Engine 🧠"]
    end
    subgraph "Delivery"
        F -->|Format| H["Slack Client 💬"]
        H -->|Push| I(("Your Slack Channel"))
    end
```

## 📂 Project Structure

```bash
📦 news_bot
├── 📂 .github
│   └── 📂 workflows
│       └── daily_digest.yml   # 🤖 GitHub Actions Automation
├── 📂 data                    # 💾 Local storage for state/cache
├── 📂 modules                 # 🧠 Core Logic
│   ├── ai_handler.py          # LLM Integration
│   ├── analyst.py             # Content Filtering
│   ├── news_fetcher.py        # RSS Parsing
│   ├── slack_bot.py           # Slack API Client
│   └── ...
├── config.py                  # ⚙️ Configuration & Feed Lists
├── main.py                    # 🚀 Entry Point
└── requirements.txt           # 📦 Dependencies
```

## <a name="installation"></a>⚡ Installation

### Prerequisites
- **Python 3.9+**
- A **Slack Workspace** with permissions to create Apps.

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/news_bot.git
cd news_bot
```

### 2. Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

## <a name="configuration"></a>⚙️ Configuration

1. Create a `.env` file in the root directory:
```bash
touch .env
```

2. Add your secrets:
```ini
# .env
SLACK_BOT_TOKEN=xoxb-your-bot-token
SLACK_CHANNEL_ID=C12345678  # Channel ID where messages will be sent
BYTEZ_API_KEY=your-llm-api-key # Optional: If using external LLM services
```

3. **Customize Feeds**:
   Open `config.py` to edit your source lists.
   ```python
   RSS_FEEDS = {
       "⚖️ International Law": [ ... ],
       "💻 Tech": [ ... ]
   }
   ```

## <a name="usage"></a>🕹️ Usage

### Run Manually
To test the bot immediately:
```bash
python main.py
```
*The bot will start the scheduler. To force a run instantly, check `run_now.py` (if available) or modify the schedule.*

### Run via GitHub Actions ☁️
This repository includes a pre-configured workflow in `.github/workflows/daily_digest.yml`.

1. Go to your repo **Settings** > **Secrets and variables** > **Actions**.
2. Add the following Repository Secrets:
   - `SLACK_BOT_TOKEN`
   - `SLACK_CHANNEL_ID`
   - `BYTEZ_API_KEY`
3. The workflow runs automatically at **07:00 UTC** (12:00 PM Pakistan Time).



<div align="center">

Made with ❤️ and ☕ by **Muhammad Anas Rehman**

Created with the help of **Google Antigravity**

</div>
