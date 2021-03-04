import streamlit as st
from st_aggrid import AgGrid
import pandas as pd

w = st.file_uploader("Upload a excel file", type="xlsx")
if w:
    data = pd.read_excel(w)
    st.write(data)

st.title("IBNR")

d = pd.to_datetime("now")
d = pd.Period(d, freq='Q') - 1
d = d.end_time.floor(freq='D')
st.sidebar.date_input('Введіть звітну дату (останню дату звітного періоду)', value=d, min_value=None, max_value=None)
st.sidebar.file_uploader('Введіть Журнал виплат',['xls','xlsx'])
st.sidebar.file_uploader('Введіть Журнал зароблених премій',['xls','xlsx'])
st.sidebar.file_uploader('Введіть Журнал збитковості',['xls','xlsx'])

ddd = st.text('Loading data...')
ddd.text('Loading data...2')
data_load_state = st.text('Loading data....3')

f=st.file_uploader('File uploader')

href = f'<a href="data:file/csv;base64,{f}">Download csv file</a>'
st.markdown(href, unsafe_allow_html=True)
data_load_state.text('Loading data...done!')


st.title("Lists!")

lists = [
    [],
    [10, 20, 30],
    [[10, 20, 30], [1, 2, 3]],
    [[10, 20, 30], [1]],
    [[10, "hi", 30], [1]],
    [[{"foo": "bar"}, "hi", 30], [1]],
    [[{"foo": "bar"}, "hi", 30], [1, [100, 200, 300, 400]]],
]


for i, l in enumerate(lists):
    st.header("List %d" % i)

    st.write("With st.write")
    st.write(l)

    st.write("With st.json")
    st.json(l)

    st.write("With st.dataframe")
    st.dataframe(l)

df = pd.read_csv('https://raw.githubusercontent.com/fivethirtyeight/data/master/airline-safety/airline-safety.csv')
AgGrid(df)