import streamlit as st
import numpy as np
import tensorflow as tf
from PIL import Image
import json
import wikipedia
from googletrans import Translator
from gtts import gTTS
from io import BytesIO
import os
import base64

# ------------------- Load Model & Labels -------------------
MODEL_PATH = "landmark_model.keras"
LABELS_PATH = "labels.json"

@st.cache_resource
def load_model():
    return tf.keras.models.load_model(MODEL_PATH)

@st.cache_resource
def load_labels():
    with open(LABELS_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

model = load_model()
labels = load_labels()
translator = Translator()

# ------------------- Safe image loader -------------------
def load_image_base64(path):
    if os.path.exists(path):
        with open(path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return None

# ------------------- Landmark Prediction -------------------
def predict_landmark(img):
    img = img.resize((224, 224))
    arr = np.array(img) / 255.0
    arr = np.expand_dims(arr, axis=0)
    pred = model.predict(arr)[0]
    idx = np.argmax(pred)
    return labels[str(idx)]

# ------------------- Wikipedia Info Fetch -------------------
import requests

def fetch_wiki_info(query):
    try:
        headers = {
            "User-Agent": "Snap2Know (student project)"
        }

        # STEP 1: Search correct title
        search_url = "https://en.wikipedia.org/w/api.php"
        params = {
            "action": "query",
            "list": "search",
            "srsearch": query,
            "format": "json"
        }

        search_res = requests.get(search_url, params=params, headers=headers).json()

        if not search_res["query"]["search"]:
            return "No information found."

        # Get best match title
        title = search_res["query"]["search"][0]["title"]

        # STEP 2: Fetch summary
        summary_url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{title.replace(' ', '_')}"
        summary_res = requests.get(summary_url, headers=headers).json()

        return summary_res.get("extract", "No information found.")

    except Exception as e:
        return f"Error: {str(e)}"
# ------------------- Translation -------------------
def translate_text(text, lang):
    try:
        translated = translator.translate(text, dest=lang)
        return translated.text
    except:
        return "Translation unavailable."

# ------------------- Text to Speech -------------------
def generate_audio(text, lang_choice):
    try:
        tts = gTTS(text=text, lang=lang_choice)
        audio_bytes = BytesIO()
        tts.write_to_fp(audio_bytes)
        audio_bytes.seek(0)
        return audio_bytes
    except:
        return None

# ------------------- UI Settings ------------------
st.set_page_config(page_title="Snap2Know", layout="centered")

# ---- Custom Title Style ----
st.markdown("""
    <h1 style='text-align:center; color:#ffffff; background-color:#4A90E2; padding:12px; border-radius:8px;'>📷 Snap2Know</h1>
    <h3 style='text-align:center; color:#4A90E2;'>Your Smart Visual Tourist Guide</h3>
""", unsafe_allow_html=True)

# ---- Banner Image (Optional No Crash) ----
banner = load_image_base64("images/banner.jpg")
if banner:
    st.markdown(f"<img src='data:image/jpg;base64,{banner}' style='width:100%; border-radius:10px;'>", unsafe_allow_html=True)
else:
    st.info("⭐ Add banner image at:  images/banner.jpg")

# ---- Gallery Section ----
st.write("### 🌍 Popular Monuments")
gallery_path = "images/"
gallery_files = ["taj.jpg", "charminar.jpg", "qutub.jpg", "mysore.jpg"]

cols = st.columns(4)
for i, file in enumerate(gallery_files):
    if os.path.exists(os.path.join(gallery_path, file)):
        with cols[i]:
            st.image(os.path.join(gallery_path, file), width=150, caption=file.split(".")[0].title())
    else:
        with cols[i]:
            st.write("⚠ Missing")

st.write("---")

# ------------------- Upload & Output ------------------
uploaded = st.file_uploader("Upload Monument Image", type=["jpg", "jpeg", "png"])

language_map = {
    "English": "en", "Hindi": "hi", "Kannada": "kn", "Tamil": "ta",
    "Telugu": "te", "Malayalam": "ml", "Bengali": "bn", "Marathi": "mr",
    "Gujarati": "gu", "German": "de", "French": "fr"
}

lang = st.selectbox("Select Language", list(language_map.keys()))
lang_code = language_map[lang]

if uploaded:
    img = Image.open(uploaded)
    st.image(img, caption="Uploaded Image", use_column_width=True)

    with st.spinner("Identifying…"):
        name = predict_landmark(img)

    st.success(f"🏛 Identified Monument: {name}")

    with st.spinner("Fetching details…"):
        info = fetch_wiki_info(name)

    final_text = translate_text(info, lang_code)
    st.info(final_text)

    if st.button("🔊 Play Audio"):
        audio = generate_audio(final_text, lang_code)
        if audio:
            st.audio(audio, format="audio/mp3")
        else:
            st.error("Unable to play audio.")

st.write("---")
st.caption("Developed by ⭐ Khushi ✨ Kavana ✨ Kavanshree")