import numpy as np
import requests
import os
import json
import pandas as pd
import streamlit as st
from datetime import date
import playfab

st.set_page_config(page_title="B Dashboard", layout='wide', initial_sidebar_state='collapsed')
st.markdown('# B Dashboard sample')
st.text(" \n\n")  # break line

"""
# My first app
Here's our first attempt at using data to create a table:
"""
date = st.date_input('Select a date')
print(date)
st.write(date)

chart_data = pd.DataFrame(
	np.random.randn(20, 3),
	columns=['a', 'b', 'c'])

st.line_chart(chart_data)

data_report_url_from_server = None
playfab.PlayFabSettings.TitleId = "1d015"
playfab.PlayFabSettings.DeveloperSecretKey = "Y5TDEU3YJRYEOAIIPFON16OAS75WEOAXQXRSCGTSRFFMR6PKC4"

report_data = {
	"Day": "03",
	"Month": "05",
	"ReportName": "Daily Totals Report",
	"Year": "2021"

}


def cb(success, failure):
	if success or success == {}:
		# print(success['DownloadUrl'])
		global data_report_url_from_server
		data_report_url_from_server = success['DownloadUrl']
		print(data_report_url_from_server)
	# handle success
	else:
		print(failure)


report_response = playfab.PlayFabAdminAPI.GetDataReport(request=report_data, callback=cb)

# print(data_report_url_from_server)
response_csv = requests.get(data_report_url_from_server)
print(response_csv.content)
open('report.csv', 'wb').write(response_csv.content)
