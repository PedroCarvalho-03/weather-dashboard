import streamlit as st
import pandas as pd
import requests

#chave api
API_KEY = "06899b3d545c3d892ea50f9bca82a71e"

#textos
st.set_page_config(page_title="Clima", page_icon="🌤️", layout="centered")
st.title("⛅ Dashboard de previsão do tempo")

cidade = st.text_input("cidade","Belo Horizonte")
bt = st.button("Buscar")

def geocode(cidade):
    geocode_url = f"https://api.openweathermap.org/geo/1.0/direct?q={cidade}&appid={API_KEY}"
    response = requests.get(geocode_url)
    if response.status_code == 200:
        data = response.json()
        if data:
            return data[0]['lat'], data[0]['lon']
    return None, None

def get_forecast(lat, lon):
    forecast_url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={API_KEY}&lang=pt_br"
    response = requests.get(forecast_url)
    if response.status_code == 200:
        return response.json()
    return None


    response = requests.get(weather_url)
    if response.status_code == 200:
        return response.json()
    return None

if bt:
    lat, lon = geocode(cidade)
    if lat and lon:
        data = get_forecast(lat, lon)
        if data:
            def kelvin_to_celsius(temp_k):
                return temp_k - 273.15

           #previsão atual
            temp = kelvin_to_celsius(data['list'][0]['main']['temp'])
            desc = (data['list'][0]['weather'][0]['description'])
            feels_like = kelvin_to_celsius(data['list'][0]['main']['feels_like'])
            temp = kelvin_to_celsius(data['list'][0]['main']['temp'])
            st.subheader(f"Clima em {cidade}")
           
        else:
            st.error("Não foi possível obter os dados do clima.")
        
    else:
        st.error("Cidade não encontrada.")

    col1, col2, col3 = st.columns(3)
    col1.metric("Temperatura", f"{temp:.1f}°C")
    col2.metric("Sensação", f"{feels_like:.1f}°C")
    col3.metric("Umidade", f"{data['list'][0]['main']['humidity']}%")

    col1, col2, col3 = st.columns(3)
    col1.metric("Pressão", f"{data['list'][0]['main']['pressure']} hPa")
    col2.metric("Vento", f"{data['list'][0]['wind']['speed']} m/s")
    col3.metric("Descrição", desc.capitalize())

    icon_code = data["list"][0]["weather"][0]["icon"]
    icon_url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"
    st.image(icon_url)
    
       # previsão dos próximos dias
    st.markdown("### 📅 Previsão dos próximos dias")

    dias = {}
    for item in data["list"]:
        dt_txt = item["dt_txt"]
        dia = dt_txt.split(" ")[0]
        hora = dt_txt.split(" ")[1]

        # pega previsão do meio-dia (12:00:00) para representar o dia
        if hora == "12:00:00":
            dias[dia] = {
                "temp": kelvin_to_celsius(item["main"]["temp"]),
                "desc": item["weather"][0]["description"],
                "icon": item["weather"][0]["icon"]
            }

    if dias:
        tabs = st.tabs(list(dias.keys()))  # cria uma aba para cada dia
        for i, (dia, info) in enumerate(dias.items()):
            with tabs[i]:
                st.subheader(dia)
                col1, col2, col3 = st.columns(3)
                col1.metric("Temperatura", f"{info['temp']:.1f}°C")
                col2.metric("Descrição", info['desc'].capitalize())
                col3.image(f"http://openweathermap.org/img/wn/{info['icon']}@2x.png")
    else:
        st.error("Não foi possível obter os dados do clima.")
