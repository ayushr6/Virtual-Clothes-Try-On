# Virtual Try-On Assistant

This project is a Flask-based application that integrates **Twilio** for *messaging* and **Gradio** for *virtual try-on functionality*. Users can upload images of themselves and garments, and the application will perform a virtual try-on, sending the result back via **WhatsApp**.

We have utilized the following *HuggingFace Spaces*:
- `Nymbo/Virtual-Try-On`, @ [HugginFace Space](https://huggingface.co/spaces/Nymbo/Virtual-Try-On).
- `Nymbo/Mistral-Small-22B`, @ [HugginFace Space](https://huggingface.co/spaces/Nymbo/Mistral-Small-22B).

### Prerequisites
Before you begin, ensure you have the following:

- Python 3.9 or higher
- Pip (Python package installer)
- A Twilio account
- Ngrok account (optional for local testing)

### Setup Twilio
- Create a **Twilio Account**:
- Go to **Twilio** and sign up for a [new account](https://www.twilio.com/login).
- Get a [**Send a Whatsapp Message**](https://console.twilio.com/us1/develop/sms/try-it-out/whatsapp-learn?frameUrl=%2Fconsole%2Fsms%2Fwhatsapp%2Flearn%3Fx-target-region%3Dus1) section.

- Now, follow the instructions on the display.

### Get Twilio Account SSID & Auth Token

- Redirect to [Twilio console](https://console.twilio.com/), and you will find your *Twilio Account SSID & Auth Token*.
- Note the *Twilio Account SSID & Auth Token* (will be required in further steps).


### Setup Ngrok
- Setup Ngrok: Open [Ngrok Downloads](https://ngrok.com/download)
- Login to Ngrok and note down the *Ngrok Auth Token*.


### Add Ngrok Auth token in terminal

- Open terminal, run:

```
    ngrok config add-authtoken TOKEN_VALUE
```

## Installation

- Clone repository

```
    git clone https://github.com/ayushr6/Virtual-Clothes-Try-On
```
```
    cd Virtual-Clothes-Try-On 
```

- Create & Activate environment

```
    conda create -n env-name python=3.x
```

```
    conda activate env-name
```

- Install requirements

```
    pip install -r requirements.txt
```

- Create an `.env` file and add the following **Auth**, & **Tokens**

```
    TWILIO_ACCOUNT_SID=
    TWILIO_AUTH_TOKEN=
    NGROK_URL=
```


*NOTE: to get the `NGROK_URL`, run the below command:*

```
    ngrok http 8080
```

Under the *Ngork details*, copy the `URL` from in-front of `Forwarding` and set the `NGROK_URL` environment variable.

*Note: With this command, your local server will be accessible to everyone.*

*Everytime you restart your `ngrok server`, new `url` will be generated. So, don't forget to update the `env` and `Twilio Sandbox Configuration`. 

## Run the Application

### Flask Application

```
    python app.py
```

### Ngrok server

```
    ngrook http 8080
```

## How to Use?

- After setting up all environment variables, and twilio account.
- Open Twilio chat on whatsapp, and type "Hi" or send an image.
- Share your image or someone's else.
- Share a garment image you want to try-on.

Thant's all, it is that simple!!