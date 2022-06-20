from pathlib import Path
import os
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
import argparse
from bot import Bot, start_threading_run
from learn_feedback import training_with_feedback

# Create the parser
parser = argparse.ArgumentParser(description='Sociopath bot')
parser.add_argument('-r', '-rebuild', action='store_true')
parser.add_argument('-t', '-train', action='store_true')

def train():
    print('--Training--')
    bot = Bot()    
    print("--Type something to start learning--")
    training_with_feedback(bot)

def rebuild():
    print('--Rebuild--')

    cwd = Path().cwd()
    for f in cwd.iterdir():
        if f.suffix == '.sqlite3':
            f.unlink()
    
    trainer = ChatterBotCorpusTrainer(Bot())
    trainer.train(
        "chatterbot.corpus.english.greetings",
        "chatterbot.corpus.english.humor",
        "chatterbot.corpus.english.movies",
        "chatterbot.corpus.english.sports",
        "chatterbot.corpus.english.psychology",
        "chatterbot.corpus.english.food"        
        )

def run():
    print('--Run--')
    bot = Bot()   
    start_threading_run(bot)

if __name__ == '__main__':
    args = parser.parse_args()
    if(args.r):
        rebuild()
    elif(args.t):
        train()
    else:
        run()