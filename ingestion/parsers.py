import re
from datetime import datetime

# Format A: [date, time] Sender: message
FORMAT_A_RE = re.compile(
    r'^\[(\d{1,2}/\d{1,2}/\d{2}),\s([\d:]+\s[AP]M)\]\s(.+?):\s(.*)'
)

# Format B: date, time - Sender: message  OR system message
FORMAT_B_RE = re.compile(
    r'^(\d{1,2}/\d{1,2}/\d{2,4}),\s([\d:]+\s?(?:AM|PM|am|pm))\s-\s(.*)',
    re.IGNORECASE
)



def parse_messages_start(line: str):
    """
    Returns:
      None → continuation line
      dict → new message fields
    """

    #for format A
    m = FORMAT_A_RE.match(line)
    if m:
        date,time,sender,text = m.groups()
        return {
            "date": date,
            "time": time,
            "sender": sender,
            "text": text,
            "format": "A"
        }
    
    m = FORMAT_B_RE.match(line)
    if m:
        date,time,rest = m.groups()
        if ":" in rest:
            sender,text = rest.split(":", 1)
            return {
                "date": date,
                "time": time,
                "sender": sender.strip(),
                "text": text.strip(),
                "format": "B"
            }
        else:
            return {
                "date": date,
                "time": time,
                "sender": None,
                "text": rest.strip(),
                "format": "B"
            }
        
    return None

def parse_timestamp(date_str, time_str):
    time_str = time_str.upper().strip()
    
    # Determine year format based on length
    parts = date_str.split('/')
    if len(parts) == 3:
        year = parts[2]
        if len(year) == 4:
            fmt = "%d/%m/%Y %I:%M %p"
        else:
            fmt = "%d/%m/%y %I:%M %p"
    else:
        # Fallback, assume 2-digit year
        fmt = "%d/%m/%y %I:%M %p"
    
    return datetime.strptime(f"{date_str} {time_str}", fmt)