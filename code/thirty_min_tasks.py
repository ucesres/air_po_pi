# 30 minute tasks
import numpy, pandas, datetime, plotly
import plotly.graph_objs as go

h_T = pandas.read_csv('/home/pi/projects/Air_po_pi/data/temp_humid.csv')
lux = pandas.read_csv('/home/pi/projects/Air_po_pi/data/lux.csv')
co2 = pandas.read_csv('/home/pi/projects/Air_po_pi/data/co2.csv')
now = datetime.datetime.now()
now_minus_24h = now - datetime.timedelta(hours=24)
now_minus_7d = now - datetime.timedelta(days=7)

def extract_time_slices(df_name, start_year, start_month, start_day,end_year, end_month, end_day):
    extract = df_name[(df_name['dts'] >datetime.datetime(start_year, start_month, start_day, 0, 0, 0))&
                (df_name['dts']<datetime.datetime(end_year, end_month, end_day, 23, 59, 0))]
    return extract
def th_plot(temp, humid, save_name):
    """
    plot a temp, humid timeseries
    temp (str):
    humid(str)
    save_name(str)
    """
    trace = go.Scatter(x=humid['timestamp'].values,y=humid['humidity'].values, name = 'Humidity %')
    trace1 = go.Scatter(x=temp['timestamp'].values,y=temp['temperature'].values, name = 'Temperature C', yaxis='y2')
    layout = go.Layout(yaxis = dict(title='Humidity %'), yaxis2 = dict(title='oC', overlaying='y',side ='right'))
    data=[trace, trace1]
    fig = go.Figure(data=data, layout=layout)
    plotly.offline.plot(fig, filename = '/home/pi/projects/web_pi/'+save_name+'.html', auto_open =False)

def lux_plt(lux,plot_name):
    trace = go.Scatter(x=lux['timestamp'].values,y=lux['lux'].values, name = 'lux')
    layout = go.Layout(yaxis = dict(title='lux'))
    data=[trace]
    fig = go.Figure(data=data, layout=layout)
    plotly.offline.plot(fig, filename = '/home/pi/projects/web_pi/'+plot_name+'.html', auto_open =False)
    
def co2_plt(co2, plot_name):
    trace = go.Scatter(x=co2['timestamp'].values,y=co2['co2_ppm'].values, name = 'co2 ppm')
    layout = go.Layout( yaxis = dict(title='co2'))
    data=[trace]
    fig = go.Figure(data=data, layout=layout)
    plotly.offline.plot(fig, filename = '/home/pi/projects/web_pi/'+plot_name+'.html', auto_open =False)
 
"""CO2 plotting"""
co2  = co2[co2.co2_ppm<5000]
co2 = co2[((co2.co2_ppm- co2.co2_ppm.mean()) / co2.co2_ppm.std()).abs() < 3]
co2  = co2[co2.index!=0]

co2 = co2.dropna(axis=0)
cdts = []
for i in co2['timestamp'].values:
    cdts.append(datetime.datetime.strptime(i,'%Y-%m-%d %H:%M:%S.%f'))
co2['dts'] = cdts
    
co2_24 = extract_time_slices(co2,now_minus_24h.year,now_minus_24h.month, now_minus_24h.day, now.year,now.month, now.day )
co2_7d = extract_time_slices(co2,now_minus_7d.year,now_minus_7d.month, now_minus_7d.day, now.year,now.month, now.day )
co2_this_month = extract_time_slices(co2,now.year,now.month, 1, now.year,now.month, now.day )

co2_plt(co2_24,'co2_24')
co2_plt(co2_7d,'co2_7d')
co2_plt(co2_this_month,'co2_this_month')
    
trace1 = go.Histogram(x=co2['co2_ppm'].values,opacity=0.75, name = 'co2 pm')
data = [trace1]
layout = go.Layout( barmode='overlay', title = 'Lifetime co2 distribution', yaxis = dict(title='Readings'), xaxis = dict(title='co2 ppm'))
fig = go.Figure(data=data, layout=layout)
plotly.offline.plot(fig, filename = '/home/pi/projects/web_pi/histogram_co2.html', auto_open =False)  

