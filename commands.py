import asyncio
from telegram.ext import Application

running = True
_console_commands = {}

def command(name=None):
    def decorator(func):
        cmd_name = name or func.__name__
        _console_commands[cmd_name] = func
        return func
    return decorator

@command("help")
def help_command(bot_app: Application = None, loop: asyncio.BaseEventLoop = None):
    print("Available commands:", ", ".join(_console_commands.keys()))

@command("exit")
def exit_command(bot_app: Application, loop: asyncio.BaseEventLoop):
    global running
    running = False
    loop.call_soon_threadsafe(bot_app.stop_running)

def listen_input(bot_app, loop):
    print("\nType commands or 'help' to see available commands for manipulating.")
    
    while running:
        cmd = input().strip().lower()
        func = _console_commands.get(cmd)
        if func:
            func(bot_app, loop)
        elif cmd == "":
            continue
        else:
            print("Unknown command:", cmd)