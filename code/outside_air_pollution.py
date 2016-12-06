# hourly outside air pollution data call and plotting

import numpy, urllib2, json, pandas, datetime, plotly

import plotly.graph_objs as go
prep = 'http://api.erg.kcl.ac.uk/AirQuality'


# index
f = urllib2.urlopen(prep +'/Hourly/MonitoringIndex/SiteCode=BL0/Json')
json_string = f.read()
parsed_json_hour_index = json.loads(json_string)
species = parsed_json_hour_index['HourlyAirQualityIndex']['LocalAuthority']['Site']['species']
cols = ['name', 'index', 'band']
pd_index = pandas.DataFrame(columns = cols)
for spec in species:
	pd_data = [spec['@SpeciesName'],spec['@AirQualityIndex'], spec['@AirQualityBand']]
	pd_index.loc[len(pd_index)] = pd_data
pd_index.to_csv('/home/pi/projects/web_pi/outside_air_pollution.csv')

# data
now = datetime.datetime.now()
now_plus_1 = now + datetime.timedelta(days=1)
now_minus_3d = now - datetime.timedelta(days=3)
now_txt = now_plus_1.strftime('%d%b%Y')
n3d_txt = now_minus_3d.strftime('%d%b%Y') 
f = urllib2.urlopen(prep +'/Data/Wide/Site/SiteCode=BL0/StartDate='+n3d_txt+'/EndDate='+now_txt+'/Json')
json_string = f.read()
parsed_json_wide_data= json.loads(json_string)
col_names = parsed_json_wide_data['AirQualityData']['Columns']['Column']
pd_col = ['timestamp']
for cl_nm in col_names:
    col_title = cl_nm['@ColumnName']
    pd_col.append(col_title[21:len(col_title)])
conc_data = pandas.DataFrame(columns = pd_col)
all_data = parsed_json_wide_data['AirQualityData']['RawAQData']['Data']
for i in range(0, len(all_data)):
    p_dat = all_data[i]
    DA = [p_dat['@MeasurementDateGMT'],p_dat['@Data1'],p_dat['@Data2'],p_dat['@Data3'],p_dat['@Data4'],p_dat['@Data5'],p_dat['@Data6'],p_dat['@Data7'],p_dat['@Data8']]
    conc_data.loc[len(conc_data)] = DA
conc_data.to_csv('/home/pi/projects/web_pi/outside_air_pollution_timeseries.csv')

def conc_plt(conc_data,plot_name):
    #trace = go.Scatter(x=conc_data['timestamp'].values,y=conc_data['Nitric Oxide (ug/m3)'].values, name = 'Nitric Oxide')
    trace1 = go.Scatter(x=conc_data['timestamp'].values,y=conc_data['Nitrogen Dioxide (ug/m3)'].values, name = 'Nitrogen Dioxide')
    trace2 = go.Scatter(x=conc_data['timestamp'].values,y=conc_data['Ozone (ug/m3)'].values, name = 'Ozone')
    trace3 = go.Scatter(x=conc_data['timestamp'].values,y=conc_data['PM10 Particulate (ug/m3)'].values, name = 'PM10 Particulate')
    trace4 = go.Scatter(x=conc_data['timestamp'].values,y=conc_data['PM2.5 Particulate (ug/m3)'].values, name = 'PM2.5 Particulate')
    trace5 = go.Scatter(x=conc_data['timestamp'].values,y=conc_data['Sulphur Dioxide (ug/m3)'].values, name = 'Sulphur Dioxide ')
    layout = go.Layout(yaxis = dict(title='Concentration (microgram/m3)'))
    data=[trace1,trace2,trace3,trace4,trace5]
    fig = go.Figure(data=data, layout=layout)
    plotly.offline.plot(fig, filename = '/home/pi/projects/web_pi/'+plot_name+'.html', auto_open =False)
    
conc_plt(conc_data,'outside_pol_conc')
