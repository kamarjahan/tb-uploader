
import os
import time
import requests
from pyrogram import Client, filters
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

# Your API credentials from my.telegram.org (for Pyrogram Client)
api_id = "17875613"
api_hash = "6798f54a7f74e94f2ef0923fba8a8377"
bot_token = "7290308705:AAFMacn2DefUe_2BgK2a_HP2z2CF1pdtY4g"

# Path to your ChromeDriver executable
CHROME_DRIVER_PATH = '/path/to/chromedriver'  # Update this path

# Create a new Pyrogram Client
app = Client("terabox_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

# Directory to save downloaded files temporarily
DOWNLOAD_DIR = "./downloads/"

# Function to initialize Selenium WebDriver
def init_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode to avoid opening a browser window
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    # Initialize WebDriver
    service = Service(CHROME_DRIVER_PATH)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

# Function to download video via TeraBox or TeraFileShare
def download_video(url):
    driver = init_driver()
    
    # Load the URL
    driver.get(url)
    time.sleep(5)  # Allow some time for the page to fully load
    
    # Extract the download link from the page (adjust selector as per the actual site structure)
    try:
        download_button = driver.find_element(By.CLASS_NAME, "download-button-class")  # Example selector; adjust as needed
        download_url = download_button.get_attribute("href")  # Get the direct download link
        
        if download_url:
            # Download the file using requests
            video_response = requests.get(download_url, stream=True)

            # Save the file locally
            file_name = os.path.join(DOWNLOAD_DIR, "downloaded_video.mp4")  # Change extension based on file type
            with open(file_name, "wb") as f:
                for chunk in video_response.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)

            driver.quit()  # Close the browser
            return file_name
        else:
            driver.quit()
            raise Exception("Download link not found")

    except Exception as e:
        driver.quit()
        raise e

# Command to start the bot
@app.on_message(filters.command("start"))
async def start(client, message):
    await message.reply("Send me a TeraBox or TeraFileShare link, and I'll download the video for you!")

# Function to handle links
@app.on_message(filters.text)
async def handle_link(client, message):
    url = message.text

    # Basic URL validation
    if "terabox.com" in url or "terafileshare.com" in url:
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

if __name__ == "__main__":
    if not os.path.exists(DOWNLOAD_DIR):
        os.makedirs(DOWNLOAD_DIR)

    # Run the Pyrogram bot
    app.run()
