import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message
from aiogram import F
from dotenv import load_dotenv
import os
import openai
import asyncio

# Define your Reference class
class Reference:
    '''
    A class to store previously response from the chatGPT API
    '''
    def __init__(self) -> None:
        self.response = ""
        self.chat_id = None  # Added to store chat_id as per your code

# Load environment variables
load_dotenv()

openai.api_key = os.getenv('OPENAI_API_KEY')
API_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

reference = Reference()

# Model Name
MODEL_NAME = "gpt-3.5-turbo"

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Function to clear the previous conversation and context
def clear_past():
    reference.response = ""

# Command handler for /start
@dp.message(Command("start"))
async def welcome(message: Message):
    """ 
    This handler receives messages with '/start' command.
    """
    await message.answer('Hi\nI am Tele Bot!\nCreated by Mohit Solunke. How can I assist you?')
    reference.chat_id = message.chat.id  # Store chat_id to reference

# Command handler for /clear
@dp.message(Command("clear"))
async def clear(message: Message):
    """ 
    A handler to clear the previous conversation and context.
    """
    clear_past()
    await message.answer("I've cleared the previous conversation and context.")

# Command handler for /help
@dp.message(Command("help"))
async def helper(message: Message):
    """ 
    A handler to display the help message.
    """
    help_command = """
    Hi There, I'm chatGPT Telegram bot created by Mohit Solunke! Please follow these commands:
    /start - to start the conversation.
    /clear - to clear the past conversation and context.
    /help - to get the help menu.
    I hope this helps. :)      
    """
    await message.answer(help_command)

# Handler for processing user input and responding with chatGPT API
@dp.message(F.text)
async def chatgpt(message: Message):
    """
    A handler to process the user's inputs and generate a response using the chatgpt API.
    """
    print(f">>> USER: \n\t{message.text}")
    response = openai.ChatCompletion.create(
        model=MODEL_NAME,
        messages=[
            {"role": "assistant", "content": reference.response},  # Role assistant
            {"role": "user", "content": message.text}  # User's query
        ]
    )
    
    reference.response = response.choices[0]['message']['content']
    print(f">>> RESPONSE: \n\t{reference.response}")
    await bot.send_message(chat_id=message.chat.id, text=reference.response)

# Main function to run the bot
async def main():
    # Start polling
    await dp.start_polling(bot)

if __name__ == "__main__":
    # Run the bot with asyncio
    asyncio.run(main())
