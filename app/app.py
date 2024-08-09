import os
from dotenv import load_dotenv
import time

load_dotenv()
bot_name = os.getenv('BOT_NAME', 'DefaultBot')  # Si no está definida, usa 'DefaultBot'
print("")
print(f"Bot name is {bot_name}")
time.sleep(20)
print(f"se finalizara")
time.sleep(20)
