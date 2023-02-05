from api_keys import *
import requests

class Telegram:

    def __init__(self) -> None:
        pass

    def send_message(self, msg:str) -> bool:
        bot_request = f'https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage?chat_id={TELEGRAM_CHAT_ID}&text={msg}'
        print(bot_request)
        response = requests.get(bot_request) 
        if (response == 200):
            return True 
        else:
            return False