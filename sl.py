import streamlit as st
from st_aggrid import AgGrid
import pandas as pd
import interface_util as iu


iu.set_conf()
iu.localCSS("static/bulma.css")
iu.localCSS("static/st.css")
iu.set_HeroSection()
iu.hide_main_menu()

#st.components.v1.iframe('file:///Users/volodymyr/ACTUAR/CON/kit2.html',width=1000, height=1100)
#iu.new_index()

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

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
#c1, col1, c3, col2, c5 = mc.beta_columns([1,12,1,12,1])
#col2 = col1
c1, col1, c3 = mc.beta_columns([1,25,1])

col1.header("Обери XML файл звітності НБУ:")
col1.subheader("Обери XML файл звітності НБУ:")

f = col1.file_uploader( '',type="xml")
if f:
    file_details = {"FileName":f.name,"FileType":f.type}
    col1.text(file_details["FileName"])
    col1.text(file_details["FileType"])

f ='https://raw.githubusercontent.com/fivethirtyeight/data/master/airline-safety/airline-safety.csv'

df = pd.read_csv(f)
col1.write(df)
#with col1:  AgGrid(df)

with col1:
    st.subheader("Завантажте на ваш комп'ютер конвертований файл .XLSX")
    iu.frame_download(df)
    st.button('Download')


#################################

iu.set_footer()


