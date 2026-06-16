import streamlit as st
import pickle
import requests
import matplotlib.pyplot as plt

# ---------------- PAGE SETUP ----------------
st.set_page_config(
    page_title="AI Crop & Weather App",
    page_icon="🌾",
    layout="wide"
)

# ---------------- LOAD MODEL ----------------
model = pickle.load(open("model.pkl", "rb"))

# ---------------- WEATHER FUNCTION ----------------
def get_weather(city):
    api_key = "e5e2b84cc88735ed32dfd7195c530ea7"

    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

    response = requests.get(url)
    data = response.json()

    if response.status_code == 200:
        return {
            "temp": data["main"]["temp"],
            "humidity": data["main"]["humidity"],
            "desc": data["weather"][0]["description"]
        }
    else:
        return None


# ---------------- TITLE ----------------
st.title("🌾 AI Crop & Weather Prediction App")
st.write("AI + Weather + Graph Dashboard")

st.markdown("---")

# ---------------- WEATHER SECTION ----------------
st.subheader("🌦️ Live Weather Panel")

city = st.text_input("Enter City Name")

if st.button("Get Weather"):

    if city == "":
        st.warning("Please enter a city name")

    else:
        weather = get_weather(city)

        if weather:
            st.success(f"🌡️ Temperature: {weather['temp']} °C")
            st.info(f"💧 Humidity: {weather['humidity']} %")
            st.write(f"🌤️ Condition: {weather['desc']}")

        else:
            st.error("City not found")


st.markdown("---")

# ---------------- CROP INPUTS ----------------
st.subheader("🌱 Crop Prediction Inputs")

col1, col2 = st.columns(2)

with col1:
    N = st.number_input("Nitrogen (N)")
    P = st.number_input("Phosphorus (P)")
    K = st.number_input("Potassium (K)")
    ph = st.number_input("pH Value")

with col2:
    temperature = st.number_input("Temperature (°C)")
    humidity = st.number_input("Humidity (%)")
    rainfall = st.number_input("Rainfall (mm)")

st.markdown("---")

# ---------------- GRAPH SECTION ----------------
st.subheader("📊 Soil Data Visualization")

if st.button("Show Graph"):

    labels = ["Nitrogen", "Phosphorus", "Potassium"]
    values = [N, P, K]

    fig, ax = plt.subplots()

    ax.bar(labels, values)

    ax.set_title("Soil Nutrient Levels")
    ax.set_ylabel("Value")

    st.pyplot(fig)

st.markdown("---")

# ---------------- AI ASSISTANT ----------------
st.subheader("🧠 AI Crop Assistant")

question = st.text_input(
    "Ask something about farming (example: Which crop should I grow?)"
)

if st.button("Ask AI Assistant"):

    if question:

        if "crop" in question.lower():
            st.info(
                "Based on soil and weather conditions, suitable crops may include Rice, Wheat, Maize, Cotton, Coconut and others."
            )

        elif "weather" in question.lower():
            st.info(
                "Weather affects crop growth. Check temperature, humidity and rainfall before farming decisions."
            )

        else:
            st.info(
                "I can help with crop prediction and weather-related farming advice."
            )

st.markdown("---")

# ---------------- PREDICTION ----------------
if st.button("🌾 Predict Crop"):

    if rainfall > 200:
        crop = "Rice"

    elif temperature > 30:
        crop = "Cotton"

    elif humidity > 80:
        crop = "Coconut"

    elif ph < 6:
        crop = "Tea"

    elif N > 100:
        crop = "Maize"

    else:
        crop = "Wheat"

    st.success(f"🌾 Recommended Crop: {crop}")