import asyncio
from telegram.ext import Application

running = True

def help_command(bot_app=None, loop=asyncio.BaseEventLoop):
    print("Available commands:", ", ".join(commands_dict.keys()))
def exit_command(bot_app: Application, loop):
    global running
    running = False

    loop.call_soon_threadsafe(bot_app.stop_running)

commands_dict = {
    "help": help_command,
    "exit": exit_command,
}

def listen_input(bot_app, loop):
    print("\nType commands or 'help' to see available commands.")
    
    while running:
        cmd = input().strip().lower()
        func = commands_dict.get(cmd)
        if func:
            func(bot_app, loop)
        elif cmd == "":
            continue
        else:
            print("Unknown command:", cmd)