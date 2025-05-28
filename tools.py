import re
from io import BytesIO
from urllib.parse import parse_qs, urlparse

import requests
from telethon import TelegramClient

def check_url_patterns(url: str) -> bool:
    url_pattern = re.compile(
        r'^(https?|ftp)://[^\s/$.?#].[^\s]*$', re.IGNORECASE
    )
    return bool(re.match(url_pattern, url))

def extract_code_from_url(url: str) -> str or None:
    pattern1 = r"/s/(\w+)"
    pattern2 = r"surl=(\w+)"
    match = re.search(pattern1, url)
    if match:
        return match.group(1)
    match = re.search(pattern2, url)
    if match:
        return match.group(1)
    return None

def get_urls_from_string(string: str) -> str or None:
    pattern = r"(https?://\S+)"
    urls = re.findall(pattern, string)
    urls = [url for url in urls if check_url_patterns(url)]
    if not urls:
        return None
    return urls[0]

def extract_surl_from_url(url: str) -> str or bool:
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)
    surl = query_params.get("surl", [])
    if surl:
        return surl[0]
    else:
        return False

def parse_size_to_bytes(size_str: str) -> int or None:
    """Convert size string (e.g., '130.28 MB') to bytes."""
    if not size_str:
        return None
    try:
        size, unit = size_str.split()
        size = float(size)
        units = {"KB": 1024, "MB": 1024**2, "GB": 1024**3, "TB": 1024**4}
        return int(size * units.get(unit.upper(), 1))
    except Exception as e:
        print(f"Failed to parse size '{size_str}': {e}")
        return None

def get_formatted_size(size_bytes: int) -> str:
    if size_bytes >= 1024 * 1024:
        size = size_bytes / (1024 * 1024)
        unit = "MB"
    elif size_bytes >= 1024:
        size = size_bytes / 1024
        unit = "KB"
    else:
        size = size_bytes
        unit = "b"
    return f"{size:.2f} {unit}"

def convert_seconds(seconds: int) -> str:
    seconds = int(seconds)
    hours = seconds // 3600
    remaining_seconds = seconds % 3600
    minutes = remaining_seconds // 60
    remaining_seconds_final = remaining_seconds % 60
    if hours > 0:
        return f"{hours}h:{minutes}m:{remaining_seconds_final}s"
    elif minutes > 0:
        return f"{minutes}m:{remaining_seconds_final}s"
    else:
        return f"{remaining_seconds_final}s"

async def is_user_on_chat(bot: TelegramClient, chat_id: int, user_id: int) -> bool:
    try:
        check = await bot.get_permissions(chat_id, user_id)
        return check
    except:
        return False

async def download_file(
    url: str,
    filename: str,
    callback=None,
) -> str or bool:
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        with open(filename, "wb") as file:
            for chunk in response.iter_content(chunk_size=1024):
                file.write(chunk)
                if callback:
                    downloaded_size = file.tell()
                    total_size = int(response.headers.get("content-length", 0))
                    await callback(downloaded_size, total_size, "Downloading")
        return filename
    except Exception as e:
        print(f"Error downloading file: {e}")
        return False

def download_image_to_bytesio(url: str, filename: str) -> BytesIO or None:
    try:
        response = requests.get(url)
        if response.status_code == 200:
            image_bytes = BytesIO(response.content)
            image_bytes.name = filename
            return image_bytes
        else:
            return None
    except:
        return None
