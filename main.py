import re
import requests
import os
from pyrogram import Client, filters
from bs4 import BeautifulSoup

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
    await message.reply("Send me a TeraBox or TeraFileShare link, and I'll download the video for you!")

# Function to handle links
@app.on_message(filters.text)
async def handle_link(client, message):
    url = message.text
    # Use regex to validate the URL
    if re.match(VALID_URL_PATTERN, url):
        await message.reply("Attempting to download the video...")

        try:
            # Extract and download the video file
            file_name = download_video(url)

            # Send the downloaded file to the user
            await app.send_document(message.chat.id, file_name)

            # Clean up the downloaded file after sending
            os.remove(file_name)
        except Exception as e:
            await message.reply(f"Failed to download the video. Error: {e}")
    else:
        await message.reply("Please send a valid TeraBox or TeraFileShare link.")

# Function to extract download link and download the video
def download_video(url):
    # Send a GET request to the link
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception("Failed to load the page")

    # Parse the HTML to find the actual download link (using BeautifulSoup)
    soup = BeautifulSoup(response.content, "html.parser")
    
    # Find the download link in the page (example, adjust selector as necessary)
    # Assuming <a> tag contains the final download link
    download_link = soup.find("a", {"class": "download-button-class"})  # Example; adjust according to the site’s structure
    if not download_link:
        raise Exception("Download link not found")

    download_url = download_link['href']  # Extract the href attribute

    # Now download the video from the extracted link
    video_response = requests.get(download_url, stream=True)

    # Save the file locally
    file_name = os.path.join(DOWNLOAD_DIR, "downloaded_video.mp4")  # Change extension based on file type
    with open(file_name, "wb") as f:
        for chunk in video_response.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)

    return file_name

if __name__ == "__main__":
    if not os.path.exists(DOWNLOAD_DIR):
        os.makedirs(DOWNLOAD_DIR)

    # Run the Pyrogram bot
    app.run()
