import streamlit as st
from prompts import get_prompt
from ai_engine import improve_bullet
from utils import calculate_ats_score

st.set_page_config(page_title = "AI Resume Bullet Improver", layout = "centered")

st.title("AI Resume Bullet Improver")
st.markdown("Turn weak resume bullets into **ATS-optimized statements**.")

# input
bullet = st.text_area("Enter your resume bullet:", height = 120)

tone = st.selectbox(
    "select tone:",
    ["Intern", "Professional", "Leadership"]
)

if st.button("Improve Bullet"):
    if bullet.strip() == "":
        st.warning("Please enter a bullet point.")
    else:
        with st.spinner("Improving your bullet..."):
            prompt = get_prompt(bullet, tone, role=None, industry=None, years_experience=None)
            result = improve_bullet(prompt)

            st.success("Done!")

            st.subheader("Improved Output")
            st.write(result)

            # ATS score
            score = calculate_ats_score(result)

            st.subheader("ATS Score")
            st.progress(score)
            st.write(f"Score: {score}/100")

            if score < 60:
                st.warning("Try adding measurable impact (numbers, %).")
            elif score < 80:
                st.info("Good, but can be slightly stronger")
            else:
                st.success("Execellent bullet!")

