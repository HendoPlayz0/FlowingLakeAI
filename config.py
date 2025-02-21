import os

# Discord Bot Configuration
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN', '')
HUGGINGFACE_TOKEN = os.getenv('HUGGINGFACE_TOKEN', '')

# Rate Limiting Configuration
RATE_LIMIT_MINUTES = 5
MAX_REQUESTS_PER_USER = 3

# HuggingFace Configuration
MODEL_ID = "stabilityai/stable-diffusion-2-1"
API_URL = f"https://api-inference.huggingface.co/models/{MODEL_ID}"

# Discord Bot Settings
COMMAND_PREFIX = "!"
BOT_DESCRIPTION = "A Discord bot that generates images using AI"
