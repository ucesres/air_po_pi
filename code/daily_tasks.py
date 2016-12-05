# daily tasks
import urllib2, json, time, pandas, datetime, plotly
import plotly.graph_objs as go

f = urllib2.urlopen('http://api.wunderground.com/api/7687a5aed195a60d/hourly10day/q/UK/London.json')
json_string = f.read()
parsed_json_hour = json.loads(json_string)
time_series={}
dts=[]
df_weather = pandas.DataFrame(columns = ['ts','wspd','humidity','tempe', 'icon'])
for time_period in range(0,len(parsed_json_hour['hourly_forecast'])):
    #a = parsed_json_hour['hourly_forecast'][time_period]['FCTTIME']['pretty']
    year = int(parsed_json_hour['hourly_forecast'][time_period]['FCTTIME']['year'])
    month = int(parsed_json_hour['hourly_forecast'][time_period]['FCTTIME']['mon'])
    day = int(parsed_json_hour['hourly_forecast'][time_period]['FCTTIME']['mday'])
    hour = int(parsed_json_hour['hourly_forecast'][time_period]['FCTTIME']['hour'])
    minute = int(parsed_json_hour['hourly_forecast'][time_period]['FCTTIME']['min'])
    
    timestamp = datetime.datetime(year,month, day, hour, minute)
    wspd = int(parsed_json_hour['hourly_forecast'][time_period]['wspd']['metric']) *0.27777777777778
    humi = int(parsed_json_hour['hourly_forecast'][time_period]['humidity']) 
    temp = int(parsed_json_hour['hourly_forecast'][time_period]['temp']['metric']) 
    icon = parsed_json_hour['hourly_forecast'][time_period]['icon_url']
    time_series [timestamp] = wspd,humi,temp, icon
    dts.append(timestamp)
    df_weather.loc[len(df_weather)] = [timestamp,wspd,humi,temp, icon]

df_weather.to_csv('/home/pi/projects/Air_po_pi/data/external_weather_data.csv')

dts = df_weather['ts']
def plot_timeseries_forecast(df_weather, dts):
	trace = go.Scatter(x=dts,y=df_weather['humidity'].values, name = 'Humidity %')
	trace1 = go.Scatter(x=dts,y=df_weather['tempe'].values, name = 'Temperature C', yaxis='y2')
	layout = go.Layout(yaxis = dict(title='Humidity %'), yaxis2 = dict(title='oC', overlaying='y',side ='right'))
	data=[trace, trace1]
	fig = go.Figure(data=data, layout=layout)
	plotly.offline.plot(fig, filename = '/home/pi/projects/web_pi//daily_forecast.html', auto_open =False)

plot_timeseries_forecast(df_weather, dts)
