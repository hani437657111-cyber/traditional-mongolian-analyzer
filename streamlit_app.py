import streamlit as st
import unicodedata

st.set_page_config(
    page_title="Traditional Mongolian Text Analyzer",page_icon="ᠮ",layout="wide")

st.title("Traditional Mongolian Text Analyzer")

# =========================
# 1. Please enter the Mongolian text here
# =========================

text = st.text_area("Please enter or paste Traditional Mongolian text here：",height=250,placeholder="Please enter the Mongolian text here")
st.write("Font rendering test:")
st.markdown('<div style="font-family: Mongolian Baiti; font-size: 30px;">ᠮᠣᠩᠭᠣᠯ</div>', unsafe_allow_html=True)
# =========================
# 2. Affix/suffix rule
# =========================

st.subheader("Affix/Suffix Exclusion Rules")

st.write(
    "Please enter or paste the affixes or suffixes to exclude from character counting."
    "Enter one rule per line. The original text will not be modified.")

suffix_input = st.text_area("Suffixes and affixes to exclude:",height=120,placeholder="Enter one affix or suffix per line.\nExample:\n ᠤ\nᠤ\nᠠ᠋")

# =========================
# 3. special Unicode characters
# =========================

SPECIAL_CHARS = {"\u180E": "MONGOLIAN VOWEL SEPARATOR","\u202F": "NARROW NO-BREAK SPACE","\u200D": "ZERO WIDTH JOINER","\u200C": "ZERO WIDTH NON-JOINER",
"\u180B": "MONGOLIAN FREE VARIATION SELECTOR ONE","\u180C": "MONGOLIAN FREE VARIATION SELECTOR TWO","\u180D": "MONGOLIAN FREE VARIATION SELECTOR THREE",}


# =========================
# 4. processing function
# =========================

def remove_suffixes(text, suffixes):
    """
   Remove user-specified affixes/suffixes from the text used for counting.The original text will not be modified.
    """
    processed = text

    for suffix in suffixes:
        if suffix:
            processed = processed.replace(suffix, "")

    return processed


def analyze_special_characters(text):
    results = []

    for position, char in enumerate(text):
        if char in SPECIAL_CHARS:
            results.append({"position": position + 1,"character": repr(char),"code_point": f"U+{ord(char):04X}","name": SPECIAL_CHARS[char]})

    return results


# =========================
# 5. Start detection
# =========================

if st.button("Start detection"):

    if not text:
        st.warning("Please enter the Mongolian text here")

    else:

        # ---------------------------------
        # original statistics
        # ---------------------------------

        original_count = len(text)

        # ---------------------------------
        # whitespace detection
        # ---------------------------------

        whitespace_count = 0
        whitespace_positions = []

        for position, char in enumerate(text):
            if char.isspace():
                whitespace_count += 1
                whitespace_positions.append({
                    "position": position + 1,
                    "character": repr(char),
                    "code_point": f"U+{ord(char):04X}",
                    "name": unicodedata.name(char, "UNKNOWN")})

        # ---------------------------------
        # remove whitespace 
        # ---------------------------------

        text_without_spaces = "".join(
            char for char in text
            if not char.isspace()
        )

        count_without_spaces = len(text_without_spaces)

        # ---------------------------------
        # affixes/ suffixes rule
        # ---------------------------------

        suffixes = [line.strip()
                    for line in suffix_input.splitlines()
                    if line.strip() != ""]

        # Continue processing the text after whitespace removal.
        processed_text = remove_suffixes(text_without_spaces,suffixes)

        final_count = len(processed_text)

        # ---------------------------------
        # special Unicode character detection
        # ---------------------------------

        special_results = analyze_special_characters(text)

        # ================================
        # Basic Statistics
        # ================================

        st.subheader("1. Basic Statistics")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Original UniCode Code Points",original_count)

        with col2:
            st.metric("Whitespace Characters",whitespace_count)

        with col3:
            st.metric("Code Points After Removing Whitespace",count_without_spaces)

        with col4:
            st.metric("Final Character Count",final_count)

        st.info("Note: Character counts are based on Unicode code points, A Unicode code point does not always correspond to one visually perceived""character or Linguistic unit.")

        # ================================
        # Space Detection
        # ================================

        st.subheader("2. Space Detection and Handling")

        if whitespace_count > 0:

            st.write(f"**{whitespace_count}** whitespace character(s) were detected.")

            st.dataframe(whitespace_positions,use_container_width=True)

            st.write("Whitespace characters are excluded from the final character count,""but the original text remains unchanged.")

        else:

            st.success("No whitespace characters detected")

        # ================================
        # Special Unicode Characters
        # ================================

        st.subheader("3. Special Unicode Character Detection")

        if special_results:

            st.write(
                f"**{len(special_results)}** special Unicode character(s)were detected.")

            st.dataframe(special_results,use_container_width=True)

        else:

            st.success("No special  Unicode character listed in this tool were detected.")

        # ================================
        # Affix / Suffix Exclusion
        # ================================

        st.subheader("4. Traditional Mongolian Affix / Suffix Exclusion")

        if suffixes:

            st.write("Affix/suffix rules used in this analysis:")

            for suffix in suffixes:
                st.code(f"{repr(suffix)}   →   {len(suffix)} code point(s)")

            removed_by_suffix = (count_without_spaces - final_count)

            st.write(
                f"Excluded from the character count based on these rules "
                f"**{removed_by_suffix}**code points.")

        else:

            st.info(
                "No affix or suffix exclusion rules were entered for this analysis."
                "Therefore,no affixes or suffixes were excluded from the character count.")

        # ================================
        # Original vs Processed
        # ================================

        st.subheader("5. Original Text vs. Processed Text")

        col1, col2 = st.columns(2)

        with col1:

            st.markdown("### Original Text")

            st.text_area("Original text",value=text,height=250,disabled=True,key="original_text")

            st.write(f"Original Unicode Code Points: **{original_count}**")

        with col2:

            st.markdown("### Processed Text")

            st.text_area(
                "processed text",
                value=processed_text,
                height=250,
                disabled=True,
                key="processed_text"
            )

            st.write(
                f"Processed Character Count: **{final_count}**"
            )

        # ================================
        # Comparison Summary
        # ================================

        st.subheader("6. Comparison")

        difference = original_count - final_count

        st.write(
            f"Original Unicode Code Point Count：**{original_count}**"
        )

        st.write(
            f"After Removing Whitspace：**{count_without_spaces}**"
        )

        st.write(
            f"After Excluding Specified Affixes/Suffixes:**{final_count}**"
        )

        st.write(
            f"Total Reduction:**{difference}**code points")

        st.success(
            "The original text remains unchanged,""The processed text is used only for character counting and comparison.")
