import streamlit as st
import requests

st.set_page_config(page_title="skillpathAI – Personalized 7-Day Learning Path", layout="centered")

API_BASE_URL = "http://127.0.0.1:8000"

def generate_plan(topic):
    response = requests.post(f"{API_BASE_URL}/generate_plan", json={"topic": topic})
    response.raise_for_status()
    return response.json()

def get_detailed_day(topic, day_topic, day_number):
    response = requests.post(f"{API_BASE_URL}/get_detailed_day", json={
        "topic": topic,
        "day_topic": day_topic,
        "day_number": day_number
    })
    response.raise_for_status()
    return response.json()

# Initialize session state
if 'plan' not in st.session_state:
    st.session_state['plan'] = None
if 'current_day' not in st.session_state:
    st.session_state['current_day'] = None
if 'detailed_day_data' not in st.session_state:
    st.session_state['detailed_day_data'] = None
if 'original_topic' not in st.session_state:
    st.session_state['original_topic'] = None

# --- Detailed Day Page ---
if st.session_state['current_day']:
    # Find the day data safely
    day_data = None
    for d in st.session_state['plan']:
        if d['day'] == st.session_state['current_day']:
            day_data = d
            break
    
    if not day_data:
        st.error("Day not found. Returning to main page.")
        st.session_state['current_day'] = None
        st.rerun()
    
    # Load detailed day data if not already loaded
    if not st.session_state['detailed_day_data'] or st.session_state['detailed_day_data']['day'] != st.session_state['current_day']:
        with st.spinner("Loading detailed learning plan..."):
            try:
                # Extract day number more safely
                day_str = st.session_state['current_day']
                if "Day" in day_str:
                    day_number = int(day_str.split()[-1])  # Get the last part after splitting
                else:
                    day_number = 1  # Default fallback
                

                st.session_state['detailed_day_data'] = get_detailed_day(
                    st.session_state['original_topic'], 
                    day_data['topic'], 
                    day_number
                )
            except Exception as e:
                st.error(f"Failed to load detailed plan: {e}")
                st.error(f"Debug info: current_day='{st.session_state['current_day']}', original_topic='{st.session_state.get('original_topic', 'None')}'")
                st.session_state['current_day'] = None
                st.rerun()
    
    detailed_data = st.session_state['detailed_day_data']
    
    # Navigation
    col1, col2 = st.columns([1, 4])
    with col1:
        if st.button("← Back to Overview"):
            st.session_state['current_day'] = None
            st.session_state['detailed_day_data'] = None
            st.rerun()
    
    # Header
    st.title(f"{detailed_data['day']}: {detailed_data['topic']}")
    
    # Key Info Cards
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Estimated Time", detailed_data.get('estimated_time', 'N/A'))
    with col2:
        st.metric("Difficulty", detailed_data.get('difficulty_level', 'N/A'))
    with col3:
        st.metric("Objectives", f"{len(detailed_data.get('learning_objectives', []))}")
    
    st.divider()
    
    # Detailed Description
    st.subheader("What You'll Learn Today")
    st.write(detailed_data.get('detailed_description', ''))
    
    # Learning Objectives
    if detailed_data.get('learning_objectives'):
        st.subheader("Learning Objectives")
        for i, objective in enumerate(detailed_data['learning_objectives'], 1):
            st.write(f"{i}. {objective}")
    
    # Prerequisites
    if detailed_data.get('prerequisites'):
        st.subheader("Prerequisites")
        for prereq in detailed_data['prerequisites']:
            st.write(f"• {prereq}")
    
    # Key Concepts
    if detailed_data.get('key_concepts'):
        st.subheader("Key Concepts")
        cols = st.columns(2)
        for i, concept in enumerate(detailed_data['key_concepts']):
            with cols[i % 2]:
                st.info(f"{concept}")
    
    st.divider()
    
    # Step-by-Step Guide
    if detailed_data.get('step_by_step_guide'):
        st.subheader("Step-by-Step Learning Guide")
        for i, step in enumerate(detailed_data['step_by_step_guide'], 1):
            with st.expander(f"Step {i}", expanded=i==1):
                st.write(step)
    
    # Challenge Section
    st.subheader("Today's Challenge")
    
    # Mini Challenge
    st.write("**Quick Challenge:**")
    st.info(detailed_data.get('mini_challenge', ''))
    
    # Detailed Challenge
    if detailed_data.get('detailed_challenge'):
        with st.expander("Detailed Challenge Instructions", expanded=False):
            st.write(detailed_data['detailed_challenge'])
    
    st.divider()
    
    # Resources Section
    st.subheader("Learning Resources")
    if detailed_data.get('resources'):
        # Group resources by type
        resource_types = {}
        for res in detailed_data['resources']:
            res_type = res.get('type', 'Other')
            if res_type not in resource_types:
                resource_types[res_type] = []
            resource_types[res_type].append(res)
        
        # Display resources by type
        for res_type, resources in resource_types.items():
            st.write(f"**{res_type} Resources:**")
            for res in resources:
                with st.expander(f"{res.get('title', 'Untitled')}", expanded=False):
                    if res.get('snippet'):
                        st.write(res['snippet'])
                    st.markdown(f"🔗 [Open Resource]({res.get('url', '#')})")
            st.write("")
    
    # Next Steps
    if detailed_data.get('next_steps'):
        st.subheader("What's Next?")
        st.success(detailed_data['next_steps'])
    
    # Reasoning
    if detailed_data.get('reasoning'):
        with st.expander("Why This Topic Today?", expanded=False):
            st.write(detailed_data['reasoning'])

# --- Main 7-Day Overview ---
else:
    st.title("skillpathAI")
    st.write("Personalized 7-Day Learning Path Generator")

    topic = st.text_input("Enter a learning topic:", placeholder="e.g., Python for Data Analysis")

    if st.button("Generate 7-Day Learning Plan"):
        if topic.strip() == "":
            st.warning("Please enter a topic.")
        else:
            with st.spinner("Generating your personalized learning plan..."):
                try:
                    st.session_state['plan'] = generate_plan(topic)
                    st.session_state['original_topic'] = topic
                    st.success("Your learning plan is ready!")
                except Exception as e:
                    st.error(f"Failed to generate plan: {e}")

    if st.session_state['plan']:
        st.success("Click on any day to start learning!")
        for day in st.session_state['plan']:
            st.subheader(day['day'])
            st.write(f"**Topic:** {day['topic']}")
            st.write(f"**Mini Challenge:** {day['mini_challenge']}")
            st.write(f"**Reasoning:** {day['reasoning']}")
            
            if day.get("resources"):
                st.write("**Recommended Resources:**")
                for res in day["resources"]:
                    st.markdown(f"- **{res['type']}**: [{res['title']}]({res['url']})")
            
            if st.button(f"Start Learning - {day['day']}", key=f"btn_{day['day']}"):
                st.session_state['current_day'] = day['day']
                st.rerun()
            
            st.divider()
