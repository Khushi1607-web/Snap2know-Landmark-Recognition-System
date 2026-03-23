import tensorflow as tf
import numpy as np
import cv2
import os

MODEL_PATH = "landmark_model.h5"
LABELS_PATH = "labels.txt"

def load_labels():
    with open(LABELS_PATH, "r") as f:
        return [line.strip() for line in f.readlines()]

def predict_landmark(image_path):
    model = tf.keras.models.load_model(MODEL_PATH)
    labels = load_labels()

    img = cv2.imread(image_path)
    img = cv2.resize(img, (224, 224))
    img = img / 255.0
    img = np.expand_dims(img, axis=0)

    predictions = model.predict(img)[0]
    idx = np.argmax(predictions)
    confidence = predictions[idx]

    return labels[idx], float(confidence)

if _name_ == "_main_":
    path = input("Enter image path: ")
    label, conf = predict_landmark(path)
    print(f"Predicted: {label} ({conf*100:.2f}% confidence)")