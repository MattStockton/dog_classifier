import requests
import base64
import json

# Function to encode the image
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

# Path to your image file
image_path = "./image.jpeg"

# Encode the image
base64_image = encode_image(image_path)

# API endpoint
url = "http://localhost:5001/classify"

# Data to be sent in JSON format
payload = json.dumps({
    "image": base64_image
})

# Headers
headers = {
    'Content-Type': 'application/json'
}

# Send POST request
response = requests.post(url, headers=headers, data=payload)

# Check if the request was successful
if response.status_code == 200:
    # Print the response from the API
    print(json.dumps(response.json(), indent=2))
else:
    print(f"Request failed with status code: {response.status_code}")
    print(response.text)
