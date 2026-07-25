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

**News Bot** is a sophisticated, AI-driven automation tool designed to curb information overload. It autonomously scrapes high-value RSS feeds—ranging from International Law and Global Politics to Frontier Tech—and synthesizes them into two premium outputs each morning:
1.  A **Visual PDF Newspaper** ("The Morning Edition") for offline reading.
2.  A **Slack Digest** for quick team synchronization.

By leveraging **LLMs (Large Language Models)** and advanced filtering logic, it separates signal from noise, delivering deep, research-grade analysis rather than just headlines.

## <a name="features"></a>✨ Features

| Feature | Description |
|:---:|:---|
| **📄 PDF Newspaper** | Automatically generates a professionally styled `"Morning Edition"` PDF with headlines, summaries, and "Concept of the Day". |
| **🤖 AI-Curation** | Uses **Artificial Intelligence** to generate dense, analytical (3-paragraph) executive summaries of complex topics. |
| **🎓 Learning Engine** | Dynamically serves a daily **Legal/Political Concept** (e.g., *Stare Decisis, Realpolitik*) from a curated knowledge base. |
| **🌍 Global Scope** | Monitors high-impact sources including *Foreign Policy, Reuters, Dawn, Jurist, and TechCrunch*. |
| **⚖️ specialized Intelligence** | Dedicated modules for **International Law**, **International Relations**, and **National Security**. |
| **📅 Automated Delivery** | Runs automatically at **12:00 PM** (configurable) via Github Actions or local cron. |

## <a name="architecture"></a>🛠️ Architecture

The system operates on an enhanced ETL pipeline reinforced by AI agents and a document generation layer.

```mermaid
graph TD
    A["⏰ Scheduler (12:00 PM)"] -->|Trigger| B("🚀 Main Process")
    
    subgraph "Data Ingestion"
        B -->|Fetch| C{"RSS Feeds"}
        B -->|Load| L["Legal Tips DB 📚"]
        C -->|Law| D["Raw Data"]
        C -->|Politics| D
    end
    
    subgraph "Intelligence Layer"
        D -->|Filter| E["Analyst Agent 🕵️"]
        E -->|Summarize & Expand| F["AI Content Engine 🧠"]
        F -->|Generate| G["Full Report"]
    end
    
    subgraph "Production"
        G -->|Layout| P["PDF Generator 📄"]
        P -->|Create| PDF["Morning_Edition.pdf"]
        G -->|Format| S["Slack Composer 💬"]
    end
    
    subgraph "Delivery"
        S -->|Push| Slack(("Slack Channel"))
        PDF -->|Upload| Slack
    end
```

## 📂 Project Structure

```bash
📦 news_bot
├── 📂 .github
│   └── 📂 workflows
│       └── daily_digest.yml   # 🤖 GitHub Actions Automation
├── 📂 data                    # 💾 Local storage (Legal Tips, PDF cache)
│   ├── legal_tips.json        # 🎓 Source for "Concept of the Day"
│   └── *.pdf                  # 📄 Generated newspapers
├── 📂 modules                 # 🧠 Core Logic
│   ├── ai_handler.py          # LLM Integration (Mistral API)
│   ├── learning_engine.py     # Educational Content Manager
│   ├── news_fetcher.py        # RSS Parsing & Filtering
│   ├── pdf_generator.py       # FPDF2 Newspaper Layout Engine
│   ├── slack_bot.py           # Slack API Client (Block Kit)
│   └── ...
├── config.py                  # ⚙️ Configuration & Feed Lists
├── main.py                    # 🚀 Scheduler Entry Point
├── run_now.py                 # ⚡ Manual Trigger Script
└── requirements.txt           # 📦 Dependencies
```

## <a name="installation"></a>⚡ Installation

### Prerequisites
- **Python 3.9+**
- A **Slack Workspace** with permissions to create Apps.
- (Optional) **Mistral API Key** for AI summarization.

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
SLACK_APP_TOKEN=xapp-your-app-token # (Optional, depending on socket mode)
SLACK_CHANNEL_ID=C12345678
MISTRAL_API_KEY=your-llm-api-key 
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

### 🚀 Manual Trigger (Instant Run)
To run the full pipeline immediately (bypass scheduler):
```bash
python run_now.py
```
*This will fetch news, generate the PDF, and send it to Slack instantly.*

### ⏰ Scheduler Mode
To start the bot in background mode (waiting for 12:00 PM):
```bash
python main.py
```

### ☁️ Run via GitHub Actions
This repository includes a pre-configured workflow in `.github/workflows/daily_digest.yml`.

1. Go to your repo **Settings** > **Secrets and variables** > **Actions**.
2. Add the following Repository Secrets:
   - `SLACK_BOT_TOKEN`
   - `SLACK_CHANNEL_ID`
   - `MISTRAL_API_KEY`
3. The workflow runs automatically at **07:00 UTC** (12:00 PM Pakistan Time).


