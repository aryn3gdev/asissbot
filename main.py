import os
import discord
from discord.ext import commands
import requests

# -----------------------------
# Environment variables
# -----------------------------
DISCORD_TOKEN = os.environ.get("DISCORD_TOKEN")
HF_API_TOKEN = os.environ.get("HF_API_TOKEN")
MODEL = "Jackrong/Qwen3.5-27B-Claude-4.6-Opus-Reasoning-Distilled"  # You can change to any Hugging Face model

if not DISCORD_TOKEN or not HF_API_TOKEN:
    raise ValueError("DISCORD_TOKEN and HF_API_TOKEN must be set as environment variables.")

# -----------------------------
# Discord bot setup
# -----------------------------
intents = discord.Intents.default()
intents.message_content = True  # Needed to read messages

bot = commands.Bot(command_prefix="!", intents=intents)

# -----------------------------
# Hugging Face API call
# -----------------------------
def query_hf_api(question: str) -> str:
    headers = {"Authorization": f"Bearer {HF_API_TOKEN}"}
    payload = {"inputs": question}
    response = requests.post(
        f"https://api-inference.huggingface.co/models/{MODEL}",
        headers=headers,
        json=payload,
        timeout=60  # Prevent hanging
    )
    if response.status_code != 200:
        return f"Error from Hugging Face API: {response.status_code}"
    
    data = response.json()
    # API returns a list of dicts with 'generated_text'
    if isinstance(data, list) and "generated_text" in data[0]:
        return data[0]["generated_text"]
    elif isinstance(data, dict) and "error" in data:
        return f"API error: {data['error']}"
    else:
        return "I couldn't generate a response."

# -----------------------------
# Commands
# -----------------------------
@bot.command(name="ask")
async def ask(ctx, *, question: str):
    """Ask the AI a question"""
    await ctx.send("Thinking...")
    answer = query_hf_api(question)
    await ctx.send(answer)

# -----------------------------
# Bot events
# -----------------------------
@bot.event
async def on_ready():
    print(f"Bot is online as {bot.user}")

# -----------------------------
# Run the bot
# -----------------------------
bot.run(DISCORD_TOKEN)