"""Lux plotting"""
lux  = lux[lux.lux<1000]
lux = lux[((lux.lux- lux.lux.mean()) / lux.lux.std()).abs() < 3]
# remove first row - with false values
lux = lux[lux.index!=0]
lux = lux.dropna(axis=0)
ldts = []
for i in lux['timestamp'].values:
    ldts.append(datetime.datetime.strptime(i,'%Y-%m-%d %H:%M:%S.%f'))
lux['dts'] = ldts

lux_24 = extract_time_slices(lux,now_minus_24h.year,now_minus_24h.month, now_minus_24h.day, now.year,now.month, now.day )

lux_7d = extract_time_slices(lux,now_minus_7d.year,now_minus_7d.month, now_minus_7d.day, now.year,now.month, now.day )

lux_this_month = extract_time_slices(lux,now.year,now.month, 1, now.year,now.month, now.day )

lux_plt(lux_24,'lux_24')
lux_plt(lux_7d,'lux_7d')
lux_plt(lux_this_month,'lux_current_month')

trace1 = go.Histogram(x=lux['lux'].values,opacity=0.75, name = 'lux')
data = [trace1]
layout = go.Layout( barmode='overlay', title = 'Lifetime lux distribution', yaxis = dict(title='Readings'), xaxis = dict(title='lux'))
fig = go.Figure(data=data, layout=layout)
plotly.offline.plot(fig, filename = '/home/pi/projects/web_pi/histogram_lux.html', auto_open =False)

"""H_t_plotting"""
h_T  = h_T[h_T.humidity<100]
h_T  = h_T[h_T.temperature<50]
# remove false readings
humid = h_T[((h_T.humidity- h_T.humidity.mean()) / h_T.humidity.std()).abs() < 3]
temp = h_T[((h_T.temperature- h_T.temperature.mean()) / h_T.temperature.std()).abs() < 3]
# remove first row - with false values - could use  range to remove proto values
humid = humid[humid.index!=0]
temp = temp[temp.index!=0]
# remove nan
humid = humid.dropna(axis=0)
temp = temp.dropna(axis=0)
dts = []
for i in humid['timestamp'].values:
    dts.append(datetime.datetime.strptime(i,'%Y-%m-%d %H:%M:%S.%f'))
dts1 = []
for i in temp['timestamp'].values:
    dts1.append(datetime.datetime.strptime(i,'%Y-%m-%d %H:%M:%S.%f'))
humid['dts'] = dts
temp['dts'] = dts1    

humid_24 = extract_time_slices(humid,now_minus_24h.year,now_minus_24h.month, now_minus_24h.day, now.year,now.month, now.day )
temp_24 = extract_time_slices(temp,now_minus_24h.year,now_minus_24h.month, now_minus_24h.day, now.year,now.month, now.day )
humid_7d = extract_time_slices(humid,now_minus_7d.year,now_minus_7d.month, now_minus_7d.day, now.year,now.month, now.day )
temp_7d = extract_time_slices(temp,now_minus_7d.year,now_minus_7d.month, now_minus_7d.day, now.year,now.month, now.day )
humid_this_month = extract_time_slices(humid,now.year,now.month, 1, now.year,now.month, now.day )
temp_this_month = extract_time_slices(temp,now.year,now.month, 1, now.year,now.month, now.day )

th_plot(temp_24,humid_24,'th_24')
th_plot(temp_7d, humid_7d,'th_7d')
th_plot(temp_this_month,humid_this_month, 't_h_current_month')

trace1 = go.Histogram(x=humid['humidity'].values,opacity=0.75, name = 'Humidity %')
data = [trace1]
layout = go.Layout( barmode='overlay', title = 'Lifetime humidity distribution', yaxis = dict(title='Readings'), xaxis = dict(title='%'))
fig = go.Figure(data=data, layout=layout)
plotly.offline.plot(fig, filename = '/home/pi/projects/web_pi/histogram_humidity.html', auto_open =False)

trace1 = go.Histogram(x=temp['temperature'].values,opacity=0.75, name = 'Temperature')
data = [trace1]
layout = go.Layout( barmode='overlay', title = 'Lifetime temperature distribution', yaxis = dict(title='Readings'), xaxis = dict(title='Degrees Centigrade'))
fig = go.Figure(data=data, layout=layout)
plotly.offline.plot(fig, filename = '/home/pi/projects/web_pi/histogram_temperature.html', auto_open =False)

