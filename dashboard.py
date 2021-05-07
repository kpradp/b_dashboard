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

data_report_url_from_server: None = None
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




df = pd.DataFrame(
	np.random.randn(200, 3),
	columns=['a', 'b', 'c'])


def cb(success, failure):
	if success or success == {}:
		# print(success['DownloadUrl'])
		global data_report_url_from_server
		data_report_url_from_server = success['DownloadUrl']
		print(data_report_url_from_server)
	# handle success
	else:
		print(failure)


def main():
	global df

	c = alt.Chart(df).mark_circle().encode(
		x='a', y='b', size='c', color='c', tooltip=['a', 'b', 'c'])
	st.altair_chart(c, use_container_width=True)

	""" 
	Sample beyond dashboard using py
	"""

	left_column_1, right_column_1 = st.beta_columns(2)
	report_data = {}
	with left_column_1:
		# s_date = st.date_input('select a date')
		st.text(" \n\n")
		selected_month = st.selectbox("Select month", options=months)
		# st.write(months.index(selected_month))
		st.text(" \n\n")  # break line

		if months.index(selected_month) != 0:
			st.write(f'selected month is = {selected_month} ')
			st.write(f'contacting server ')
	report_data["Day"] = "01"
	report_data["Month"] = str(months.index(selected_month))
	report_data["ReportName"] = "Monthly Overview Report"
	report_data["Year"] = "2021"
	# st.write(report_data)

	with right_column_1:
		st.file_uploader('File uploader')
	try:

		report_response = playfab.PlayFabAdminAPI.GetDataReport(request=report_data, callback=cb)
		# print(data_report_url_from_server)
		response_csv = requests.get(data_report_url_from_server)

		# st.write(response_csv.content)
		open('report.csv', 'wb').write(response_csv.content)
		df = pd.read_csv("report.csv")
		selected_df = df.iloc[:, [2, 3, 7, 8]]
		st.text(" \n\n")  # break line

		st.dataframe(selected_df)

		st.line_chart(df['Total Logins'])
		st.text(" \n\n")  # break line
		st.line_chart(df['Unique Logins'])
		st.text(" \n\n")  # break line

		chart_data = df['Total Logins']
		st.bar_chart(chart_data)
		st.text(" \n\n")  # break line
		st.table(selected_df)

	except:
		pass


if __name__ == "__main__":
	main()
