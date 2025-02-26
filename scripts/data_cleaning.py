def clean_time(df):
    df['estimated_time'] = df['time'].str[-5:]
    df['estimated_date_time'] = df['date']+' '+df['estimated_time'] 
    df.drop(columns=['time', 'date', 'estimated_time'], inplace=True)
    df['estimated_date_time']  = pd.to_datetime(df['estimated_date_time'] )
    df.to_parquet('all_flights_data_2025_02_26.parquet')
    
    return df