import streamlit as st
import unicodedata

st.set_page_config(
    page_title="Traditional Mongolian Text Analyzer",page_icon="ᠮ",layout="wide")

st.title("Traditional Mongolian Text Analyzer")
st.write("Traditional Mongolian Text Analyzer")

# =========================
# 1. Please enter the Mongolian text here
# =========================

text = st.text_area("Please enter or past Traditioanl Mongolian Text here：",height=250,placeholder="Please enter the Mongolian text here")

# =========================
# 2. Affix/suffix rule
# =========================

st.subheader("Affix/suffix exclution rule")

st.write(
    "Please enter or past the affixes or suffixes to be excluded from character counting"
    "Enter one rule per line, the original text will not be modified.")

suffix_input = st.text_area(
    "Suffixes and affixes to be excluded：",height=120,placeholder="例如：\n ᠤ\nᠤ\nᠠ᠋")

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
            results.append({
                "position": position + 1,
                "character": repr(char),
                "code_point": f"U+{ord(char):04X}",
                "name": SPECIAL_CHARS[char]
            })

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

        suffixes = [
            line for line in suffix_input.splitlines()
            if line.strip() != ""
        ]

        # Continue processing the text after whitespace removal.
        processed_text = remove_suffixes(
            text_without_spaces,
            suffixes
        )

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
            st.metric(
                "Original Code Points",
                original_count
            )

        with col2:
            st.metric(
                "Whitespace",
                whitespace_count
            )

        with col3:
            st.metric(
                "After Removing Spaces",
                count_without_spaces
            )

        with col4:
            st.metric(
                "Final Character Count",
                final_count
            )

        st.info(
            "Note: Character counts here are based on Unicode code points, which do not necessarily correspond to visually perceived glyphs or linguistic characters.")

        # ================================
        # Space Detection
        # ================================

        st.subheader("2. Space Detection and Handling")

        if whitespace_count > 0:

            st.write(
                f"detected **{whitespace_count}** whitespace character."
            )

            st.dataframe(
                whitespace_positions,
                use_container_width=True
            )

            st.write(
                "Whitespace characters are excluded from the final character count,"
                "but the original text remains unchanged.")

        else:

            st.success("No whitespace characters detected")

        # ================================
        # Special Unicode Characters
        # ================================

        st.subheader("3. Special Unicode Character Detection")

        if special_results:

            st.write(
                f"detected **{len(special_results)}** special Unicode character。")

            st.dataframe(
                special_results,
                use_container_width=True
            )

        else:

            st.success(
                "no special  Unicode character listed in this tool were detected.")

        # ================================
        # Affix / Suffix Exclusion
        # ================================

        st.subheader("4. Traditional Mongolian Affix / Suffix Exclusion")

        if suffixes:

            st.write("suffix rule used in this analysis：")

            for suffix in suffixes:
                st.code(
                    f"{repr(suffix)}   →   {len(suffix)} code point(s)"
                )

            removed_by_suffix = (
                count_without_spaces - final_count
            )

            st.write(
                f"excluded from the statistics based on this rule "
                f"**{removed_by_suffix}** 个 code points。"
            )

        else:

            st.info(
                "No affix or suffix exclusion rules were entered for this analysis. Therefore,"
                "no affixes or suffixes were excluded from the statistics."
            )

        # ================================
        # Original vs Processed
        # ================================

        st.subheader("5. Original Text vs. Processed Text")

        col1, col2 = st.columns(2)

        with col1:

            st.markdown("### Original Text")

            st.text_area(
                "original text",
                value=text,
                height=250,
                disabled=True,
                key="original_text"
            )

            st.write(
                f"Original Code Points: **{original_count}**"
            )

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
            f"original Unicode point count：**{original_count}**"
        )

        st.write(
            f"after excluding whitspace characters：**{count_without_spaces}**"
        )

        st.write(
            f"after excluding specified affix or suffix：**{final_count}**"
        )

        st.write(
            f"final reduction code points：**{difference}**"
        )

        st.success(
            "the original text remains unchanged,the processed text is used for character counting and comparison purposes only"
        )
