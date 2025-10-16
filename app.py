import streamlit as st
import requests

st.set_page_config(page_title="skillpathAI – Personalized 7-Day Learning Path", layout="centered")

st.title("skillpathAI")
st.write("Personalized 7-Day Learning Path Generator")

API_BASE_URL = "http://127.0.0.1:8000"

def generate_plan(topic):
    url = f"{API_BASE_URL}/generate_plan"
    response = requests.post(url, json={"topic": topic})
    return response.json()

topic = st.text_input("Enter a learning topic:", placeholder="e.g., Python for Data Analysis")

if st.button("Generate 7-Day Learning Plan"):
    if topic.strip() == "":
        st.warning("Please enter a topic before generating a plan.")
    else:
        with st.spinner("Generating your personalized learning plan..."):
            try:
                plan = generate_plan(topic)
                st.success("Your learning plan is ready!")

                for day in plan:
                    st.subheader(day.get("day", ""))
                    st.write(f"**Topic:** {day.get('topic', '')}")
                    st.write(f"**Mini Challenge:** {day.get('mini_challenge', '')}")
                    st.write(f"**Reasoning:** {day.get('reasoning', '')}")

                    if day.get("resources"):
                        st.write("**Recommended Resources:**")
                        for res in day["resources"]:
                            st.markdown(f"- **{res['type']}**: [{res['title']}]({res['url']})")

                    st.divider()

            except Exception as e:
                st.error(f"Failed to generate plan: {e}")
