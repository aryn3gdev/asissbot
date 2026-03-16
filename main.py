import discord
from discord.ext import commands
import os
from openai import OpenAI

# Load environment variables
openai_api_key = os.environ.get("API_KEY")
discord_token = os.environ.get("TOKEN")

# Initialize OpenAI client
client = OpenAI(api_key=openai_api_key)

# Initialize Discord bot
bot = commands.Bot(command_prefix="!")

@bot.event
async def on_ready():
    print(f"Bot is online as {bot.user}")

@bot.command()
async def ask(ctx, *, question):
    """Responds to user queries using OpenAI."""
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": question}]
        )
        answer = response.choices[0].message.content
        await ctx.send(answer)
    except Exception as e:
        await ctx.send(f"Error: {e}")

# Run the bot
bot.run(discord_token)
