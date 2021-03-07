import streamlit as st

import time

import os
import base64
from pathlib import Path

def load_image(path):
    return base64.b64encode(Path(str(os.getcwd()) + "/" + path).read_bytes()).decode()

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
