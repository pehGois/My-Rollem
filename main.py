import discord
from discord.ext import commands

import random

import os
from dotenv import load_dotenv
load_dotenv()

import re

TOKEN = os.getenv("DISCORD_TOKEN")

def is_input_ok(dice_input):
    dice_pattern = re.compile(r'^(\d+)d(\d+)(>>(\d+))?(\d+)?$')
    match = dice_pattern.match(dice_input.content)
    return match

def parse_dice_input(dice_input):
    return int(dice_input.group(1)), int(dice_input.group(2))

def roll(number_dices, numberOfSides):
    rollArray = []
    for _ in range(number_dices):
        rollArray.append(random.randint(1, numberOfSides)) 
    return rollArray

def print_dice_array(dice_rolls, num_sides):
    formatted_rolls = []
    for roll in dice_rolls:
        if roll == num_sides or roll == 1:
            formatted_rolls.append(f'**{roll}**')
        else:
            formatted_rolls.append(str(roll))
    return str(sum(dice_rolls)) + " ← ["+', '.join(formatted_rolls)+"]"

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
prefix = "."

bot = commands.Bot(command_prefix=prefix, intents=intents)

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')
    
@bot.event
async def on_message(message: discord.Message):
    if message.author.bot:
        return
    
    match = is_input_ok(message) 

    if (match):
        num_dice, num_sides = parse_dice_input(match)

        if num_dice > 0 and num_sides > 0:
            dice_rolls = roll(num_dice, num_sides)
            response = print_dice_array(dice_rolls, num_sides)
            await message.channel.send(response)

bot.run(TOKEN)