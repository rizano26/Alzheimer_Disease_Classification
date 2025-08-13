from flask import Flask, request, jsonify
import numpy as np
from PIL import Image
import io
from keras.layers import TFSMLayer 

# Inisialisasi Flask app
app = Flask(__name__)

# Load model untuk inference-only
model_path = "model/saved_model"
model = TFSMLayer(model_path, call_endpoint="serving_default")


# Mapping kelas
class_names = ['Mild Demented', 'Moderate Demented', 'Non Demented', 'Very Mild Demented']

# Fungsi preprocessing gambar
def preprocess_image(image_bytes):
    image = Image.open(io.BytesIO(image_bytes)).convert('RGB')
    image = image.resize((180, 180))
    image = np.array(image) / 255.0
    image = np.expand_dims(image, axis=0)
    return image

# Endpoint prediksi
@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']
    img_bytes = file.read()

    try:
        processed_image = preprocess_image(img_bytes)
        raw_output = model(processed_image)  
        prediction = raw_output['output_0'].numpy()  
        predicted_class = class_names[np.argmax(prediction)]
        confidence = float(np.max(prediction))

        return jsonify({
            'predicted_class': predicted_class,
            'confidence': confidence
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Run lokal
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
    
