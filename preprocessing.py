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

MESSAGE_START_RE = re.compile(
    r'\[(\d{1,2}/\d{1,2}/\d{2}),\s([\d:]+\s[AP]M)\]\s(.+?):\s(.*)'
)

SYSTEM_MESSAGE_RE = re.compile(
    r"(messages and calls are end-to-end encrypted"
    r"|this message was deleted"
    r"|you deleted this message"
    r"|security code changed"
    r"|missed (voice|video) call"
    r"|changed (the subject|the group description|this group's icon)"
    r"|added|removed|left|joined)"
    r"|(document|image) omitted",
    re.IGNORECASE
)

def is_system_message(message: str) -> bool:
    message = message.replace("\u200e", "").replace("\u200f", "")
    return SYSTEM_MESSAGE_RE.search(message) is not None

def split_noise_messages(messages):
    noise_msg,normal_msg =[],[]

    for msg in messages:
        if msg["is_system"] or msg["message_type"]=="reaction":
            noise_msg.append(msg)
        else:
            normal_msg.append(msg)
    
    return normal_msg,noise_msg

def write_messages_json(messages, output_path: str):
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok = True)

    messages_copy = []
    for msg in messages:
        msg_copy = msg.copy()
        msg_copy["timestamp"] = msg_copy["timestamp"].isoformat()
        messages_copy.append(msg_copy)

    with output_path.open("w", encoding="utf-8") as f:
        json.dump(messages_copy, f, ensure_ascii=False, indent=2)

def parse_whatsapp_chat(file_path: str):
    messages = []
    sender_map = {}

    current_msg = None
    raw_lines = []

    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.rstrip("\n")
            match = MESSAGE_START_RE.search(line)

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
                    "is_system": is_system_message(line) 
                }
                if current_msg["is_system"]:
                    current_msg["message_type"] = "system"
                
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
        
    normal_msgs,noise_msgs = split_noise_messages(messages)

    write_messages_json(normal_msgs,"data/processed/messages.json")
    write_messages_json(noise_msgs,"data/processed/noise_messages.json")

    return normal_msgs

    