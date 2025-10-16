import streamlit as st
from services.llm_client import GeminiLLM
import json

st.set_page_config(page_title="SkillPath AI – Personalized 7-Day Learning Path", layout="centered")

st.title("skillpathAI")
st.write("Personalized 7-Day Learning Path Generator")

topic = st.text_input("Enter a learning topic:", placeholder="e.g., Python for Data Analysis")

if st.button("Generate 7-Day Learning Plan"):
    if not topic.strip():
        st.warning("Please enter a topic before generating a plan.")
    else:
        with st.spinner("Generating your personalized learning plan..."):
            try:
                llm = GeminiLLM()
                plan = llm.generate_learning_plan(topic)
                st.success("Your learning plan is ready!")

                for day_data in plan:
                    st.subheader(day_data.get("day", ""))
                    st.write(f"**Topic:** {day_data.get('topic', '')}")
                    st.write(f"**Mini Challenge:** {day_data.get('mini_challenge', '')}")
                    st.write(f"**Reasoning:** {day_data.get('reasoning', '')}")

                    resources = day_data.get("resources", [])
                    if resources:
                        st.write("**Recommended Resources:**")
                        for res in resources:
                            res_type = res.get("type", "")
                            res_title = res.get("title", "")
                            res_url = res.get("url", "")
                            st.markdown(f"- **{res_type}**: [{res_title}]({res_url})")

                    st.divider()

            except Exception as e:
                st.error(f"Failed to generate plan: {e}")
