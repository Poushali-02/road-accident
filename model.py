import tensorflow as tf
from tensorflow import keras

# Load the model and pipeline
model = keras.models.load_model('model.keras')

def prediction(input_data):
    prediction = model.predict(input_data, verbose=0)
    return prediction[0][0]