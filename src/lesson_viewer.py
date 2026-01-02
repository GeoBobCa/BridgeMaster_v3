import streamlit as st
import json
from pathlib import Path

def render_hand(hand_data):
    """Draws a visual representation of a single hand."""
    # A simple ASCII-style rendering, or you could use columns
    cols = st.columns(4)
    suits = ['S', 'H', 'D', 'C']
    colors = {'S': 'blue', 'H': 'red', 'D': 'orange', 'C': 'green'}
    suit_sym = {'S': '♠', 'H': '♥', 'D': '♦', 'C': '♣'}

    # We need to parse the PBN string or use the summary provided in JSON
    # For now, let's use the summary text if available, or just display raw
    # Simpler: Just display the text summary for N and S
    
    with cols[1]: # North
        st.markdown(f"**NORTH**")
        st.caption(f"HCP: {hand_data['hands_summary']['N_hcp']}")
        st.code(hand_data['hands_summary']['N_shape']) # e.g. 5=4=3=1

    with cols[1]: # South (Visual trick to stack them)
        st.markdown("---")
        st.markdown(f"**SOUTH**")
        st.caption(f"HCP: {hand_data['hands_summary']['S_hcp']}")
        st.code(hand_data['hands_summary']['S_shape'])

    # Display the PBN for copying
    st.text_area("PBN (Copy for Bridge Software)", hand_data['pbn'], height=70)

def show_lesson_viewer():
    st.header("🎓 Lesson Library")

    # 1. Find all JSON lessons
    lessons_dir = Path("lessons")
    if not lessons_dir.exists():
        st.warning("No lessons found. Run 'src/lesson_builder.py' first!")
        return

    files = list(lessons_dir.glob("*.json"))
    if not files:
        st.info("The 'lessons' folder is empty.")
        return

    # 2. Select a Lesson
    selected_file = st.selectbox("Choose a Lesson:", files, format_func=lambda x: x.stem.replace('_', ' ').title())
    
    # 3. Load Data
    with open(selected_file, "r") as f:
        data = json.load(f)

    st.subheader(f"📂 {data['title']}")
    st.caption(f"Target Sequence: {' - '.join(data['target_sequence'])}")

    # 4. Flip through Examples
    # Session state to track which hand we are viewing
    if 'lesson_index' not in st.session_state:
        st.session_state.lesson_index = 0

    examples = data['examples']
    total = len(examples)
    
    # Navigation Buttons
    c1, c2, c3 = st.columns([1, 2, 1])
    with c1:
        if st.button("⬅️ Previous"):
            st.session_state.lesson_index = max(0, st.session_state.lesson_index - 1)
    with c3:
        if st.button("Next ➡️"):
            st.session_state.lesson_index = min(total - 1, st.session_state.lesson_index + 1)
    
    # Show Content
    current_hand = examples[st.session_state.lesson_index]
    
    with st.container(border=True):
        st.markdown(f"### Hand #{current_hand['id']}")
        render_hand(current_hand)
        
        st.success(f"**💡 Teaching Point:** {current_hand['teaching_point']}")
        st.info(f"**Auction:** {' - '.join(current_hand['auction'])}")