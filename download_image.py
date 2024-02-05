import os
import json
import requests
from PIL import Image
from io import BytesIO
from urllib.parse import urlparse

def download_image(image_url, set_name, card_name, save_path):
    try:
        # Send a GET request to the image URL
        response = requests.get(image_url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Convert the image data to PNG format
            image = Image.open(BytesIO(response.content))

            # Create the directory for the set if it doesn't exist
            set_path = os.path.join(save_path, set_name)
            os.makedirs(set_path, exist_ok=True)

            # Save the image with a unique filename based on the card_name
            filename = f"{card_name.replace(' ', '_')}.png"
            full_path = os.path.join(set_path, filename)
            image.save(full_path, "PNG")

            print(f"Image downloaded successfully: {full_path}")
        else:
            print(f"Failed to download image: {image_url}")

    except Exception as e:
        print(f"An error occurred: {str(e)}")

def download_images_from_set(json_file_path, save_path):
    # Read JSON file
    with open(json_file_path, 'r') as file:
        data = json.load(file)

    # Prompt user for set name
    set_name = input("Enter the set name: ")

    # Download images for the specified set
    for item in data:
        if item['set_name'] == set_name and item['image_url']:
            download_image(item['image_url'], item['set_name'], item['card_name'], save_path)

# Example usage:
json_file_path = r'C:\Pictures\kamen rider\Python crawl img\battlespiritscraper\card_url.json'
save_path = r'C:\Pictures\kamen rider\Kamen_rider_sets'

download_images_from_set(json_file_path, save_path)
