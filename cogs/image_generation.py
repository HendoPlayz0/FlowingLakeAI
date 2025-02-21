import discord
from discord.ext import commands
import aiohttp
import io
import logging
from config import (
    HUGGINGFACE_TOKEN,
    API_URL,
    RATE_LIMIT_MINUTES,
    MAX_REQUESTS_PER_USER
)
from utils.rate_limiter import RateLimiter

logger = logging.getLogger(__name__)

class ImageGeneration(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.rate_limiter = RateLimiter()
        self.headers = {
            "Authorization": f"Bearer {HUGGINGFACE_TOKEN}"
        }

    @commands.command(name="generate")
    async def generate_image(self, ctx, *, prompt: str):
        """
        Generate an image based on the provided prompt
        Usage: !generate a beautiful sunset over mountains
        """
        if not self.rate_limiter.can_make_request(ctx.author.id):
            remaining_time = RATE_LIMIT_MINUTES
            await ctx.send(f"Rate limit exceeded. Please try again in {remaining_time} minutes.")
            return

        async with ctx.typing():
            try:
                # Send request to HuggingFace
                async with aiohttp.ClientSession() as session:
                    payload = {
                        "inputs": prompt,
                    }

                    async with session.post(API_URL, headers=self.headers, json=payload) as response:
                        if response.status != 200:
                            await ctx.send(f"Error: Failed to generate image (Status code: {response.status})")
                            return

                        image_bytes = await response.read()

                # Create discord file from image bytes
                image_file = discord.File(io.BytesIO(image_bytes), filename="generated_image.png")

                # Record the request
                self.rate_limiter.add_request(ctx.author.id)

                # Send the image
                await ctx.send(
                    f"Here's your generated image for prompt: '{prompt}'",
                    file=image_file
                )

                # Show remaining requests
                remaining = self.rate_limiter.get_remaining_requests(ctx.author.id)
                await ctx.send(f"You have {remaining} generations remaining in the current time window.")

            except Exception as e:
                logger.error(f"Error generating image: {e}")
                await ctx.send("Sorry, there was an error generating your image. Please try again later.")

    @commands.command(name="help_generate")
    async def help_generate(self, ctx):
        """Show help information about the image generation commands"""
        help_embed = discord.Embed(
            title="Image Generation Bot Help",
            color=discord.Color.blue()
        )

        help_embed.add_field(
            name="!generate [prompt]",
            value="Generate an image based on your text prompt\n"
                  "Example: !generate a beautiful sunset over mountains",
            inline=False
        )

        help_embed.add_field(
            name="Rate Limits",
            value=f"You can generate {MAX_REQUESTS_PER_USER} images every {RATE_LIMIT_MINUTES} minutes",
            inline=False
        )

        help_embed.add_field(
            name="Tips",
            value="- Be specific in your prompts\n"
                  "- Avoid inappropriate or offensive content\n"
                  "- The more detailed your prompt, the better the result",
            inline=False
        )

        await ctx.send(embed=help_embed)

async def setup(bot):
    await bot.add_cog(ImageGeneration(bot))