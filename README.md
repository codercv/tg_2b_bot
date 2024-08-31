# 2B Telegram Bot

This project is a Telegram bot powered by GPT-4, designed to act as a flirty and shy personal assistant who is also very knowledgeable in programming. The bot can answer questions, assist with programming tasks, and engage in playful conversation.

## Features

- Responds to text commands like `/start`, `/help`, and `/info`.
- Utilizes OpenAI's GPT-4 model to generate responses.
- Keeps a conversation context with a number of recent messages.
- Configurable via environment variables.

## Prerequisites

Before you start, ensure you have the following:

- A Linux (Ubuntu) server.
- Python 3.7+ installed on the server.
- A Telegram bot token. You can obtain this by creating a new bot through [BotFather](https://core.telegram.org/bots#botfather) on Telegram.
- An OpenAI API key to access GPT-4.

## Installation

Follow these steps to set up and run the bot:

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/2b-telegram-bot.git
cd 2b-telegram-bot
```

### 2. Set Up Environment Variables

Create a `.env` file in the root directory of the project with the following content:

```bash
OPENAI_API_KEY=your_openai_api_key
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
```

Replace `your_openai_api_key` and `your_telegram_bot_token` with your actual OpenAI API key and Telegram bot token.

### 3. Run the Activation Script

Run the `activate.sh` script to set up the virtual environment and install dependencies:

```bash
chmod +x activate.sh
./activate.sh
```

This script will:

- Install Python and necessary packages if they are not already installed.
- Create a Python virtual environment in a folder named `myenv`.
- Install the required Python packages.
- Create necessary `.txt` files for bot configuration if they do not already exist.

### 4. Running the Bot

After the environment is set up, you can start the bot using the `start.sh` script:

```bash
chmod +x start.sh
./start.sh
```

The bot will start running and polling for updates.

### 5. Running the Bot in the Background

To keep the bot running even after you disconnect from the SSH session, you can use `tmux`:

```bash
sudo apt install tmux
tmux new -s bot_session
./start.sh
```

Press `Ctrl+B` then `D` to detach from the session. You can reattach later with:

```bash
tmux attach -t bot_session
```

To stop the bot session:

```bash
tmux attach -t bot_session
exit
tmux kill-session -t bot_session
```

## Customization

You can customize the bot's behavior by editing the following files:

- **`bot_instructions.txt`**: The general instructions for the bot's personality and behavior.
- **`com_start.txt`**: The message sent when the `/start` command is issued.
- **`com_help.txt`**: The message sent when the `/help` command is issued.
- **`com_info.txt`**: The message sent when the `/info` command is issued.

## Contributing

Feel free to fork this repository, make improvements, and send pull requests. Any contributions to improve the bot are welcome!

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

---

Enjoy your time with 2B! 💻🤖
