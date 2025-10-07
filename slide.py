import asyncio
import random
import logging
from itertools import cycle
from urllib.parse import unquote
from playwright.async_api import async_playwright

# Configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

class InstagramReplyBot:
    def __init__(self, session_id, target_url, replies, task_count=3):
        self.session_id = session_id
        self.target_url = target_url
        self.replies = replies
        self.task_count = task_count
        self.success_count = 0
        self.fail_count = 0
        self.lock = asyncio.Lock()
        self.reply_cycle = cycle(replies)

    def get_next_reply(self):
        return next(self.reply_cycle)

    async def send_reply(self, page, reply_text):
        """Send a reply to the current conversation"""
        try:
            # Find the message input area
            message_input = page.locator('div[role="textbox"][aria-label="Message"]')
            
            # Check if input is available
            if await message_input.count() == 0:
                logging.warning("Message input not found")
                return False

            # Clear and type the reply
            await message_input.click()
            await message_input.press("Control+A")
            await message_input.type(reply_text, delay=random.uniform(50, 150))
            
            # Send the message
            await message_input.press("Enter")
            
            # Wait for message to be sent
            await asyncio.sleep(random.uniform(1, 2))
            
            # Verify message was sent by checking for the message in the chat
            await asyncio.sleep(1)
            
            return True
            
        except Exception as e:
            logging.error(f"Failed to send reply: {e}")
            return False

    async def reply_worker(self, worker_id):
        """Worker function to send replies"""
        async with async_playwright() as p:
            browser = await p.chromium.launch(
                headless=True,
                args=['--no-sandbox', '--disable-gpu', '--disable-dev-shm-usage']
            )
            
            context = await browser.new_context(
                viewport={'width': 1920, 'height': 1080},
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                locale="en-US"
            )
            
            # Add session cookie
            await context.add_cookies([{
                "name": "sessionid",
                "value": self.session_id,
                "domain": ".instagram.com",
                "path": "/",
                "httpOnly": True,
                "secure": True,
                "sameSite": "Lax"
            }])
            
            page = await context.new_page()
            
            try:
                # Navigate to target URL
                await page.goto(self.target_url, wait_until='networkidle', timeout=60000)
                logging.info(f"Worker {worker_id}: Page loaded successfully")
                
                # Wait for page to fully load
                await asyncio.sleep(3)
                
                # Check if we're in a conversation
                if "direct" not in self.target_url.lower():
                    logging.error("Target URL doesn't appear to be a direct message")
                    return
                
                while True:
                    try:
                        # Get next reply text
                        reply_text = self.get_next_reply()
                        
                        # Send the reply
                        success = await self.send_reply(page, reply_text)
                        
                        async with self.lock:
                            if success:
                                self.success_count += 1
                                logging.info(f"Worker {worker_id}: ✅ Sent: '{reply_text}'")
                            else:
                                self.fail_count += 1
                                logging.warning(f"Worker {worker_id}: ❌ Failed to send reply")
                        
                        # Random delay between replies
                        delay = random.uniform(5, 15)
                        await asyncio.sleep(delay)
                        
                    except Exception as e:
                        logging.error(f"Worker {worker_id}: Error in reply loop: {e}")
                        async with self.lock:
                            self.fail_count += 1
                        
                        # Wait before retry
                        await asyncio.sleep(10)
                        
            except Exception as e:
                logging.error(f"Worker {worker_id}: Initialization failed: {e}")
            finally:
                await browser.close()

    async def status_monitor(self):
        """Monitor and display status"""
        while True:
            async with self.lock:
                total = self.success_count + self.fail_count
                logging.info(f"📊 STATUS | Total: {total} | ✅: {self.success_count} | ❌: {self.fail_count}")
            await asyncio.sleep(10)

    async def run(self):
        """Main function to run the bot"""
        logging.info("🚀 Starting Instagram Reply Bot...")
        
        # Create tasks
        tasks = []
        for i in range(self.task_count):
            task = asyncio.create_task(self.reply_worker(i+1))
            tasks.append(task)
            await asyncio.sleep(random.uniform(1, 3))  # Stagger startup
        
        # Add status monitor
        tasks.append(asyncio.create_task(self.status_monitor()))
        
        # Run all tasks
        try:
            await asyncio.gather(*tasks)
        except KeyboardInterrupt:
            logging.info("🛑 Shutdown requested by user")
        except Exception as e:
            logging.error(f"Unexpected error: {e}")
        finally:
            # Cancel all tasks
            for task in tasks:
                task.cancel()

# Sample reply messages
SAMPLE_REPLIES = [
    "lighter tushar ci maa cudi! 🙏",
    "lighter tushar ci maa cudi! 👍",
    "lighter tushar ci maa cudi 💯",
    lighter tushar ci maa cudi! 🤔",
    "lighter tushar ci maa cudi! 👏",
    "Thanks for the update! 📢",
    "lighter tushar ci maa cudi! ❤️",
    "lighter tushar ci maa cudi! 🙌",
    "lighter tushar ci maa cudi! 😊",
    "lighter tushar ci maa cudi! 📚"
]

async def main():
    # Get user input
    session_id = input("Instagram Session ID: ").strip() or unquote('4487278012:lBxRlMbkQ8WzcC:16:AYcyM38OO9GCtmfmg7mG44_6TiSGHUoBaTKrFhsBfg')
    target_url = input("Target chat URL: ").strip() or 'https://www.instagram.com/direct/t/24336138072742166/'
    task_count = int(input("Number of workers (1-5): ").strip() or 3)
    
    # Custom replies or use sample
    use_custom = input("Use custom replies? (y/n): ").strip().lower() == 'y'
    if use_custom:
        print("Enter your replies (one per line, empty line to finish):")
        custom_replies = []
        while True:
            reply = input().strip()
            if not reply:
                break
            custom_replies.append(reply)
        replies = custom_replies if custom_replies else SAMPLE_REPLIES
    else:
        replies = SAMPLE_REPLIES
    
    # Create and run bot
    bot = InstagramReplyBot(session_id, target_url, replies, task_count)
    await bot.run()

if __name__ == "__main__":
    asyncio.run(main())
