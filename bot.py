import discord
import os
import shlex
import subprocess
from discord.ext import commands
import asyncio
import argparse

# Define constants
DISCORD_TOKEN = os.environ.get('DISCORD_TOKEN')
MODEL_NUMBERS = [7, 13, 30]
MAX_TOKENS = {7: 2048, 13: 1024, 30: 256}
DEFAULT_MODEL = 13
DEFAULT_THREADS = 8
NEW_BOT_COMMAND = '!gpt4all'
OLD_BOT_COMMAND = '!alpaca'
LLAMA_COMMAND = '!llama'
COMMAND_PREFIX = '!'

# Define the bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=COMMAND_PREFIX, intents=intents)

# Define a timeout for subprocesses
SUBPROCESS_TIMEOUT = 60

# Define a lock to ensure only one process runs at a time
lock = asyncio.Lock()

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.event
async def on_message(message):
    if message.author == bot.user or not message.content.startswith(COMMAND_PREFIX):
        return

    if message.content.startswith(OLD_BOT_COMMAND):
        await handle_llama_command(message, new_model=False)
    elif message.content.startswith(NEW_BOT_COMMAND):
        await handle_llama_command(message, new_model=True)
    elif message.content.startswith(LLAMA_COMMAND):
        await handle_llama_command(message, new_model=True)
    else:
        await message.channel.send(f'Invalid command. Please use {NEW_BOT_COMMAND} or {OLD_BOT_COMMAND}.')

async def handle_llama_command(message, new_model=True):
    # react with hourglass
    await message.add_reaction('⏳')
    async with lock:
        try:
            # Parse the command options using argparse
            parser = argparse.ArgumentParser(prog=LLAMA_COMMAND, description='LLaMa Language Model Bot')
            parser.add_argument('-m', '--model', type=int, default=DEFAULT_MODEL, choices=MODEL_NUMBERS, help='model number (7/13/30) (default: 13)')
            parser.add_argument('-t', '--threads', type=int, default=DEFAULT_THREADS, help='number of threads to use during computation')
            parser.add_argument('-n', '--n_predict', type=int, default=128, help='number of tokens to predict (max 2048/1024/512)')
            parser.add_argument('-p', '--prompt', type=str, required=True, help='prompt to start generation with')
            parser.add_argument('-c', '--ctx_size', type=int, default=512, help='size of the prompt context')
            parser.add_argument('-k', '--top_k', type=int, default=40, help='top-k sampling')
            parser.add_argument('--top_p', type=float, default=0.5, help='top-p sampling')
            parser.add_argument('-s', '--seed', type=int, default=-1, help='RNG seed')
            parser.add_argument('--temp', type=float, default=0.7, help='temperature')
            parser.add_argument('--repeat_penalty', type=float, default=1.17647, help='penalize repeat sequence of tokens')
            parser.add_argument('--repeat_last_n', type=int, default=256, help='last n tokens to consider for penalize')

            args = parser.parse_args(shlex.split(message.content)[1:])

            # limit n_predict based on model number
            args.n_predict = min(args.n_predict, MAX_TOKENS.get(args.model, MAX_TOKENS[DEFAULT_MODEL]))

            # Build the command to execute to execute
            if new_model:
                model = 'gpt4all-lora-unfiltered-quantized.bin'
                command = ['./gpt4all-lora-quantized-OSX-m1', '-m', model, '-t', str(args.threads), '-n', str(args.n_predict), '-p', args.prompt]
            else:
                command = ['./chat', '-m', 'ggml-model-q4_0.bin', '-n', str(args.n_predict), '-t', str(args.threads), '-p', args.prompt]

            print(f'Executing command: {command}')

            # react to the message with a llama emoji
            await message.add_reaction('🦙')
        
            # Send typing notification
            async with message.channel.typing():
                # Run the command and capture the output
                process = await asyncio.wait_for(asyncio.create_subprocess_exec(*command, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE), timeout=SUBPROCESS_TIMEOUT)
                stdout, stderr = await process.communicate()
        
                # Decode the output from bytes to string
                result_stdout = stdout.decode('utf-8')
                result_stderr = stderr.decode('utf-8')
        
            # Send the output back to the channel
            if process.returncode == 0:
                if len(result_stdout) <= 2000:
                    response_prefix = "**GPT4All:** " if new_model else "**Alpaca:** "
                    result_stdout = response_prefix + result_stdout
                    # reply to the message
                    await message.reply(result_stdout)
                else:
                    # send the message 2000 characters at a time
                    for i in range(0, len(result_stdout), 2000):
                        await message.channel.send(result_stdout[i:i+2000])
                # react to the message with a checkmark
                await message.add_reaction('✅')
            else:
                await message.channel.send('An error occurred while running the command.')
                await message.add_reaction('❌')

        except (argparse.ArgumentError, SystemExit) as e:
            await message.channel.send(f'Invalid command arguments: {str(e)}')
            await message.add_reaction('❌')
        except (discord.errors.HTTPException, asyncio.TimeoutError) as e:
            await message.channel.send(f'Error executing command: {str(e)}')
            await message.add_reaction('❌')
        except argparse.ArgumentError as e:
            await message.channel.send(f'Invalid command arguments: {str(e)}')
            await message.add_reaction('❌')
        except Exception as e:
            # Send a message back to the channel if an exception occurs
            await message.channel.send(f'An error occurred: {str(e)}')
            await message.add_reaction('❌')
    await message.remove_reaction('⏳', bot.user)

bot.run(DISCORD_TOKEN)
