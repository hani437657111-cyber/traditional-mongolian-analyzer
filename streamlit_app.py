import streamlit as st

st.title("Traditional Mongolian Text Analyzer")

st.write("Traditional Mongolian Text Analyzer")

text = st.text_area(
    "Place enter or paste Traditional Mongolian text here：",
    height=200
)

if st.button("Start Detection"):
    if text:
        st.write("Character Count：", len(text))
    else:
        st.warning("Place enter or paste Traditional Mongolian text here")
