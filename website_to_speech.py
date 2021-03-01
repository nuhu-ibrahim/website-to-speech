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
        print("Sorry, an error occureed while converting webpage to image using Restpack, please try again.")
        return False
    else:
        response.raise_for_status()

        image_properties = response.json()

        image_location = image_properties['image']

        r = requests.get(image_location, allow_redirects=True)

        open('website-image.jpg', 'wb').write(r.content)

    return True

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

    return True, prediction

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
        print("Sorry, we were unable to convert your website to speech, please try again.")
        return False

def playing_sound():
    path = str(Path("audio.wav").resolve())
    path = path.replace(" ", "%20")

    playsound(path)

# Do not alter the code below here!
# If you are interested in how it works, read the module documentation for argparse.
# argparse makes writing reasonably robust command line tools pretty easy.

if __name__ == '__main__':
    # Importing here is not standard, but convenient for this assignment.
    import argparse
    parser = argparse.ArgumentParser(description='Converts a webpage to speech')
    parser.add_argument('website', type=str, default='https://nuhuibrahim.com', nargs='?',
                    help='The web address of the page you will like to predict')

    args = parser.parse_args()
    website = args.website

    restpack_key = 'Restpack API Key'
    cloudmersive_key = 'Cloudmersive API Key'
    ibm_text_to_speech_key = 'IBM API Key'
    ibm_service_url = 'IBM Service URL'

    if convert_website_to_image(restpack_key, website):
        condition, text = predict_image_to_caption(cloudmersive_key)
        if condition:
            if text_to_voice(ibm_text_to_speech_key, ibm_service_url, text):
                playing_sound()