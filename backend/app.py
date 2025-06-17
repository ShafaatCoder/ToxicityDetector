from flask import Flask, request, jsonify
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
import pickle
import re

app = Flask(__name__)

# Load model and tokenizer
model = load_model("toxicity_model.h5")
with open('tokenizer.pickle', 'rb') as handle:
    tokenizer = pickle.load(handle)

def predict_toxicity(text):
    sequence = tokenizer.texts_to_sequences([text])
    padded = pad_sequences(sequence, maxlen=100)
    prediction = model.predict(padded)[0][0]
    return prediction

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    text = data['text']
    score = predict_toxicity(text)
    return jsonify({
        "text": text,
        "is_toxic": bool(score > 0.5),
        "confidence": float(score)
    })

if __name__ == '__main__':
    app.run(debug=True)