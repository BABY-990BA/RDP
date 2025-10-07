import datetime
import time
import asyncio
import logging
import random
from itertools import count
from urllib.parse import unquote
from playwright.async_api import async_playwright


EXPIRY = "2025-08-02 23:59:00"
expiry_timestamp = int(time.mktime(datetime.datetime.strptime(EXPIRY, "%Y-%m-%d %H:%M:%S").timetuple()))


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

try:
    with open("ufo_bases.txt", "r", encoding="utf-8") as f:
        ufo_bases = [line.strip() for line in f if line.strip()]
except Exception:
        ufo_bases = [
"LIGHTER 𝗞𝗔𝗖𝗛𝗥𝗘 𝗪𝗔𝗟𝗘 ", "LIGHTER  𝗚𝗨𝗟𝗔𝗠", "LIGHTER  𝗞𝗨𝗧𝗧𝗘"]
emo = ["🥀", "🤙🏿", "🖖🏿", "🤟🏿", "🔥", "💥", "🚀", "👾" ,"🤘", "🤙", "👎", "👌", "✋", "🖐️", "✊", "👊", "🤛", "🤜", "🤚", "👋", "🫶", "🙌", "👐", "✍️", "🤟", "🤲", "🙏", "💅", "💅", "🩷", "🧡", "💛", "💚", "💔", "❤️", "🔥", "❤️", "🩹", "❣️", "💕", "💞", "💟", "💝", "💘", "💖", "💓", "💗", "💌", "💢", "💥", "💤", "💦", "💨", "🕉️", "☪️", "✝️", "☮️", "🕳️", "💫", "☸️", "✡️", "🔯", "🪯", "🕎", "☯️", "☦️", "🛐", "⛎", "♈", "♉", "♊", "♐", "♏", "♎", "♍", "♌", "♋", "♑", "♒", "🆔", "⚕️", "♾️", "🈸", "🈚", "🈶", "🈹", "🈳", "⚛️", "🈺", "🈷️", "✴️", "🉑", "💮", "🪷", "🉐", "🈴", "🈵", "🆑", "🆎", "🅱️", "🅰️", "🚼", "🈲", "🅾️", "⛔", "🆘", "🛑", "📛", "❌", "⭕", "🚫", "🔇", "🔕", "🚭", "🚷", "❗", "📵", "🔞", "🚱", "🚳", "🚯", "❕", "❓", "❔", "‼️", "⁉️", "💯", "☢️", "〽️", "⚜️", "🔱", "🔆", "🔅", "☣️", "⚠️", "🚸", "🔰", "♻️", "🈯", "💠", "✅", "✳️", "❇️", " 💹", "🌐", "➿", "🛂", "🛃", "🛅", "♿", "🚾", "🅿️", "🚰", "🛜", "📶", "🚮", "🚻", "🚺", "🚺", "🚹", "🕧", "🕦", "🕥", "🕤", "🕣", "🕢", "🕡", "🕠", "🕟", "🕞", "🕝", "🕜", "🕛", "🕚", "🕙", "🕘", "🕗", "🕖", "🕕", "🕔", "🕓", "🕒"]
nc = count(1)
un = set()
ssc = 0
fcc = 0
lock = asyncio.Lock()


sid = input("Session ID: ").strip() or unquote('4487278012:lBxRlMbkQ8WzcC:16:AYcyM38OO9GCtmfmg7mG44_6TiSGHUoBaTKrFhsBfg')
dm = input("Group chat URL: ").strip() or 'https://www.instagram.com/direct/t/24336138072742166/'
tskc = int(input("Number of async tasks: ").strip() or 5)
tbm = input("Enable rampage tick? (y/n): ").strip().lower() == "y"

def genm():
    while True:
        base = random.choice(ufo_bases)
        emoji = random.choice(emo)
        suffix = next(nc)
        name = f"{base}_{emoji}{suffix}"
        if name not in un:
            un.add(name)
            return name

async def rmlp(session_cookie):
    global ssc, fcc
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True, args=['--no-sandbox', '--disable-gpu'])
        context = await browser.new_context(
            locale="en-US",
            extra_http_headers={"Referer": "https://www.instagram.com/"}
        )
        await context.add_cookies([{
            "name": "sessionid",
            "value": session_cookie,
            "domain": ".instagram.com",
            "path": "/",
            "httpOnly": True,
            "secure": True,
            "sameSite": "None"
        }])
        page = await context.new_page()

        try:
            await page.goto(dm, wait_until='domcontentloaded', timeout=60000)
            gear = page.locator('svg[aria-label="Conversation information"]')
            await gear.click()
            await asyncio.sleep(1)
        except Exception as e:
            logging.error(f"Init failed: {e}")
            return

        change_btn = page.locator('div[aria-label="Change group name"][role="button"]')
        group_input = page.locator('input[aria-label="Group name"][name="change-group-name"]')
        save_btn = page.locator('div[role="button"]:has-text("Save")')

        while True:
            try:
                name = genm()
                await change_btn.click()
                await group_input.click(click_count=3)
                await group_input.fill(name)

                if await save_btn.get_attribute("aria-disabled") == "true":
                    async with lock:
                        fcc += 1
                    continue

                await save_btn.click()
                async with lock:
                    ssc += 1

                delay = random.uniform(0.01, 0.03) if tbm else 0.05
                await asyncio.sleep(delay)

            except Exception as e:
                logging.warning(f"Rename failed: {e}")
                async with lock:
                    fcc += 1
                await asyncio.sleep(0.1)

        await browser.close()

async def stm():
    while True:
        async with lock:
            total_attempts = ssc + fcc
            logging.info(f"Used Names: {len(un)} | Attempts: {total_attempts} | ✅ {ssc} | ❌ {fcc}")
        await asyncio.sleep(3)

async def main():
    tasks = []
    for _ in range(tskc):
        tasks.append(asyncio.create_task(rmlp(sid)))
        await asyncio.sleep(random.uniform(0.05, 0.1)) 

    tasks.append(asyncio.create_task(stm()))
    try:
        await asyncio.gather(*tasks)
    except KeyboardInterrupt:
        logging.info("Shutdown requested by user.")

if __name__ == "__main__":
    asyncio.run(main())
