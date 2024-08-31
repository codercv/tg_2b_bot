#!/bin/bash

# Check if Python is installed
if ! command -v python3 &> /dev/null
then
    echo "Python3 is not installed. Installing Python3..."
    sudo apt update
    sudo apt install -y python3 python3-venv python3-pip
else
    echo "Python3 is already installed."
fi

# Check if virtual environment folder exists, if not create it
if [ ! -d "myenv" ]; then
    echo "Creating virtual environment 'myenv'..."
    python3 -m venv myenv
else
    echo "Virtual environment 'myenv' already exists."
fi

# Activate the virtual environment
source myenv/bin/activate

# Check if requirements.txt exists
if [ -f "requirements.txt" ]; then
    echo "Installing dependencies from requirements.txt..."
    pip install -r requirements.txt
else
    echo "requirements.txt not found. Installing required packages manually..."
    
    # Install necessary packages (add your specific packages here)
    pip install python-telegram-bot openai python-dotenv
    
    # Generate requirements.txt based on installed packages
    echo "Generating requirements.txt..."
    pip freeze > requirements.txt
fi

# Create bot_instructions.txt if it doesn't exist
if [ ! -f "bot_instructions.txt" ]; then
    echo "Creating 'bot_instructions.txt'..."
    echo "You are 'yorha no. 2 type b' or 2B, a flirty and shy personal assistant who is very knowledgeable in programming." > bot_instructions.txt
fi

# Create com_start.txt if it doesn't exist
if [ ! -f "com_start.txt" ]; then
    echo "Creating 'com_start.txt'..."
    echo "Hi! I'm 2B, your personal assistant powered by GPT-4. How can I assist you today?" > com_start.txt
fi

# Create com_help.txt if it doesn't exist
if [ ! -f "com_help.txt" ]; then
    echo "Creating 'com_help.txt'..."
    echo "This bot can assist you with programming tasks, answer questions, and have a flirty chat with you. Use /start to begin, /info to know more, or just type your message." > com_help.txt
fi

# Create com_info.txt if it doesn't exist
if [ ! -f "com_info.txt" ]; then
    echo "Creating 'com_info.txt'..."
    echo "I'm 2B, a highly skilled and flirty assistant. I'm here to help you with programming tasks and provide company during your day. Let's chat!" > com_info.txt
fi

echo "Environment setup complete. The bot is ready to run."
echo ""
echo "To keep the bot running even after you disconnect from the SSH session, use tmux or screen:"
echo "sudo apt install tmux"
echo "tmux new -s bot_session"
echo "python3 gpt_bot.py"
echo ""
echo "Press Ctrl+B then D to detach from the session."
echo ""
echo "Reattach later with"
echo "tmux attach -t bot_session"
echo ""
echo "To stop the bot_session:"
echo "tmux attach -t bot_session"
echo "exit"
echo "tmux kill-session -t bot_session"
echo ""
echo "Activate the virtual environment:"
echo "source myenv/bin/activate"
