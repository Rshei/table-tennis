import streamlit as st
import random

# Initialize session state
if 'participants' not in st.session_state:
    st.session_state.participants = []
if 'matches' not in st.session_state:
    st.session_state.matches = []
if 'winner' not in st.session_state:
    st.session_state.winner = None

# App title
st.title("Workplace Table Tennis Tournament")

# Participant registration
st.header("Participant Registration")
with st.form("participant_form"):
    full_name = st.text_input("Full Name")
    submit_button = st.form_submit_button("Add Participant")

if submit_button:
    if full_name:
        st.session_state.participants.append(full_name)
        st.success(f"Participant '{full_name}' added successfully!")
    else:
        st.error("Please enter a full name.")

# Display registered participants
st.header("Registered Participants")
if st.session_state.participants:
    for participant in st.session_state.participants:
        st.write(participant)
else:
    st.write("No participants registered yet.")

# Tournament bracket generation
st.header("Tournament Bracket")
if st.button("Generate Bracket"):
    if len(st.session_state.participants) < 2:
        st.error("At least 2 participants are required to generate a bracket.")
    else:
        random.shuffle(st.session_state.participants)
        participants = st.session_state.participants[:]
        st.session_state.matches = []
        while len(participants) > 1:
            round_matches = []
            for i in range(len(participants) // 2):
                round_matches.append((participants[i], participants[len(participants) - i - 1]))
            if len(participants) % 2 != 0:
                round_matches.append((participants[len(participants) // 2], "BYE"))
            st.session_state.matches.append(round_matches)
            participants = [f"Winner of Match {i+1}" for i in range(len(round_matches))]
        st.success("Bracket generated successfully!")

# Display tournament bracket
if st.session_state.matches:
    st.header("Tournament Matches")
    for i, round_matches in enumerate(st.session_state.matches):
        st.write(f"Round {i+1}:")
        for j, match in enumerate(round_matches):
            st.write(f"Match {j+1}: {match[0]} vs {match[1]}")
