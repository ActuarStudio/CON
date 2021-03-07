import streamlit as st
from st_aggrid import AgGrid
import pandas as pd
import interface_util as iu

iu.set_conf()
iu.localCSS("style.css")
iu.set_HeroSection()

#################################

d = pd.to_datetime("now")
d = pd.Period(d, freq='Q') - 1
d = d.end_time.floor(freq='D')
st.sidebar.date_input('Введіть звітну дату (останню дату звітного періоду)', value=d, min_value=None, max_value=None)
st.sidebar.file_uploader('Введіть Журнал виплат',['xls','xlsx'])
st.sidebar.file_uploader('Введіть Журнал зароблених премій',['xls','xlsx'])
st.sidebar.file_uploader('Введіть Журнал збитковості',['xls','xlsx'])

##############################

mc = st.beta_container()

col1, col2, col3, col4, col5 = mc.beta_columns([1,12,1,12,1])

f = col2.file_uploader("Оберіть XML файл звітності НБУ", type="xml")
if f:
    data = pd.read_excel(w)
    mc.write(data)

cl1, cl2, cl3 = mc.beta_columns([1,25,1])

f ='https://raw.githubusercontent.com/fivethirtyeight/data/master/airline-safety/airline-safety.csv'

df = pd.read_csv(f)
cl2.write(df)
#with cl2:  AgGrid(df)

with col4:
    st.text("\nЗавантажте на ваш комп'ютер конвертований файл .XLSX\n")
    iu.frame_download(df)


#################################

iu.set_footer()


