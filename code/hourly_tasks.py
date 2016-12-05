# hourly tasks for room 106 monitoring project
import pandas, datetime, datetime

def extract_hourly_conditions(df_weather):
    """Extract current external conditions."""
    now  = datetime.datetime(datetime.datetime.now().year,datetime.datetime.now().month,datetime.datetime.now().day, datetime.datetime.now().hour,0)
    df_now = df_weather.loc[df_weather['ts'] == now.strftime('%Y-%m-%d %H:%M:%S')]
    print now
    print df_now
    return df_now
    
df_weather = pandas.read_csv('/home/pi/projects/Air_po_pi/data/external_weather_data.csv')  
df_now = extract_hourly_conditions(df_weather)    
df_now.to_csv('/home/pi/projects/web_pi/current_external_conditions.csv')


