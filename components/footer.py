import streamlit as st

def render_footer():

    st.markdown("""
    <hr style="margin-top:40px;">

    <div style="text-align:center; font-size:12px; color:gray;">
        © 2026 Powered by ACE | FAO EFSP Project
    </div>
    """, unsafe_allow_html=True)
