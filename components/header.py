import streamlit as st
import base64
import streamlit.components.v1 as components


def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()


def render_header():

    left_logo = get_base64_image("assets/logo_left.png")
    right_logo = get_base64_image("assets/logo_right.png")

    html = f"""
    <div style="
        background-color:#0b1f3a;
        padding:15px 20px;
        border-radius:8px;
        display:flex;
        align-items:center;
        justify-content:space-between;
    ">
        <img src="data:image/png;base64,{left_logo}" style="height:65px; object-fit:contain;">

        <h2 style="
            color:white;
            margin:0;
            text-align:center;
            flex-grow:1;
            font-size:22px;
            font-family:sans-serif;
        ">
            Emergency Food Security Project (EFSP) Dashboard
        </h2>

        <img src="data:image/png;base64,{right_logo}" style="height:70px; object-fit:contain;">
    </div>
    """

    components.html(html, height=100)