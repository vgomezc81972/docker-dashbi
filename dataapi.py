import pandas as pd


fields="""
['date', 'ID', 'resultID', 'ap_id', 'ip_ap', 'expected_download_mbps',
       'expected_upload_mbps', 'speedtest_server_url', 'payload_download_size',
       'payload_upload_size', 'result_download_mbps', 'result_upload_mbps',
       'result_start_date', 'result_end_date', 'duration', 'result_execution',
       'test_type', 'workflow_process_id', 'ap_type', 'is_satellite', 'cumple',
       'result_message', 'flow_id', 'hour']

"""




def load_df(filename='data.csv'):
	df = pd.read_csv(filename,sep=";",low_memory=False)
	# Convert the 'date_column' to a datetime data type
	df['date'] = df['date'].str.strip()
	df['date'] = pd.to_datetime(df['date'])
	# Calculate the hour from the date column
	df['hour'] = df['date'].dt.hour
	df['expected_download_mbps']= df['expected_download_mbps'].astype(int)
	print(df.info())
	print(df.columns)
	return df 
