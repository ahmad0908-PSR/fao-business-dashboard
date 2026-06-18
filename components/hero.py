import streamlit as st
import json
from streamlit_lottie import st_lottie


def load_lottie_file(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)


def render_hero():

    # ✅ Load animation
    lottie_animation = load_lottie_file("assets/animation.json")

    # ✅ CENTER the animation
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        st_lottie(lottie_animation, height=200)
