from flask import Flask, request, jsonify
import torch
import torchvision.transforms as transforms
from torchvision.models import resnet50
from PIL import Image
import base64
import io

app = Flask(__name__)

# Load pre-trained ResNet50 model
model = resnet50(pretrained=True)
model.eval()

# Define image transformations
transform = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

# Classes we're interested in (assuming indices from ImageNet)
classes = {
    199: 'dog',
    281: 'cat'
}

@app.route('/classify', methods=['POST'])
def classify_image():
    # Check if image data is in the request
    if 'image' not in request.json:
        return jsonify({'error': 'No image data provided'}), 400

    # Decode the base64 image
    try:
        image_data = base64.b64decode(request.json['image'])
        image = Image.open(io.BytesIO(image_data))
    except:
        return jsonify({'error': 'Invalid image data'}), 400

    # Preprocess the image
    input_tensor = transform(image)
    input_batch = input_tensor.unsqueeze(0)

    # Make prediction
    with torch.no_grad():
        output = model(input_batch)

    # Get probabilities for dog and cat
    probabilities = torch.nn.functional.softmax(output[0], dim=0)
    dog_prob = probabilities[199].item()
    cat_prob = probabilities[281].item()

    # Determine if it's a dog (True) or cat (False)
    is_dog = dog_prob > cat_prob

    return jsonify({
        'is_dog': is_dog,
        'dog_probability': dog_prob,
        'cat_probability': cat_prob
    })

if __name__ == '__main__':
    app.run(debug=True, port=5001)
