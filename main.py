import os
from discord.ext import commands
from openai import OpenAI

# Get your tokens from environment variables
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]
DISCORD_TOKEN = os.environ["DISCORD_TOKEN"]

# Initialize OpenAI client
openai_client = OpenAI()  # No api_key argument needed; it reads OPENAI_API_KEY automatically

# Initialize Discord bot
bot = commands.Bot(command_prefix="!")

@bot.event
async def on_ready():
    print(f"Bot is online as {bot.user}")

@bot.command()
async def ask(ctx, *, question):
    """Responds to user queries using OpenAI."""
    try:
        response = openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": question}]
        )
        answer = response.choices[0].message.content
        await ctx.send(answer)
    except Exception as e:
        await ctx.send(f"Error: {e}")

# Run the bot
bot.run(DISCORD_TOKEN)
