import re
import requests
import os
from pyrogram import Client, filters

# Your API credentials from my.telegram.org (for Pyrogram Client)
api_id = "17875613"
api_hash = "6798f54a7f74e94f2ef0923fba8a8377"
bot_token = "7290308705:AAFMacn2DefUe_2BgK2a_HP2z2CF1pdtY4g"

# Create a new Pyrogram Client
app = Client("terabox_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

# Directory to save downloaded files temporarily
DOWNLOAD_DIR = "./downloads/"

# Regex pattern to match both TeraBox and TeraFileShare URLs
VALID_URL_PATTERN = r'(https?://)?(www\.)?(terabox\.com|terafileshare\.com)/[^\s]+'

# Command to start the bot
@app.on_message(filters.command("start"))
async def start(client, message):
    await message.reply("Send me a TeraBox or TeraFileShare link, and I'll download the file for you!")

# Function to handle links
@app.on_message(filters.text)
async def handle_link(client, message):
    url = message.text
    # Use regex to validate the URL
    if re.match(VALID_URL_PATTERN, url):
        await message.reply("Downloading the file...")

        try:
            # Download file from TeraBox or TeraFileShare (placeholder for actual download logic)
            file_name = download_file(url)

            # Send the downloaded file to the user
            await app.send_document(message.chat.id, file_name)

            # Clean up the downloaded file after sending
            os.remove(file_name)
        except Exception as e:
            await message.reply(f"Failed to download the file. Error: {e}")
    else:
        await message.reply("Please send a valid TeraBox or TeraFileShare link.")

# Placeholder for actual file download logic
def download_file(url):
    # Simulate downloading a file from TeraBox or TeraFileShare
    file_name = os.path.join(DOWNLOAD_DIR, "sample_file.txt")
    with open(file_name, "w") as f:
        f.write("This is a sample file.\n")
    return file_name

if __name__ == "__main__":
    if not os.path.exists(DOWNLOAD_DIR):
        os.makedirs(DOWNLOAD_DIR)

    # Run the Pyrogram bot
    app.run()
