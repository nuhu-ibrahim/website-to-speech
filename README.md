# Website to Speech
Created by [Nuhu Ibrahim](https://nuhuibrahim.com)

## Project Goals
The goal of this project is to develop a python script that:
1. Converts a valid web URL into an image,
2. Automatically Describe the image using a caption, 
3. and coverts the caption into audio so that it could be read aloud and listened to. 

This project aims to assist visually impaired people in gaining a general overview of a website so that they can infer if the website is worth spending time on or not. It is generally known that it takes a long time for people with visual impairment to go through a webpage completely.

Appreciation to the [Public APIs Github Repository](https://github.com/public-apis/public-apis.git) as all the APIs used in this project was first found there.

## Setting up the API Keys
### Part 1: Converting a website to an image
You will need to create an account with restpack [here](https://restpack.io/console/register) and then assign your access token to the "restpack_api_key" variable in the code.

### Part 2: Automatically describing the image using a simple caption
You will need to register with Cloudmersive website [here](https://account.cloudmersive.com/signup), create an api key and assign it to the "cloudmersive_api_key" variable in the code.

### Part 3: Converting the caption into an audio so that it could be read aloud
You need to first create an acount on the IBM text to speech website [here](https://cloud.ibm.com/registration?target=%2Fdocs%2Ftext-to-speech%2Fgetting-started.html), create an api key and then assign the key to the "ibm_text_to_speech_api_key" variable in the code below.

## Running the program
```bash
# Run the following commands on your terminal from the project root directory.
python3 website_to_speech.py <URL>

#URL is the web address of the page whose prediction you want to listen to aloud.

# ...and that is all.
```
## Thank you
If you find this code interesting or useful, kindly click on the like button and follow me for more.
