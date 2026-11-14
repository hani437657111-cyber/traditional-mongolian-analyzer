import streamlit as st
import unicodedata

st.title("Traditional Mongolian Text Analyzer")
st.write("Traditional Mongolian Text Analyzer")

text = st.text_area(
    "Please enter or paste Traditional Mongolian script text here：",height=200)

SPECIAL_CHARS = {"\u180E": "MONGOLIAN VOWEL SEPARATOR","\u202F": "NARROW NO-BREAK SPACE",
"\u200D": "ZERO WIDTH JOINER","\u200C": "ZERO WIDTH NON-JOINER","\u180B": "MONGOLIAN FREE VARIATION SELECTOR ONE",
"\u180C": "MONGOLIAN FREE VARIATION SELECTOR TWO","\u180D": "MONGOLIAN FREE VARIATION SELECTOR THREE",}

if st.button("Start detection"):
    if text:
        st.subheader("Basic Statistics")
        st.write("Unicode of Code Points：", len(text))

        st.subheader("Special Unicode Character Detection")

        found = False

        for position, char in enumerate(text):
            if char in SPECIAL_CHARS:
                found = True
                st.write(f"Position：{position + 1} | "
                    f"Character：{repr(char)} | "
                    f"Code Point：U+{ord(char):04X} | "
                    f"Name：{SPECIAL_CHARS[char]}")

        if not found:
            st.success("No special characters listed in this tool were found.")
    else:
        st.warning("Please enter or paste Traditional Mongolian script text here：")
