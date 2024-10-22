from gradio_client import Client as GradioClient

# Initialize Gradio client for LLM
text_model_client = GradioClient("Nymbo/Mistral-Small-22B")

def handle_user_message(user_input):
    # System prompt for the virtual try-on assistant
    system_prompt = """
    You are a virtual try-on assistant.
    User will share his/her image along with garment image, and guide the user accordingly.

    User Instructions:
    We do not support media link. Directly Upload media.
    """

    # Check if the user sent a link instead of media
    if 'http' in user_input:
        return "Please do not send links. Kindly upload the image directly."

    try:
        # Call the LLM API with user input and system prompt
        result = text_model_client.predict(
            message=user_input,
            system_message=system_prompt,
            max_tokens=512,
            temperature=0.7,
            top_p=0.95,
            api_name="/chat"
        )
        return result
    except Exception as e:
        print(f"Error in processing user message: {e}")
        return "Apologies, I couldn't process your request."
