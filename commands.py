import asyncio

running = True
app = None

def help_command():
    print("Available commands:", ", ".join(commands.keys()))
def exit_command():
    global running
    running = False
    asyncio.run_coroutine_threadsafe(app.stop(), asyncio.get_event_loop())
    return

commands = {
    "help": help_command,
    "exit": exit_command,
}

async def main(bot_app):
    print("\nType commands or 'help' to see available commands.")
    
    global running, app
    app = bot_app
    
    while running:
        cmd = input().strip().lower()
        func = commands.get(cmd)
        if func:
            func()
        elif cmd == "":
            continue
        else:
            print("Unknown command:", cmd)

if __name__ == "__main__":
    main()