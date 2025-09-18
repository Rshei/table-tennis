import streamlit as st
import random

# Initialize session state
if 'participants' not in st.session_state:
    st.session_state.participants = []
if 'matches' not in st.session_state:
    st.session_state.matches = []
if 'winner' not in st.session_state:
    session_state.winner = None

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
        st.session_state.matches = []
        for i in range(len(st.session_state.participants) // 2):
            st.session_state.matches.append((st.session_state.participants[i], st.session_state.participants[len(st.session_state.participants) - i - 1]))
        st.success("Bracket generated successfully!")

# Display tournament bracket
if st.session_state.matches:
    st.header("Tournament Matches")
    for i, match in enumerate(st.session_state.matches):
        st.write(f"Match {i+1}: {match[0]} vs {match[1]}")

# Winner selection
st.header("Select Winner")
if st.session_state.matches:
    match_number = st.selectbox("Select Match", range(1, len(st.session_state.matches) + 1))
    winner = st.selectbox("Select Winner", [st.session_state.matches[match_number - 1][0], st.session_state.matches[match_number - 1][1]])
    if st.button("Submit Winner"):
        st.session_state.winner = winner
        st.success(f"Winner of Match {match_number} is {winner}!")

# Display winner
if st.session_state.winner:
    st.header("Tournament Winner")
    st.write(st.session_state.winner)
