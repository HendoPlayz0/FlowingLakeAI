import discord
from discord.ext import commands
import asyncio
import logging
from config import DISCORD_TOKEN, COMMAND_PREFIX, BOT_DESCRIPTION

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize bot with intents
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(
    command_prefix=COMMAND_PREFIX,
    description=BOT_DESCRIPTION,
    intents=intents
)

@bot.event
async def on_ready():
    logger.info(f'Bot is ready! Logged in as {bot.user.name}')
    try:
        await bot.load_extension('cogs.image_generation')
        logger.info('Successfully loaded image generation cog')
    except Exception as e:
        logger.error(f'Failed to load image generation cog: {e}')

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send(f"Please wait {error.retry_after:.2f} seconds before using this command again.")
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("You don't have permission to use this command.")
    else:
        await ctx.send(f"An error occurred: {str(error)}")
        logger.error(f"Command error: {error}")

def main():
    if not DISCORD_TOKEN:
        logger.error("Discord token not found in environment variables!")
        return
    
    try:
        bot.run(DISCORD_TOKEN)
    except Exception as e:
        logger.error(f"Failed to start bot: {e}")

if __name__ == "__main__":
    main()
