from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
import json

# Bot create karo
eventify_bot = ChatBot('EventifyBot')
trainer = ListTrainer(eventify_bot)

# 1. Train from intents.json
with open('intents.json', 'r') as f:
    data = json.load(f)

for intent in data:
    for pattern in intent['patterns']:
        # Trainer ko "Question-Answer" pair do
        trainer.train([pattern, intent['response']])

print("✅ Training Complete! Bot is ready to test.")