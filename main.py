import os
import requests
import feedparser
from pydub import AudioSegment
import speech_recognition as sr

def download_podcast_from_rss_feed(rss_feed_url, path_to_directory):
    # Parse the RSS feed
    feed = feedparser.parse(rss_feed_url)

    # Create directory if it doesn't exist
    os.makedirs(path_to_directory, exist_ok=True)

    for entry in feed.entries:
        # Get the title and audio URL
        title = entry.title
        audio_url = entry.enclosures[0].href if entry.enclosures else None

        if audio_url:
            # Generate a safe filename from the title
            filename = os.path.join(path_to_directory, f"{title}.mp3")

            # Check if the file already exists
            if os.path.exists(filename):
                print(f"File already exists: {filename}, skipping...")
                continue

            # Download the audio file
            print(f"Downloading {title}...")
            response = requests.get(audio_url, stream=True)

            if response.status_code == 200:
                with open(filename, "wb") as f:
                    for chunk in response.iter_content(1024):
                        f.write(chunk)
                print(f"Downloaded: {filename}")
            else:
                print(f"Failed to download {title}")

def convert_and_transcribe(path_to_directory):
    recognizer = sr.Recognizer()
    
    for filename in os.listdir(path_to_directory):
        if filename.endswith(".mp3"):
            mp3_path = os.path.join(path_to_directory, filename)
            wav_path = mp3_path.replace(".mp3", ".wav")
            text_path = mp3_path.replace(".mp3", ".txt")
            
            # Convert MP3 to WAV
            mp3_audio = AudioSegment.from_mp3(mp3_path)
            mp3_audio.export(wav_path, format="wav")
            
            # Transcribe WAV to text
            with sr.AudioFile(wav_path) as source:
                audio_data = recognizer.record(source)
                text = recognizer.recognize_google(audio_data)
            
            # Save the transcribed text to a file
            with open(text_path, "w") as text_file:
                text_file.write(text)
            print(f"Transcribed and saved: {text_path}")

download_podcast_from_rss_feed("https://feeds.feedburner.com/XadrezVerbal", "XadrezVerbal")

convert_and_transcribe("XadrezVerbal")
