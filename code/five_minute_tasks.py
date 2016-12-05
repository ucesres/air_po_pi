# run every 1 minute for current conditions
import pandas, datetime, numpy

def read_cur_con():
    """Extract the latest internal values"""
    cur_ht = pandas.read_csv('/home/pi/projects/Air_po_pi/data/temp_humid.csv')
    cur_co2 = pandas.read_csv('/home/pi/projects/Air_po_pi/data/co2.csv')
    cur_lux = pandas.read_csv('/home/pi/projects/Air_po_pi/data/lux.csv')
    ch = numpy.around(cur_ht['humidity'].values[-1],decimals = 1)
    ct = numpy.around(cur_ht['temperature'].values[-1],decimals = 1)
    cl = numpy.around(cur_lux['lux'].values[-1],decimals = 1)
    cc = numpy.around(cur_co2['co2_ppm'].values[-1],decimals = 1)
    current_internal_conditions = pandas.DataFrame(columns = ['ts','temp','humid','lux','co2'])
    current_internal_conditions.loc[0] = [datetime.datetime.now(),ct,ch,cl,cc]
    return current_internal_conditions
    
c_i_c = read_cur_con()
c_i_c.to_csv('/home/pi/projects/web_pi/current_internal_conditions.csv')
