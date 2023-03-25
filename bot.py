import discord
import os
import shlex
import subprocess
from discord.ext import commands
import argparse

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)
token = os.environ['DISCORD_TOKEN']

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.startswith('!llama'):
        try:
            # Parse the command options using argparse
            parser = argparse.ArgumentParser(prog='!llama', description='LLaMA Language Model Bot')
            parser.add_argument('-t', '--threads', type=int, default=8, help='number of threads to use during computation')
            parser.add_argument('-n', '--n_predict', type=int, default=128, help='number of tokens to predict')
            parser.add_argument('-p', '--prompt', type=str, required=True, help='prompt to start generation with')
            parser.add_argument('-c', '--ctx_size', type=int, default=512, help='size of the prompt context')
            parser.add_argument('-k', '--top_k', type=int, default=40, help='top-k sampling')
            parser.add_argument('--top_p', type=float, default=0.5, help='top-p sampling')
            parser.add_argument('-s', '--seed', type=int, default=-1, help='RNG seed')
            parser.add_argument('--temp', type=float, default=0.7, help='temperature')
            parser.add_argument('--repeat_penalty', type=float, default=1.17647, help='penalize repeat sequence of tokens')
            parser.add_argument('--repeat_last_n', type=int, default=256, help='last n tokens to consider for penalize')
            try:
                args = parser.parse_args(shlex.split(message.content[7:], posix=True))
            except SystemExit:
                await message.channel.send(f'```\n{parser.format_help()}\n```')
                await message.add_reaction('❌')
                return
            model = './models/13B/ggml-model-q4_0.bin'

            print(f'Generating text with args: {args}')

            # Build the command to execute
            command = ['./main', '-m', model, '-t', str(args.threads), '-n', str(args.n_predict), '-c', str(args.ctx_size), '--temp', str(args.temp), '--top_k', str(args.top_k), '--top_p', str(args.top_p), '--repeat_penalty', str(args.repeat_penalty), '-s', str(args.seed), '--repeat_last_n', str(args.repeat_last_n), '-p', args.prompt]

            # react to the message with a llama emoji
            await message.add_reaction('🦙')

            # Send typing notification
            async with message.channel.typing():
                # Run the command and capture the output
                result = subprocess.run(command, capture_output=True, text=True)

            # Send the output back to the channel
            if result.returncode == 0:
                if len(result.stdout) <= 2000:
                    # reply to the message
                    await message.reply(result.stdout)
                else:
                    # send the message 2000 characters at a time
                    for i in range(0, len(result.stdout), 2000):
                        await message.channel.send(result.stdout[i:i+2000])
                # react to the message with a checkmark
                await message.add_reaction('✅')
            else:
                await message.channel.send('An error occurred while running the command.')
                await message.add_reaction('❌')
        except Exception as e:
            # Send a message back to the channel if an exception occurs
            await message.channel.send(f'An error occurred: {str(e)}')
            await message.add_reaction('❌')

    elif message.content.startswith('!'):
        await message.channel.send('Invalid command. Please use the !llama command.')

bot.run(token)
