import sqlite3
from telegram import Update
from telegram.ext import Application, MessageHandler, CommandHandler, filters, ContextTypes

from dotenv import load_dotenv
import os


# Env variables
load_dotenv()
api_key = os.getenv("JS_TUT_BOT_API_KEY")


def main():
    pass


if __name__ == '__main__':
    main()
