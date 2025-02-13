import streamlit as st
import requests

def fetch_weather(city):
    api_key = '34f70e989995496aa7662156251302'  # Updated to WeatherAPI key
    base_url = "http://api.weatherapi.com/v1/current.json"
    url = f"{base_url}?key={api_key}&q={city}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        if response.status_code == 401:
            return {"error": "Invalid API key. Please check your credentials."}
        elif response.status_code == 404:
            return {"error": "City not found. Please check the name and try again."}
        else:
            return {"error": f"HTTP error occurred: {http_err}"}
    except requests.exceptions.RequestException as err:
        return {"error": f"Network error occurred: {err}"}

st.title("Weather Info App")
st.write("Enter a city name to get the current weather conditions.")

city = st.text_input("City Name:")

if st.button("Fetch Weather"):
    if city:
        data = fetch_weather(city)
        if "error" in data:
            st.error(data["error"])
        else:
            col1, col2 = st.columns(2)
            with col1:
                st.metric(label="Temperature", value=f"{data['current']['temp_c']}°C ({data['current']['temp_f']}°F)")
                st.metric(label="Humidity", value=f"{data['current']['humidity']}%")
                st.metric(label="Pressure", value=f"{data['current']['pressure_mb']} mb")
            with col2:
                st.metric(label="Wind Speed", value=f"{data['current']['wind_kph']} km/h ({data['current']['wind_mph']} mph)")
                st.write(f"Condition: {data['current']['condition']['text']}")
                st.metric(label="UV Index", value=f"{data['current']['uv']}")
                st.metric(label="Feels Like", value=f"{data['current']['feelslike_c']}°C ({data['current']['feelslike_f']}°F)")
            st.write(f"Location: {data['location']['name']}, {data['location']['region']}, {data['location']['country']}")
            st.write(f"Latitude: {data['location']['lat']}, Longitude: {data['location']['lon']}")
            st.write(f"Local Time: {data['location']['localtime']}")
    else:
        st.warning("Please enter a city name.")
