# You can run this with "python3 website_to_speech.py <URL>

# All imports are done here
# Imports for restpack
import requests
import json

# Imports for cloudmersive
import cloudmersive_image_api_client

# Imports for IBM Text to Speech
from ibm_watson import TextToSpeechV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

# Playing the sound
from pathlib import Path
from playsound import playsound

# Checking if url is valid
import validators

def validate_website(website):
    return validators.url(website)

def convert_website_to_image(restpack_api_key, website_to_predict):
    headers = {
        'Content-Type': 'application/json',
        'x-access-token': restpack_api_key
    }

    payload = {
        'url': website_to_predict,
        'json': 'true',
        'width': '1280',
        'height': '768',
        'format': 'jpg',
        'mode': 'viewport',
    }

    url = 'https://restpack.io/api/screenshot/v6/capture'

    response = requests.post(url, headers=headers, params={}, data=json.dumps(payload))

    if response.status_code != 200:
        return False, "Sorry, an error occureed while converting webpage to image, please try again."
    else:
        response.raise_for_status()

        image_properties = response.json()

        image_location = image_properties['image']

        r = requests.get(image_location, allow_redirects=True)

        open('website-image.jpg', 'wb').write(r.content)

    return True, ""

def predict_image_to_caption(cloudmersive_api_key):
    # Configure API key authorization: Apikey
    configuration = cloudmersive_image_api_client.Configuration()
    configuration.api_key['Apikey'] = cloudmersive_api_key

    # create an instance of the API class
    api_instance = cloudmersive_image_api_client.RecognizeApi(cloudmersive_image_api_client.ApiClient(configuration))
    image_file = "website-image.jpg"
    prediction = ""

    try:
        # Describe an image in natural language
        api_response = api_instance.recognize_describe(image_file)

        prediction = "Please listen to our prediction of your webpage. "

        if api_response.highconfidence == False:
            prediction = prediction + api_response.best_outcome.description + ". However, we are not very sure about this prediction."
        else:
            prediction = api_response.best_outcome.description
    except Exception as e:
        prediction = "Sorry, an error occured while we were trying to guess the content of the page. Please try again."

    return prediction

def text_to_voice(ibm_text_to_speech_api_key, service_url, prediction):
    authenticator = IAMAuthenticator(ibm_text_to_speech_api_key)
    text_to_speech = TextToSpeechV1(
        authenticator=authenticator
    )

    text_to_speech.set_service_url(service_url)

    try:
        with open('audio.wav', 'wb') as audio_file:
            audio_file.write(
                text_to_speech.synthesize(
                    prediction,
                    voice='en-US_AllisonV3Voice',
                    accept='audio/wav'
                ).get_result().content)

        return True
    except Exception as ex:
        return False

def playing_sound(audio_path):
    path = str(Path(audio_path).resolve())
    path = path.replace(" ", "%20")

    playsound(path)

# Do not alter the code below here!
# If you are interested in how it works, read the module documentation for argparse.
# argparse makes writing reasonably robust command line tools pretty easy.

if __name__ == '__main__':
    # Importing here is not standard, but convenient for this work.
    import argparse
    parser = argparse.ArgumentParser(description='Converts a webpage to speech')
    parser.add_argument('website', type=str, default='https://nuhuibrahim.com', nargs='?',
                    help='The web address of the page whose prediction you will like to listen to.')

    args = parser.parse_args()
    website = args.website

    # restpack_key = 'Restpack API Key'
    # cloudmersive_key = 'Cloudmersive API Key'
    # ibm_text_to_speech_key = 'IBM API Key'
    # ibm_service_url = 'IBM Service URL'

    restpack_key = 'Ulwu11xJs1O7VCuTVtALUmGoL2htvwPaD4t4SJbVdwfH1uQ6'
    cloudmersive_key = 'af5cf153-ba23-4b81-985f-aec482141d98'
    ibm_text_to_speech_key = 'Ea1FukVpYfI-O6iOPRyzgSFk7K1Z4HDjGpf8vDg6lY4j'
    ibm_service_url = 'https://api.eu-gb.text-to-speech.watson.cloud.ibm.com/instances/ae2db9df-e549-449c-a8bd-851130217ed0'

    if(validate_website(website) != True):
        playing_sound("malformed_website.wav")
    else:
        restpack_condition, restpack_text = convert_website_to_image(restpack_key, website)
        if restpack_condition:
            cloudmersive_text = predict_image_to_caption(cloudmersive_key)
            if text_to_voice(ibm_text_to_speech_key, ibm_service_url, cloudmersive_text):
                playing_sound("audio.wav")
            else:
                playing_sound("apology.wav")
        else:
            if text_to_voice(ibm_text_to_speech_key, ibm_service_url, restpack_text):
                playing_sound("audio.wav")
            else:
                playing_sound("apology.wav")
