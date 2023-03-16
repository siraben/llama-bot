# LLaMa Discord Bot

This is a Discord bot that uses the LLaMa language model to generate
text based on a user's input prompt. LLaMa is a collection of open and
efficient foundation language models ranging from 7B to 65B
parameters, which were trained on trillions of tokens using publicly
available datasets exclusively.

## Usage
You should clone and build
[llama.cpp](https://github.com/ggerganov/llama.cpp) and add
[bot.py](bot.py) to the project directory.  Make sure you change the
token at the end of the script.

To use the bot, type `!llama` followed by the options and arguments
for generating text. Here are the available options:

```
    -t, --threads: the number of threads to use during computation (default is 8).
    -n, --n_predict: the number of tokens to predict (default is 128).
    -p, --prompt: the prompt to start generation with (required).
    -c, --ctx_size: the size of the prompt context (default is 512).
    -k, --top_k: top-k sampling (default is 40).
    --top_p: top-p sampling (default is 0.9).
    -s, --seed: RNG seed (default is -1).
    --temp: temperature (default is 0.8).
    --repeat_penalty: penalize repeat sequence of tokens (default is 1.3).
```

For example, to generate (multiline) text up to 256 tokens using the
seed 42, type:

```
!llama -n 256 -s 42 -p "I received this long email from an excited friend.
Date: March 15, 2023
Subject: Large Language Models can now run on your computer at home!
Body:"
```

Here's what I got:

![Screenshot](./screenshot.png)

## Things to do
- [ ] handle incorrect argument passing better

## License

This project is licensed under the MIT License---see the
[LICENSE.md](LICENSE.md) file for details.
