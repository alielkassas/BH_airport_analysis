import requests 
from bs4 import BeautifulSoup
import pandas as pd
import datetime 
import time 

def collect_flight_data(day, flight_direction):
    '''
    This fun scrape data from BH airport and return it as a table
    
    Args:
        day (str): it will be today (TD) or Tomorrow (TM).
        flight_direction (str): It will be arrival or departures

    Returns:
        Pandas DataFrame that have 8 columns
    '''
    
    url = f"https://www.bahrainairport.bh/flight-{flight_direction}?date={day}"
    response = requests.get(url)

    soup = BeautifulSoup(response.text)


    time_lst = []
    destination_lst = []
    gate_lst = []
    status_lst = []
    flight_lst = []
    airways_lst = []

    flights = soup.find_all("div", {"class": f"flight-table-list row dv{flight_direction[:-1].title()}List"}) #ArrivalList

    for flight in flights:
        try:
            airways_lst.append(flight.find('img')['alt'])
        except:
            airways_lst.append(pd.NA)


        status_lst.append(flight.find('div', class_="col col-flight-status").text.strip())
        flight_lst.append(flight.find('div', class_="col col-flight-no").text.strip())
        gate_lst.append(flight.find('div', class_="col col-gate").text.strip())
        time_lst.append(flight.find('div', class_="col col-flight-time").text.strip())
        destination_lst.append(flight.find('div', class_="col col-flight-origin").text.strip())
        
    flights_data = {'destination':destination_lst, 
            'flight_number':flight_lst,
            'airline':airways_lst, 
            'gate':gate_lst, 
            'status':status_lst,
            'time':time_lst}
    df = pd.DataFrame(flights_data)
    today_date = datetime.date.today()
    if day == 'TD':
        date = today_date
    elif day == 'TM':
        date = today_date + datetime.timedelta(days=1)

    df['date'] = date
    df['direction'] = flight_direction


    return df
        
def collect_arrival_dep():
    tables = []
    directions = ['arrivals', 'departures']
    days = ['TD', 'TM']
    
    for direction in directions:
        for day in days:
            tables.append(collect_flight_data(day, direction))
            time.sleep(10) 
    df = pd.concat(tables) 
    return df

def save_data(df):
    today = datetime.date.today()
    path = f'all_flights_data_{today}.csv'.replace('-', '_')
    df.to_csv(path)


df = collect_arrival_dep()
save_data(df)
