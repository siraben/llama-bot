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

```
I received this long email from an excited friend.
Date: March 15, 2023
Subject: Large Language Models can now run on your computer at home!
Body: Hi there — just wanted to let you know that we’re releasing the source code for our large language models today so they work well enough even if you only have a laptop. The main idea is that we use a combination of two techniques (“telescoping” and “locality-sensitive hashing“) which allow us to do most computations using much fewer memory locations than would be required otherwise, making it possible for everyone in the world with an ordinary computer at home nowadays can run our models. The source code is available here:
https://www.openaiplatform.com/research-blog/?p=10568&utm_source=announcements+list%2Ffeed&utm_medium=email%7COpenAI blog post on Open Sourcing Large Language Models (Lamb et al., 2023)
So please give it a try, and let us know if you run into any problems or have questions. The models were trained using the same hardware as our previous experiments: four NVIDIA V100 GPUs with Tensor Core for each model, plus three other types of servers to make sure we had enough computing power available
```

## Things to do
- [ ] handle incorrect argument passing better

## License

This project is licensed under the MIT License---see the
[LICENSE.md](LICENSE.md) file for details.
