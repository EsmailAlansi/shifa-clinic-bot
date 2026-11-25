# Al-Shifa Clinic AI Assistant 🏥

[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688.svg?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB.svg?logo=python&logoColor=white)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![OpenRouter](https://img.shields.io/badge/OpenRouter-Free%20Tier-6366f1.svg)](https://openrouter.ai/)

An intelligent, context-grounded virtual assistant designed for **Al-Shifa Clinic** in Sana'a. Built using **Python**, **FastAPI**, and **OpenRouter's free-tier LLM models**, the assistant responds directly in Arabic to patients' questions about clinic operating hours, consultation fees, lab tests, radiology, departments, and booking procedures based strictly on the verified clinic knowledge base (`faq.md`).

---

## 🌟 Key Features

- **Professional Interactive Web UI:**
  - Modern, responsive Arabic (`RTL`) interface with mobile-first support.
  - **Light & Dark mode** toggle with persistent smooth transitions.
  - Quick-action buttons for common inquiries (hours, prices, departments, payment).
  - One-click copy for answers and retry mechanisms for network disruptions.
- **Lightweight CLI Interface:**
  - Fast, terminal-based interaction for local experimentation and testing (`bot.py`).
- **Zero Cost (100% Free):**
  - Powered by OpenRouter free routing (`openrouter/free`) with zero API charges.
- **Strict Guardrails & Medical Safety:**
  - Explicit system prompt preventing medical diagnoses, prescriptions, or speculation.
  - Strict grounding: only answers questions present in `faq.md`.
  - Fallback message with phone contact when information is not in the knowledge base.

---

## 🛠️ Architecture & Tech Stack

```text
User Request ──► FastAPI Backend (/api/chat) ──► System Prompt + faq.md Context
                                                           │
                                                           ▼
                                                OpenRouter (openrouter/free)
                                                           │
                                                           ▼
Formatted Response ◄── Chatbot UI / CLI  ◄──────── Answer & Tokens
```

- **Backend:** Python, FastAPI, Uvicorn, Pydantic
- **Frontend:** Vanilla HTML5, CSS3, JavaScript (no bulky node modules or build steps)
- **Model Provider:** OpenRouter API (`openrouter/free`)
- **Knowledge Base:** Plain Markdown (`faq.md`)

---

## 📁 Repository Structure

```text
shifa-clinic-bot/
├── app.py              # FastAPI server & API endpoints
├── bot.py              # Core LLM prompt, context injection, and CLI mode
├── faq.md              # Clinic knowledge base (hours, fees, doctors, policies)
├── results.md          # 5-question test benchmark and evaluation report
├── requirements.txt    # Python package dependencies
├── .env.example        # Environment variable template
└── static/
    └── index.html      # Responsive web chat interface (HTML/CSS/JS)
```

---

## 🚀 Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/EsmailAlansi/shifa-clinic-bot.git
cd shifa-clinic-bot
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure API Key
Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```
Add your free OpenRouter API key inside `.env`:
```env
OPENROUTER_API_KEY=sk-or-v1-your-key-here
```

### 4. Run the Application

* **Option A: Interactive Web UI (Recommended)**
  ```bash
  python app.py
  ```
  Open your browser and navigate to: `http://127.0.0.1:8000`

* **Option B: Command Line (CLI)**
  ```bash
  python bot.py
  ```

---

## 📡 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | Serves the interactive web interface |
| `GET` | `/api/health` | Returns server status and current LLM model |
| `POST` | `/api/chat` | Accepts `{ "question": "..." }` and returns `{ "answer": "...", "model": "..." }` |

---

## 📊 Evaluation & Benchmark

The bot was evaluated against 5 benchmark questions (3 in-context questions and 2 out-of-context edge cases). It achieved a **100% pass rate** without fabricating medical advice or hallucinating clinic services.

See [`results.md`](results.md) for detailed test prompts, outputs, and validation metrics.

---

## 📜 License
This project is open-source under the [MIT License](LICENSE).
