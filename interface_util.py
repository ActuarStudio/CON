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
    page_icon  =load_image("static/LOGO.png")

    st.set_page_config(
        page_title=page_title,
        page_icon=page_icon,
        layout="wide",   #'centered'
        initial_sidebar_state='collapsed')

def localCSS(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def set_HeroSection():

    image = load_image("static/lat.png")

    st.write(
    f"""    
    <div class="hero has-bg-img" width='100vw'>
        <div class="hero-head">
        <nav class="navbar  is-fixed-top">
            <div class="container">
                <!-- Brand -->
                <div class="navbar-brand">
                    <div class="navbar-item" href="/">                        
                        <div class="has-text-danger is-size-3 has-text-weight-medium">
                         Actuar
                        </div>
                    </div>
                    <a role="button" class="navbar-burger" aria-label="menu" aria-expanded="false" data-target="navbarMenu">
                        <span aria-hidden="true"></span>
                        <span aria-hidden="true"></span>
                        <span aria-hidden="true"></span>
                    </a>
                </div>
                <!-- Navbar menu -->
                <div class="navbar-menu ">
                    <!-- Navbar Start -->
                    <div class="navbar-start">
                    </div>
                    <div class="navbar-end has-text-grey is-size-4 has-text-weight-light">
                        <!-- Navbar item -->
                        <div class="navbar-item" is-size-4 has-text-grey-dark href=".html">
                            Інформація
                        </div>
                        <!-- Navbar item -->
                        <div class="navbar-item" is-size-4 has-text-grey-dark href=".html">
                            Проект
                        </div>
                        <!-- Navbar item -->
                        <div class="navbar-item" is-size-4 has-text-grey-dark href=".html">
                            Реєстрація
                        </div>
                    </div>
                </div>
            </div>
        </nav>
        </div>
        <!-- Hero image -->
        <div id="main-hero" class="hero-body" width='100vw'>
            <div class="container">
                <div class="columns is-vcentered mt-3">
                    <div class="column is-6 signup-column has-text-left">
                        <h1 class="title has-text-weight-normal is-size-1 has-text-danger">
                           ActuarOnline
                        </h1>
                        <h2 class="subtitle has-text-weight-light is-size-3 has-text-grey-dark">
                            <br>
                            Актуарний Online сервіс від ActuarStudio
                        </h2>
                        <br>
                    </div>
                    <div class="column is-4 is-offset-2">
                        <!-- Hero mockup -->
                        <figure class="image is-hidden-mobile">
                            <img src="data:image/png;base64,{image}" alt="">
                        </figure>
                    </div>
                </div>
            </div>
        </div>
        <div class="is-divider is-danger" ></div>
        <div class="hero-body has-shadow has-border">
            <div class="container">
                <div class="columns is-vcentered ">
                    <div class="column is-6 signup-column has-text-left">
                        <div class="has-text-weight-light is-size-1 has-text-grey-dark">
                            <h2 class="has-text-weight-light is-size-4 has-text-grey-dark">Перевір корректність НБУ XML</h2>
                            <h2 class="has-text-weight-light is-size-4 has-text-grey-dark">Ознайомся з вмістом</h2>
                            <h2 class="has-text-weight-light is-size-4 has-text-grey-dark">Конвертуй у XLSX формат</h2>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div class="is-divider is-danger " ></div>
    </div>
    """,
        unsafe_allow_html=True,
    )

#    st.write("""
#            <div class="base-wrapper primary-span">
#                <span class="section-header">Конвертор НБУ XML файлів</span>
#           </div>""",
#        unsafe_allow_html=True,
#    )

def set_footer():

    st.write(
        f"""
    <!-- Footer -->    
    <div class="is-divider is-danger" ></div>
    <div class="myfooter">
        <div class="container">
        <div class="is-size-4 has-text-grey-dark has-text-weight-light">
            <p class="is-size-4 has-text-grey-dark has-text-weight-light">
                ActuarOnline 2021
            </p>
        </div>
        </div>
    </div>
    <!-- /Footer -->           
        """,
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
     <button kind="primary" class="css-2trqyj edgvbvh1" type="button" >Download</button> 
     </div>
    </a>'''

def frame_download(df):
    st.markdown(get_table_download_link(df), unsafe_allow_html=True)

def hide_main_menu ():
    hide_streamlit_style = '''
    <style>
    #MainMenu {visibility: hidden;}
    </style>
    '''
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)


#################################

def new_index():

        import pathlib
        from bs4 import BeautifulSoup

        index_path = pathlib.Path(st.__file__).parent / "static" / "index.html"
        soup = BeautifulSoup(index_path.read_text(), features="lxml")

        f = open('text.txt', 'w')
        #f.write(soup.get_text())
        f.write(str(index_path))

        '''
        if not soup.find(id="google-analytics-loader"):
            script_tag_import = soup.new_tag(
                "script",
                src="https://www.googletagmanager.com/gtag/js?id=%s"
                % GOOGLE_ANALYTICS_CODE,
            )
            soup.head.append(script_tag_import)
            script_tag_loader = soup.new_tag("script", id="google-analytics-loader")
            script_tag_loader.string = GA_JS
            soup.head.append(script_tag_loader)
            script_tag_managerhead = soup.new_tag("script", id="google-tagmanagerhead")
            script_tag_managerhead.string = TAG_MANAGER
            soup.head.append(script_tag_managerhead)
            script_tag_manager_body = soup.new_tag(
                "script",
                src="https://www.googletagmanager.com/gtm.js?id=GTM-MKWTV7X"
            )
            soup.head.append(script_tag_manager_body)
            index_path.write_text(str(soup))
        '''