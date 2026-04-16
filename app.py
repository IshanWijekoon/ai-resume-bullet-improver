import streamlit as st
import re
from prompts import get_prompt
from ai_engine import improve_bullet
from utils import calculate_ats_score


st.set_page_config(page_title="AI Resume Bullet Improver", layout="wide")


def load_css():
    with open("styles.css", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


def parse_response_sections(response_text):
    sections = {
        "Improved Bullet": "",
        "Quantified Version": "",
        "Explanation": "",
    }

    text = response_text or ""
    pattern = re.compile(r"(?is)(Improved Bullet|Quantified Version|Explanation)\s*:\s*")
    parts = pattern.split(text)

    if len(parts) <= 1:
        sections["Improved Bullet"] = (response_text or "").strip()
        return sections

    for i in range(1, len(parts), 2):
        section_name = parts[i].strip()
        section_content = parts[i + 1].strip() if i + 1 < len(parts) else ""
        if section_name in sections:
            sections[section_name] = section_content

    return sections


load_css()

if "bullet_input" not in st.session_state:
    st.session_state.bullet_input = ""

if "last_result" not in st.session_state:
    st.session_state.last_result = ""

st.markdown(
    """
    <h1 class="app-title">AI Resume Bullet Improver</h1>
    <p class="app-subtitle">Turn weak resume bullets into ATS-optimized statements.</p>
    """,
    unsafe_allow_html=True,
)

st.divider()

left_col, right_col = st.columns([2, 1], gap="large")

with left_col:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("### Input")
    st.text_area(
        "Enter your resume bullet:",
        key="bullet_input",
        height=170,
        placeholder="Example: Helped improve customer onboarding by creating support docs and tracking common issues.",
        label_visibility="collapsed",
    )
    st.markdown("</div>", unsafe_allow_html=True)

with right_col:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    tone = st.selectbox(
        "Select tone:",
        ["Intern", "Professional", "Leadership"],
    )

    st.markdown("<br>", unsafe_allow_html=True)

    improve_clicked = st.button(
        "Improve Bullet",
        use_container_width=True,
        disabled=st.session_state.bullet_input.strip() == "",
    )
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

if improve_clicked:
    with st.spinner("Improving your bullet..."):
        prompt = get_prompt(
            st.session_state.bullet_input,
            tone,
            role=None,
            industry=None,
            years_experience=None,
        )
        result = improve_bullet(prompt)
        st.session_state.last_result = result

    st.success("Generated successfully. Review and copy your upgraded bullet below.")

if st.session_state.last_result:
    parsed = parse_response_sections(st.session_state.last_result)
    improved = parsed.get("Improved Bullet", "").strip() or st.session_state.last_result.strip()
    quantified = parsed.get("Quantified Version", "").strip()
    explanation = parsed.get("Explanation", "").strip()

    st.divider()

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("### Improved Bullet")
    st.code(improved, language="markdown")
    st.markdown("</div>", unsafe_allow_html=True)

    score = calculate_ats_score(st.session_state.last_result)

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("### ATS Score")
    st.progress(score)
    st.write(f"Score: {score}/100")

    if score < 60:
        st.warning("Needs more measurable impact. Add metrics like %, revenue, time saved, or scale.")
    elif score <= 80:
        st.info("Solid baseline. A stronger action verb or clearer outcome can push it higher.")
    else:
        st.success("Excellent bullet quality. Strong ATS signals and impact framing.")
    st.markdown("</div>", unsafe_allow_html=True)



