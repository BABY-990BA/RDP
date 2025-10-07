import logging
import threading
import random
import time
import os
from rich.console import Console, Group
from rich.panel import Panel
from rich.text import Text
from cfonts import render
from itertools import count
from urllib.parse import unquote
from playwright.sync_api import sync_playwright

console = Console()

# 🎨 Terminal colors
# config.py
COLORS = {
    'red': '\033[1;31m',
    'green': '\033[1;32m',
    'yellow': '\033[1;33m',
     'cyan': '\033[36m',
    'blue': '\033[1;34m',
    'reset': '\033[0m',
    'gold': '\x1b[38;5;220m',
    'bold': '\033[1m',
}

background_colors = {
    'black'     : '\033[40m',
    'red'       : '\033[41m',
    'green'     : '\033[42m',
    'yellow'    : '\033[43m',
    'blue'      : '\033[44m',
    'magenta'   : '\033[45m',
    'cyan'      : '\033[46m',
    'white'     : '\033[47m'
}

background_256 = {
    'bright_magenta' : '\033[48;5;201m',
    'bright_blue'    : '\033[48;5;117m',
    'bright_green'   : '\033[48;5;82m',
    'bright_yellow'  : '\033[48;5;226m',
    'bright_cyan'    : '\033[48;5;87m',
    'bright_red'     : '\033[48;5;196m',
    'gray'           : '\033[48;5;244m',
    'orange'         : '\033[48;5;208m',
    'purple'         : '\033[48;5;93m'
}
# 🔮 Title line
title = Text("INSTAGRAM AUTOMATION TOOL - NC", style="bold red", justify="center")

# 🌫️ Fancy Unicode separator
separator = Text("-"*40, style="red", justify="center")

# 🔗 Body content with icons
body = Text("\n".join([
    "instagram nc",
    "telegram: https://t.me/csnvsehu",
    "V12 pc compactiblity"
]), style="bold red", justify="center")

# ⛩️ Combine inner parts
inner_group = Group(title, separator, body)

# 🎁 Inner panel
inner_panel = Panel(inner_group, border_style="red", padding=(1, 4), title="V12 ", subtitle="by Team CSNV")

# 🌟 Wrap everything with graffiti in outer panel
full_group = Group( inner_panel)
outer_panel = Panel(full_group, border_style="blue")

# 📟 Print final masterpiece
console.print(outer_panel)

def logo():
    print(render("•GAME OVER •", colors=["green", "red"]))

def banner():
    #os.system("cls" if os.name == "nt" else "clear")
    print(render("• CSNV •", colors=["red", "blue"]))
    #print(COLORS['blue'] + "Instagram automation NC " + COLORS['reset'])
    #print(COLORS['yellow'] + "Created by 𝗕A𝗡𝝣." + COLORS['reset'])
    #print(COLORS['red'] + "Version: v12-beta" + COLORS['reset'])
    #print(COLORS['green']+COLORS['bold']+ "also known as\033[0m  "+background_256["bright_red"]+"the RDP killer" + COLORS['reset'])  
   # print(render("• CSNV •", colors=["red", "blue"]))

def show_progress():
    anim = ["[■□□□□□□□□□]", "[■■□□□□□□□□]", "[■■■□□□□□□□]", "[■■■■□□□□□□]", "[■■■■■□□□□□]", "[■■■■■■□□□□]", "[■■■■■■■□□□]", "[■■■■■■■■□□]", "[■■■■■■■■■□]", "[■■■■■■■■■■]"]
    for i in range(50):
        time.sleep(0.1)
        os.system("cls" if os.name == "nt" else "clear")
        print(anim[i % len(anim)])

#  Load emoji base names
default_bases = [
     "win on top🖤", "giga on top💜", "win on top💚", "apex on top💙", "BANE on top💛", "csnv on top🧡",
    "boxhi on top💞", "win on top💓", "csnv on top💗", "csnv on top💖", "csnv on top💘", "barbie randi haip💝", "barbie randi haip💕", "csnv on top💔"
]
try:
    with open("csnv_bases.txt", "r", encoding="utf-8") as f:
        csnv_bases = [line.strip() for line in f if line.strip()]
    if not csnv_bases:
        raise ValueError("Emoji base file is empty.")
