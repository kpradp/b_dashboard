import matplotlib
import numpy as np
import requests
import pandas as pd
import streamlit as st
import playfab
import altair as alt

months = (
	'Select Month',
	'Jan',
	'Feb',
	'Mar',
	'Apr'
)

# data_report_url_from_server ={}
playfab.PlayFabSettings.TitleId = "1d015"
playfab.PlayFabSettings.DeveloperSecretKey = "Y5TDEU3YJRYEOAIIPFON16OAS75WEOAXQXRSCGTSRFFMR6PKC4"

st.set_page_config(page_title="Beyond Dashboard", layout='wide', initial_sidebar_state='collapsed')

hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
           
            </style>
            """

# footer {
# 	visibility: hidden;
#
# }
# footer:after {
# 	content:'goodbye';
# visibility: visible;
# display: block;
# position: relative;
# #background-color: red;
# padding: 5px;
# top: 2px;
# }
st.markdown(hide_streamlit_style, unsafe_allow_html=True)
st.markdown('# B Dashboard ')
st.text(' \n\n')  # break line
st.markdown('# Monthly Report sample ')
st.write(""" 
	Sample beyond dashboard using py
""")


def cb(success, failure):
	if success or success == {}:

		global data_report_url_from_server
		data_report_url_from_server = success['DownloadUrl']
		print(data_report_url_from_server)
	# handle success
	else:
		print(failure)


@st.cache
def load_data(selected_month):
	report_data = {
		"Day": "01",
		"Month": str(months.index(selected_month)),
		"ReportName": "Monthly Overview Report",
		"Year": "2021"
	}

	playfab.PlayFabAdminAPI.GetDataReport(request=report_data, callback=cb)
	response_csv = requests.get(data_report_url_from_server)
	open('report.csv', 'wb').write(response_csv.content)
	df = pd.read_csv("report.csv")
	return df


def main():
	left_column_1, right_column_1 = st.beta_columns(2)
	with left_column_1:
		st.text(" \n\n")
		selected_month = st.selectbox("Select month", options=months)
		st.text(" \n\n")  # break line

	if months.index(selected_month) != 0:
		st.write(f'selected month is = {selected_month} ')
		response_data = load_data(selected_month)
		selected_df = response_data.iloc[:, [2, 3, 7, 8]]
		st.text(" \n\n")  # break line
		st.dataframe(selected_df)
		st.line_chart(response_data['Total Logins'])
		st.text(" \n\n")  # break line
		st.line_chart(response_data['Unique Logins'])
		st.text(" \n\n")  # break line
		chart_data = response_data['Total Logins']
		st.bar_chart(chart_data)
		
		st.text(" \n\n")  # break line
		st.table(selected_df)

	with right_column_1:
		st.file_uploader('File uploader')


if __name__ == "__main__":
	main()
