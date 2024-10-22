import os
import cv2
import requests
from flask import send_from_directory
from twilio.rest import Client as TwilloClient
from gradio_client import Client as GradioApp, file
from dotenv import load_dotenv

load_dotenv()

# Load environment variables for Twilio credentials
ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")

# Initialize Twilio client for sending messages (WhatsApp)
twilio_client = TwilloClient(ACCOUNT_SID, AUTH_TOKEN)

# Initialize Gradio client for Virtual Try-On
virtual_tryon_client = GradioApp("Nymbo/Virtual-Try-On")

def send_result(phone_number, media_url):
    """
    Sends the result of the virtual try-on back to the user via WhatsApp using Twilio.
    """
    try:
        twilio_client.messages.create(
            body="✨ Your Virtual Try-On is Ready! ✨",
            media_url=[media_url],
            to=phone_number,
            from_='whatsapp:+14155238886',  # Twilio's WhatsApp number
        )
        print("Result Sent!!")
    except Exception as e:
        print(f"Error sending result: {e}")

def perform_virtual_tryon(user_image_url, garment_image_url):
    """
    Performs the virtual try-on by sending the user and garment images to the Gradio model.
    The result is saved in the 'static' directory and the file path is returned.
    """
    # Download media locally
    user_image_path = save_media(user_image_url, 'user_image.jpg')
    garment_image_path = save_media(garment_image_url, 'garment_image.jpg')

    if user_image_path is None or garment_image_path is None:
        return None

    try:
        # Call Gradio model for virtual try-on prediction
        result = virtual_tryon_client.predict(
            dict={"background": file(user_image_path), "layers": [], "composite": None},
            garm_img=file(garment_image_path),
            garment_des="Custom garment description",
            is_checked=True,
            is_checked_crop=False,
            denoise_steps=30,
            seed=42,
            api_name="/tryon"
        )

        # Process the result from the model
        if result and len(result) > 0:
            tryon_image_path = result[0]
            static_dir = 'static'
            
            # Create 'static' directory if it doesn't exist
            if not os.path.exists(static_dir):
                os.makedirs(static_dir)

            # Save the result image
            if os.path.exists(tryon_image_path):
                img = cv2.imread(tryon_image_path)
                output_image_path = os.path.join(static_dir, 'result.png')
                cv2.imwrite(output_image_path, img)
                return f"/static/result.png" 
            else:
                return None
        return None
    except Exception as e:
        print(f"Error during try-on process: {e}")
        return None

def save_media(media_url, file_name):
    try:
        # Parse Twilio media URL to extract message and media SIDs
        message_sid = media_url.split('/')[-3]
        media_sid = media_url.split('/')[-1]

        # Fetch media from Twilio API
        media = twilio_client.api.accounts(ACCOUNT_SID).messages(message_sid).media(media_sid).fetch()
        media_uri = media.uri.replace('.json', '')  # Adjust the URI for media content
        image_url = f"https://api.twilio.com{media_uri}"

        # Download the image content
        response = requests.get(image_url, auth=(ACCOUNT_SID, AUTH_TOKEN))
        if response.status_code == 200:
            # Save the image to a local file
            with open(file_name, 'wb') as file:
                file.write(response.content)
            return file_name
        else:
            return None
    except Exception as e:
        print(f"Error downloading media: {e}")
        return None

def serve_static_file(filename):
    static_file_path = os.path.join('static', filename)
    if os.path.exists(static_file_path):
        return send_from_directory('static', filename, mimetype='image/png')
    else:
        return "File not found", 404