except Exception as e:
    logging.warning(f"⚠️ Failed to load emoji base file: {e}")
    csnv_bases = default_bases

emoji_suffixes = ["🌟", "✨", "⚡", "🔥", "💥", "🌈", "💫"]
name_counter = count(1)
used_names = set()
name_lock = threading.Lock()

#  Inputs

#banner()
session_id = input(COLORS['cyan']+"\nEnter session ID (or press Enter for default): "+COLORS['reset']+ "\033[1;32m\033[45m ").strip()
if not session_id:
    session_id = unquote('')

dm_url = input(COLORS['reset']+COLORS['cyan']+"Enter group chat URL (or press Enter for default): "+COLORS['reset']+ "\033[1;32m\033[45m ").strip()
if not dm_url:
    dm_url = 'https://www.instagram.com/direct/t/9525484444218120/'

try:
    thread_count = int(input(COLORS['reset']+COLORS['cyan']+"Enter number of threads (default 5): "+COLORS['reset']).strip())
except ValueError:
    thread_count = 5
show_progress()
#  Success/fail counters
success_count = 0
fail_count = 0
counter_lock = threading.Lock()

#  Name generation
def generate_unique_name():
    while True:
        base = random.choice(csnv_bases)
        emoji = random.choice(emoji_suffixes)
        suffix = next(name_counter)
        new_name = f"{base}_{emoji}{suffix}"

        with name_lock:
            if new_name not in used_names:
                used_names.add(new_name)
                return new_name

#  Thread task
def rename_thread():
    global success_count, fail_count
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=['--no-sandbox', '--disable-gpu', '--disable-dev-shm-usage'])
        context = browser.new_context(
            user_agent='Mozilla/5.0 (X11; Linux x86_64)',
            viewport=None,
            locale='en-US',
            extra_http_headers={'Referer': 'https://www.instagram.com/'}
        )
        context.add_cookies([{
            'name': 'sessionid',
            'value': session_id,
            'domain': '.instagram.com',
            'path': '/',
            'httpOnly': True,
            'secure': True,
            'sameSite': 'None'
        }])

        page = context.new_page()
        try:
            page.goto(dm_url, wait_until='domcontentloaded', timeout=60000)
        except Exception as e:
            logging.error(f"❌ Initial page.goto failed: {e}")
            return

        try:
            gear_icon = page.locator('svg[aria-label="Conversation information"]')
            gear_icon.wait_for(state="visible", timeout=8000)
            gear_icon.click()
            time.sleep(1)
        except Exception as e:
            logging.error("⚙️ Gear icon failed: " + str(e))
            return

        change_btn = page.locator('div[aria-label="Change group name"][role="button"]')
        group_input = page.locator('input[aria-label="Group name"][name="change-group-name"]')
        save_btn = page.locator('div[role="button"]:has-text("Save")')

        #  Loop infinitely
        while True:
            try:
                new_name = generate_unique_name()
                change_btn.click()
                group_input.click(click_count=3)
                group_input.fill(new_name)

                if save_btn.get_attribute("aria-disabled") == "true":
                    with open("rejected_names.log", "a", encoding="utf-8") as f:
                        f.write(f"{new_name}\n")
                    with counter_lock:
                        fail_count += 1
                    continue

                save_btn.click()
                with counter_lock:
                    success_count += 1
                time.sleep(0.05)

            except Exception:
                with counter_lock:
                    fail_count += 1
                time.sleep(0.1)

        browser.close()

#  Launch threads
for _ in range(thread_count):
    threading.Thread(target=rename_thread, daemon=True).start()

#  Live status display
try:
    while True:
        os.system("cls" if os.name == "nt" else "clear")
        print(banner())
        print(
            f"{background_colors['green']} Success: {success_count} {COLORS['reset']} "
            f"{background_colors['red']} Failed: {fail_count} {COLORS['reset']}",
            end="\r"
        )
        time.sleep(0.1)
except KeyboardInterrupt:
    os.system("cls" if os.name == "nt" else "clear")
    logo()
    print(background_256['bright_red'] + "\n Done renaming." + COLORS['reset'])
