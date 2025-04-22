import json
from datetime import datetime
import os

HISTORY_FILE = "dialogue_history.jsonl"

def save_dialogue(user_input, bot_reply, ip_address="unknown"):
    # Создание записи с данными и сообщениями
    entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "ip": ip_address,
        "user": user_input,
        "bot": bot_reply
    }
    
    # Открытие файла в режиме добавления и запись новой строки с записью
    with open(HISTORY_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")
