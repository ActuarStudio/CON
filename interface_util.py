import streamlit as st
import pandas as pd
import os
import base64
from pathlib import Path
from io import BytesIO

#from st_aggrid import AgGrid

#################################

def load_image(path):
    return base64.b64encode(Path(str(os.getcwd()) + "/" + path).read_bytes()).decode()

def set_conf():

    page_title ="ActuarOnline"
    page_icon  =load_image("LOGO.png")

    st.set_page_config(
        page_title=page_title,
        page_icon=page_icon,
        layout="wide",   #'centered'
        initial_sidebar_state='collapsed')

def localCSS(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def set_HeroSection():

    header1 = 'Actuar'
    header2 = 'Online'
    title1  = 'Actuar'
    title2  = 'Studio'
    subtitle= "Актуарний Online сервіс від Actuar.studio"
    logo = load_image("LOGO.png")

    st.write(
        f"""
        <div class="base-wrapper hero-bg">
            <div class="hero-wrapper">
                <div class="hero-container">
                    <a class="logo-link"><span class="logo-bold">{header1}</span><span class="logo-lighter">{header2}</span></a>
                    <div class="hero-container-content">
                        <span class="hero-container-product primary-span">{title1}<br/>{title2}</span>
                        <span class="hero-container-subtitle primary-span">{subtitle}</span>
                    </div>
                </div>
                <div class="hero-container-image">   
                    <img style="width: 100%;" src="data:image/png;base64,{logo}"/>
                </div>
            </div><br>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.write(f"""<div>
            <div class="base-wrapper flex flex-column" style="background-color:#0090A7">
            <div class="white-span header p1" style="font-size:30px;">Перевір корректність НБУ XML</div>
            <div class="white-span header p1" style="font-size:30px;">Ознайомся з вмістом</div>
            <div class="white-span header p1" style="font-size:30px;">Конвертуй у XLSX формат</div>
            </div>""",
         unsafe_allow_html=True,
    )

    st.write("""
            <div class="base-wrapper primary-span">
                <span class="section-header">Конвертор НБУ XML файлів</span>
            </div>""",
        unsafe_allow_html=True,
    )

def set_footer():

    st.write(f"""
            <div class="base-wrapper flex flex-column" style="background-color:#0090A7">
                <div class="white-span header p1" style="font-size:30px;">Actuar.Studio 2021</div>
            </div>""",
        unsafe_allow_html=True,
    )


#################################

def to_excel(df):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, index=False, sheet_name='Sheet1')
    writer.save()
    processed_data = output.getvalue()
    return processed_data

def get_table_download_link(df):
    """Generates a link allowing the data in a given panda dataframe to be downloaded
    in:  dataframe
    out: href string
    """
    val = to_excel(df)
    b64 = base64.b64encode(val)  # val looks like b'...'
    return f'''
    <a href="data:application/octet-stream;base64,{b64.decode()}" download="extract.xlsx">
     <div class="row-widget stButton">
     <button kind="primary" class="css-2trqyj edgvbvh1" type="button">Download</button> 
     </div>
    </a>'''

def frame_download(df):
    st.markdown(get_table_download_link(df), unsafe_allow_html=True)



#################################

