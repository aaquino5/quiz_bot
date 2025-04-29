###Project Overview###P

This project contains:

- CLI Quiz App (cli_quiz.py)

- Telegram Bot (Telegram_Bot_Sample.py)

- Quiz Dataset (questions.json) - based on public FortiSASE documentation.

Both tools allow users to:

- Answer randomized multiple-choice SASE questions

- Receive detailed explanations and source links for learning reinforcement

- Practice SASE concepts like Zero Trust, SD-WAN, FWaaS, and more

########### Key Principle: This is a study companion, not a "shortcut." No leaks. No dumps. Just pure, clean learning.###########

Features

CLI Version (cli_quiz.py)

- Random question selection

 - Final score display

- Detailed explanations after each question


########### Telegram Bot Version (Telegram_Bot_Sample.py)###########

Commands: /start, /quiz

-Inline multiple-choice answer buttons

-Real-time feedback after each question

-Explanations and reference links provided

-Tracks how many questions the user requested


########### Files Structure  ###########

├── questions.json           # Dataset: All questions, options, answers, explanations, references
├── cli_quiz.py               # CLI-based quiz runner
├── Telegram_Bot_Sample.py    # Telegram bot version of the quiz
├── .env                      # (not included) Must define TELEGRAM_API_KEY
