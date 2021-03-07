import streamlit as st
from st_aggrid import AgGrid
import pandas as pd
import util

st.set_page_config(
    page_title="ActuarOnline",
    page_icon="",                         # 🧊   st.image
    layout='centered',                    #"wide",
    initial_sidebar_state='collapsed'     #"expanded",
)

#################################

#util.localCSS("style2.css")
util.localCSS("style.css")

util.genHeroSection(
    title1="Actuar",
    title2="Studio",
    subtitle="Актуарний Online сервіс від Actuar.studio",
    logo= util.load_image("LOGO.png"),
    header=True
)

st.write(f"""<div>
        <div class="base-wrapper flex flex-column" style="background-color:#0090A7">
            <div class="white-span header p1" style="font-size:30px;">Перевір корректність НБУ XML</div>
            <div class="white-span header p1" style="font-size:30px;">Ознайомся з вмістом</div>
            <div class="white-span header p1" style="font-size:30px;">Конвертуй у XLSX формат</div>
    </div>""",
         unsafe_allow_html=True,
         )

st.write(
    """
<div class="base-wrapper primary-span">
    <span class="section-header">Конвертор НБУ XML файлів</span>
</div>""",
    unsafe_allow_html=True,
)

#################################

d = pd.to_datetime("now")
d = pd.Period(d, freq='Q') - 1
d = d.end_time.floor(freq='D')
st.sidebar.date_input('Введіть звітну дату (останню дату звітного періоду)', value=d, min_value=None, max_value=None)
st.sidebar.file_uploader('Введіть Журнал виплат',['xls','xlsx'])
st.sidebar.file_uploader('Введіть Журнал зароблених премій',['xls','xlsx'])
st.sidebar.file_uploader('Введіть Журнал збитковості',['xls','xlsx'])

##############################

main_container = st.beta_container()
mc = main_container

col1, col2, col3, col4, col5 = mc.beta_columns([1,12,1,12,1])

f = col2.file_uploader("Оберіть XML файл звітності НБУ", type="xml")
if f:
    data = pd.read_excel(w)
    mc.write(data)

data_load_state = mc.text('Loading data....3')

f ='https://raw.githubusercontent.com/fivethirtyeight/data/master/airline-safety/airline-safety.csv'
href = f'<a href="data:file/csv;base64,{f}">Download csv file</a>'
mc.markdown(href, unsafe_allow_html=True)

data_load_state.text('Loading data...done!')

df = pd.read_csv(f)

mc.write(df)

with mc:
    AgGrid(df)



#################################

# footer

st.write(f"""
        <div class="base-wrapper flex flex-column" style="background-color:#0090A7">
            <div class="white-span header p1" style="font-size:30px;">Actuar.Studio 2021</div>
        </div>""",
         unsafe_allow_html=True, )
