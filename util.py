import streamlit as st

import time

import os
import base64
from pathlib import Path

def load_image(path):
    return base64.b64encode(Path(str(os.getcwd()) + "/" + path).read_bytes()).decode()

'''
def stylizeButton(name, style_string, session_state, others=dict()):
    """ adds a css option to a button you made """
    session_state.button_styles[name] = [style_string, others]

def applyButtonStyles(session_state):
    """ Use it at the end of the program to apply styles to buttons as defined by the function above """
    time.sleep(0.1)
    html = ""
    for name, style in session_state.button_styles.items():
        parts = (
            style[0]
            .replace("\n", "")
            .replace("    ", "")
            .replace("; ", "&")
            .replace(";", "&")
            .replace(":", "=")
        )
        other_args = "&".join(
            [str(key) + "=" + str(value) for key, value in style[1].items()]
        )
        html += f"""
        <iframe src="resources/redo-button.html?name={name}&{parts}&{other_args}" style="height:0px;width:0px;">
        </iframe>"""
    st.write(html, unsafe_allow_html=True)



def gen_pdf_report():
    st.write(
        """
    <iframe src="resources/ctrlp.html" height="100" width="350" style="border:none; float: right;"></iframe>
    """,
        unsafe_allow_html=True,
    )

'''

def localCSS(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def genHeroSection(title1: str, title2: str, subtitle: str, logo: str, header: bool, explain: bool = False):

    if header:
        header = """<a class="logo-link"><span class="logo-bold">Actuar</span><span class="logo-lighter">Online</span></a>"""
    else:
        header = """<br>"""

    st.write(
        f"""
        <div class="base-wrapper hero-bg">
            <div class="hero-wrapper">
                <div class="hero-container">
                    {header}
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
