import streamlit as st
from sqlalchemy import create_engine
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
from plotly.subplots import make_subplots


import datetime as dt
import sqlite3

def _max_width_():
    max_width_str = f"max-width: 2000px;"
    st.markdown(
        f"""
    <style>
    .reportview-container .main .block-container{{
        {max_width_str}
    }}
    </style>    
    """,
        unsafe_allow_html=True,
    )

def narrow(conn, left_bound, right_bound):
	try:
		df = pd.read_sql_query("SELECT * FROM d1 WHERE timestamp BETWEEN %(left)s AND %(right)s", conn, params={"left" : left_bound, "right" : right_bound})
		return df
	except:
		st.error("There is no data in given time range")

def graph(df):
	try:
		fig = make_subplots(rows=1, cols=3)
		fig.add_trace(go.Scatter(x=df['timestamp'], y=df['temperature'], name='Temperature', mode='markers'),
					row=1, col=1)
		fig.add_trace(go.Scatter(x=df['timestamp'], y=df['pressure'], name='Pressure', mode='markers'),
					row=1, col=2)
		fig.add_trace(go.Scatter(x=df['timestamp'], y=df['no2'], name='NO2', mode='markers'),
					row=1, col=3)

		fig.update_xaxes(rangeslider_visible=True)
		fig.update_xaxes(title_text="Time", row=1, col=1)
		fig.update_xaxes(title_text="Time", row=1, col=2)
		fig.update_xaxes(title_text="Time", row=1, col=3)

		fig.update_yaxes(title_text="Temperature (°F)", row=1, col=1)
		fig.update_yaxes(title_text="Pressure (mmHg)", row=1, col=2)
		fig.update_yaxes(title_text="NO2 Concentration (ppm)", row=1, col=3)

		fig.update_layout(title_text="Sensor Data", font_family="Georgia", width= 1225, height=560)
		st.plotly_chart(fig)
	
	except:
		pass


if __name__ == "__main__":
	with open("url.txt", 'r') as file:
		url = file.read()
	engine = create_engine(url, echo=False)
	conn = engine.raw_connection()

	_max_width_()
	st.title('Dashboard')

	st.write("Last updated: " + dt.datetime.now().strftime("%m/%d/%Y, %H:%M:%S"))

	date = st.sidebar.date_input('What day?', dt.date.today())
	left_bound = st.sidebar.time_input('Left bound', dt.time(11, 30))
	right_bound = st.sidebar.time_input('Right bound', dt.time(11, 40))

	left_bound = str(date) + " " + str(left_bound)
	right_bound = str(date) + " " + str(right_bound)

	df = narrow(conn, left_bound, right_bound)

	graph(df)

	df
	
