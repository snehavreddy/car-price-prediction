import os

import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

API_URL = os.getenv("API_URL", "http://localhost:8000")
API_KEY = os.getenv("API_KEY")


st.set_page_config(
    page_title="Car Price Prediction",
    page_icon="🚗"
)

st.title("🚗 Car Price Prediction")

st.write("Login to use the car price prediction service.")


# --------------------------------
# Login
# --------------------------------

st.header("Login")

username = st.text_input("Username")
password = st.text_input("Password", type="password")

if st.button("Login"):

    response = requests.post(
        f"{API_URL}/login",
        json={
            "username": username,
            "password": password
        }
    )

    if response.status_code == 200:

        data = response.json()

        if "access_token" in data:
            st.session_state["token"] = data["access_token"]
            st.success("Login successful! 🎉")
        else:
            st.error(data.get("error", "Invalid credentials"))

    else:
        st.error(f"Login failed: {response.status_code}")


# --------------------------------
# Car Details
# --------------------------------

if "token" in st.session_state:

    st.divider()

    st.header("🚘 Car Details")

    company = st.text_input("Company", "Maruti")

    year = st.number_input(
        "Year",
        min_value=1990,
        max_value=2026,
        value=2020
    )

    owner = st.selectbox(
        "Owner",
        [
            "First Owner",
            "Second Owner",
            "Third Owner",
            "Fourth & Above Owner",
            "Test Drive Car"
        ]
    )

    fuel = st.selectbox(
        "Fuel",
        [
            "Petrol",
            "Diesel",
            "CNG",
            "LPG",
            "Electric"
        ]
    )

    seller_type = st.selectbox(
        "Seller Type",
        [
            "Individual",
            "Dealer",
            "Trustmark Dealer"
        ]
    )

    transmission = st.selectbox(
        "Transmission",
        [
            "Manual",
            "Automatic"
        ]
    )

    km_driven = st.number_input(
        "KM Driven",
        min_value=0.0,
        value=45000.0
    )

    mileage_mpg = st.number_input(
        "Mileage (MPG)",
        min_value=0.0,
        value=50.0
    )

    engine_cc = st.number_input(
        "Engine (CC)",
        min_value=0.0,
        value=1200.0
    )

    max_power_bhp = st.number_input(
        "Max Power (BHP)",
        min_value=0.0,
        value=80.0
    )

    torque_nm = st.number_input(
        "Torque (Nm)",
        min_value=0.0,
        value=100.0
    )

    seats = st.number_input(
        "Seats",
        min_value=1.0,
        max_value=20.0,
        value=5.0
    )

    st.divider()

    if st.button("🚀 Predict Price"):

        payload = {
            "company": company,
            "year": year,
            "owner": owner,
            "fuel": fuel,
            "seller_type": seller_type,
            "transmission": transmission,
            "km_driven": km_driven,
            "mileage_mpg": mileage_mpg,
            "engine_cc": engine_cc,
            "max_power_bhp": max_power_bhp,
            "torque_nm": torque_nm,
            "seats": seats
        }

        headers = {
            "token": st.session_state["token"],
            "api-key": API_KEY
        }

        try:

            response = requests.post(
                f"{API_URL}/predict",
                json=payload,
                headers=headers
            )

            if response.status_code == 200:

                result = response.json()

                st.success(
                    f"💰 Predicted Price: ₹{result['predicted_price']}"
                )

            else:

                st.error(
                    f"Prediction failed: {response.text}"
                )

        except requests.exceptions.ConnectionError:

            st.error(
                "Could not connect to FastAPI."
            )