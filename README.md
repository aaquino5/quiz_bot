# SASE Questions CLI & Telegram Bot

Welcome, traveler of the Cloud-Security realms!
This project equips you with two heroic tools to train your knowledge about **SASE (Secure Access Service Edge)**, built with passion, Python, and the stubborn refusal to accept mediocrity.

---

### Project Overview

This project contains:

- CLI Quiz App (`cli_quiz.py`)
- Telegram Bot (`Telegram_Bot_Sample.py`)
- Quiz Dataset (`questions.json`) - based on public FortiSASE documentation.

Both tools allow users to:

- Answer randomized multiple-choice SASE questions
- Receive detailed explanations and source links for learning reinforcement
- Practice SASE concepts like Zero Trust, SD-WAN, FWaaS, and more

########### Key Principle: This is a study companion, not a "shortcut." No leaks. No dumps. Just pure, clean learning. ###########

---

## Features

### CLI Version (`cli_quiz.py`)

- Random question selection
- Final score display
- Detailed explanations after each question

### Telegram Bot Version (`Telegram_Bot_Sample.py`)


- Commands: `/start`, `/quiz`
- Inline multiple-choice answer buttons
- Real-time feedback after each question
- Explanations and reference links provided
- Tracks how many questions the user requested

########### Files Structure ###########

```bash
├── questions.json           # Dataset: All questions, options, answers, explanations, references
├── cli_quiz.py               # CLI-based quiz runner
├── Telegram_Bot_Sample.py    # Telegram bot version of the quiz
├── .env                      # (not included) Must define TELEGRAM_API_KEY
├── .env.example              # Example file showing expected env vars
├── requirements.txt          # Python dependencies to install
```

---

## How to Run It

### CLI Version

```bash
python cli_quiz.py
```
It will ask how many questions you want to attempt.

### Telegram Bot Version

1. Create a `.env` file in your project directory based on `.env.example`:
   ```env
   TELEGRAM_API_KEY=your_telegram_bot_token_here
   ```
2. Install requirements:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the bot:
   ```bash
   python Telegram_Bot_Sample.py
   ```
4. Start chatting with your bot on Telegram! Type `/start`.

---

## Requirements

- Python 3.9+
- `python-telegram-bot`
- `python-dotenv`

```bash
pip install -r requirements.txt
```

---

## Important

- This material is **based on** and **references** official Fortinet SASE public documentation.
- Every question points to the proper source.
- It exists to **complement** hands-on practice and formal study.
- No confidential, internal, or proprietary material is used.

---

## Rerefences

- **Concepts Source:** Fortinet Public Docs ([https://docs.fortinet.com](https://docs.fortinet.com))
- **Quiz Generator:** LLM-based Question Generation (fine-tuned)
- **Development:** You, and your relentless will to make study less boring and more epic.

