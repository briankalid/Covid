import streamlit as st
import pandas as pd
import pandas_redshift as pr
from datetime import datetime
import time
import os
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="Real-Time Covid19 Dashboard",
    page_icon="✅",
    layout="wide",
)

def connect_to_redshift():
    pr.connect_to_redshift(dbname='dev',
                        host=os.getenv("REDSHIFT_HOST"),
                        port=5439,
                        user=os.getenv("REDSHIFT_USER"),
                        password=os.getenv("REDSHIFT_PASSWORD"))


def get_data():
    # Reconnect to Redshift to ensure the connection is fresh
    connect_to_redshift()
    df = pr.redshift_to_pandas('select * from timeline_positive')
    df['fecha_sintomas'] = pd.to_datetime(df['fecha_sintomas'])
    pr.close_up_shop()
    return df

df = get_data()

st.title("Real-Time / Live Covid19 Dashboard")

st.sidebar.subheader('Ubicacion')
country_filter = st.sidebar.multiselect("Select the country", pd.unique(df["country"]), default=pd.unique(df["country"]))
state_filter =  st.sidebar.multiselect("Select the state", pd.unique(df[df["country"].isin(country_filter)]["entidad_um"]), default= pd.unique(df[df["country"].isin(country_filter)]["entidad_um"]))


start_date = st.date_input('Start date:', value=pd.to_datetime(df['fecha_sintomas']).min().date())
end_date = st.date_input('End date:', value=pd.to_datetime(df['fecha_sintomas']).max().date())

metric_placeholder = st.empty()
line_chart_placeholder = st.empty()
map_placeholder = st.empty()

while True:
    print(datetime.now(), "init get_data")
    df = get_data()
    print(datetime.now(), "init graphic")
    filtered_df = df[(df["country"].isin(country_filter)) & 
                (df["entidad_um"].isin(state_filter)) & 
                (df["fecha_sintomas"] >= pd.to_datetime(start_date)) & 
                (df["fecha_sintomas"] <= pd.to_datetime(end_date))]

    df_line_chart = filtered_df[['fecha_sintomas','positive_cases']].groupby('fecha_sintomas').sum()
    df_map = filtered_df[["latitud","longitud","positive_cases"]].groupby(["latitud","longitud"]).sum().reset_index()
    df_map["positive_cases"] = df_map["positive_cases"]/5
    # with placeholder.container():
    metric_placeholder.metric(label="Casos Covid19 confirmados",value=sum(filtered_df["positive_cases"]))
    line_chart_placeholder.line_chart(data=df_line_chart)
    map_placeholder.map(data=df_map,latitude="latitud",longitude="longitud",size="positive_cases", use_container_width=True)

    print(datetime.now(), "end graphic")
    time.sleep(10)