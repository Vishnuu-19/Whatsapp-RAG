import re
import uuid
import json
from datetime import datetime
from pathlib import Path

def detect_message_type(text: str) -> str:
    lowered = text.lower()

    if "image omitted" in lowered:
        return "media_omitted"
    if "video omitted" in lowered:
        return "media_omitted"
    if "contact card omitted" in lowered:
        return "contact_omitted"
    if "missed" in lowered and "call" in lowered:
        return "call_event"
    if "voice" in lowered and "call" in lowered:
        return "call_event"
    if len(text.strip()) <= 2:
        return "reaction"

    return "text"

def get_sender_id(sender: str, mapping: dict) -> str:
    if sender not in mapping:
        mapping[sender] = f"user_{len(mapping)+1:03d}"
    return mapping[sender]

def parse_timestamp(date_str: str, time_str: str)-> datetime:
    return datetime.strptime(
        f"{date_str} {time_str}",
        "%m/%d/%y %I:%M:%S %p"
    )

def is_system_check(message: str):
    SYSTEM_PATTERNS = [
        "end-to-end encrypted",
        "messages and calls are encrypted",
        "this message was deleted",
        "you deleted this message",
        "added",
        "joined",
        "left",
        "changed the group description",
    ]
    if any(patterns in SYSTEM_PATTERNS for patterns in message): 
        return True 
    else:
        return False

MESSAGE_START_RE = re.compile(
    r'^\[(\d{1,2}/\d{1,2}/\d{2}),\s([\d:]+\s[AP]M)\]\s(.+?):\s(.*)'
)

def parse_whatsapp_chat(file_path: str):
    messages = []
    sender_map = {}

    current_msg = None
    raw_lines = []

    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.rstrip("\n")
            match = MESSAGE_START_RE.match(line)

            if match:
                # finalize previous message if exists
                if current_msg:
                    current_msg["message"] = "\n".join(raw_lines)
                    current_msg["raw_lines_count"] = len(raw_lines)
                    current_msg["is_multiline"] = len(raw_lines) > 1
                    current_msg["message_type"] = detect_message_type(current_msg["message"])
                    messages.append(current_msg)

                # start new message
                date_str, time_str, sender, first_text = match.groups()
                timestamp = parse_timestamp(date_str, time_str)
                sender_id = get_sender_id(sender, sender_map)

                current_msg = {
                    "message_id": str(uuid.uuid4()),
                    "timestamp": timestamp,
                    "sender": sender,
                    "sender_id": sender_id,
                    "message": "",
                    "message_type": None,
                    "is_multiline": False,
                    "raw_lines_count": 0,
                    "is_system": is_system_check(line) 
                }
                
                raw_lines = [first_text]

            else:
                # continuation of current message
                if current_msg:
                    raw_lines.append(line)

    # finalize the last message
    if current_msg:
        current_msg["message"] = "\n".join(raw_lines)
        current_msg["raw_lines_count"] = len(raw_lines)
        current_msg["is_multiline"] = len(raw_lines) > 1
        current_msg["message_type"] = detect_message_type(current_msg["message"])
        messages.append(current_msg)
        
    write_messages_json(messages,"data/processed/messages.json")    
    return messages
    
def write_messages_json(messages, output_path: str):
    output_path = Path(output_path)
    # output_path.parent.mkdir(parent=True, exist_ok = True)

    with output_path.open("w", encoding="utf-8") as f:
        for msg in messages:
            msg_copy = msg.copy()
            msg_copy["timestamp"] = msg_copy["timestamp"].isoformat()
            f.write(json.dumps(msg_copy, ensure_ascii=False) + "\n")