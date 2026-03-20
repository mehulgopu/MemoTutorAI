# MemoTutor AI

Adaptive study assistant with memory-driven teaching.

## Problem
Most study tools give one-off answers and forget everything. Students who repeatedly struggle with the same topic get no personalized follow-up.

## Solution
MemoTutor AI builds a lightweight memory profile for the student. It tracks topics, confidence, quiz mistakes, and preferred teaching style. When the student struggles on a quiz, the tutor marks the topic as weak and changes future explanations to be simpler and more focused on fundamentals.

## Features
- Personalized explanations based on learning style
- Quiz generation by topic
- Quiz answer evaluation
- Topic confidence tracking
- Weak and strong topic memory
- Adaptive follow-up explanations
- Transparent memory panel for learning state

## Tech Stack
- Python
- Flask
- HTML
- CSS
- JavaScript
- JSON-based memory storage

## How It Works
1. User asks for an explanation
2. System detects the topic
3. Tutor checks stored memory
4. Tutor explains based on learning style and confidence
5. User can generate a quiz
6. Quiz answers are evaluated
7. Confidence updates
8. Weak topics are stored
9. Future explanations adapt automatically

## Run Locally
```bash
pip install -r requirements.txt
python app.py