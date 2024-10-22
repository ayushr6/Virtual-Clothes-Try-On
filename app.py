import os
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from dotenv import load_dotenv

# Custom utility imports
from utils import send_result, perform_virtual_tryon, serve_static_file
from llm_handler import handle_user_message

load_dotenv()

app = Flask(__name__)

# Dictionary to track session data for users
session_data = {}

# Ngrok public URL to serve the static results (set via .env file)
NGROK_URL = os.getenv("NGROK_URL")

@app.route('/', methods=['POST'])
def process_request():
    sender = request.form.get('From')
    media_link = request.form.get('MediaUrl0')
    user_message = request.form.get('Body', '').strip().lower()

    # Initialize Twilio messaging response object
    twilio_resp = MessagingResponse()

    if sender not in session_data:
        session_data[sender] = {}

    # Case 1: Text message handling via LLM (no media link)
    if user_message and not media_link:
        # If expecting a response about media type (person or garment)
        if 'pending_media' in session_data[sender] and 'expecting_response' in session_data[sender]:
            # User confirms the image is of a person
            if user_message == '0':
                # Update the person image or set it for the first time
                if 'user_image' in session_data[sender]:
                    session_data[sender]['user_image'] = session_data[sender]['pending_media']
                    twilio_resp.message("New person image received! Please send the garment image.")
                else:
                    session_data[sender]['user_image'] = session_data[sender]['pending_media']
                    twilio_resp.message("Person image received! Please send the garment image.")
                del session_data[sender]['pending_media']
                del session_data[sender]['expecting_response']

            # User confirms the image is of a garment
            elif user_message == '1':
                # Update the garment image or set it for the first time
                if 'garment_image' in session_data[sender]:
                    session_data[sender]['garment_image'] = session_data[sender]['pending_media']
                    twilio_resp.message("New garment image received! Please send the person image.")
                else:
                    session_data[sender]['garment_image'] = session_data[sender]['pending_media']
                    twilio_resp.message("Garment image received! Please send the person image.")
                del session_data[sender]['pending_media']
                del session_data[sender]['expecting_response']

            # If both images (person and garment) are received, perform virtual try-on
            if 'user_image' in session_data[sender] and 'garment_image' in session_data[sender]:
                tryon_result_url = perform_virtual_tryon(session_data[sender]['user_image'], session_data[sender]['garment_image'])
                if tryon_result_url:
                    send_result(sender, f"{NGROK_URL}/static/result.png")
                    twilio_resp.message("🎉✨ Your Virtual Try-On is Ready! ✨🎉")
                else:
                    twilio_resp.message("Error during virtual try-on. Please Restart.")
                del session_data[sender]  # Clear session after completion

        # Handle normal text messages using the LLM
        else:
            reply_message = handle_user_message(user_message)
            twilio_resp.message(reply_message)

    # Case 2: Media message handling (image processing)
    elif media_link:
        # If either person or garment image is missing, prompt user for media type
        if 'user_image' not in session_data[sender] or 'garment_image' not in session_data[sender]:
            session_data[sender]['pending_media'] = media_link
            session_data[sender]['expecting_response'] = True
            twilio_resp.message("Is this a person image? Reply with '0' for person, '1' for garment.")

    return str(twilio_resp)


# Route for serving static files (like the virtual try-on result image)
@app.route('/static/<path:filename>')
def serve_file(filename):
    return serve_static_file(filename)


# Start the Flask app on port 8080
if __name__ == '__main__':
    app.run(port=8080)
