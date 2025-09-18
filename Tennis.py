import streamlit as st
import random
from streamlit_react_flow import react_flow

# Initialize session state
if 'participants' not in st.session_state:
    st.session_state.participants = []
if 'matches' not in st.session_state:
    st.session_state.matches = []
if 'winners' not in st.session_state:
    st.session_state.winners = {}
if 'current_round' not in st.session_state:
    st.session_state.current_round = 0

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


# --- Enhanced Bracket Visualization with React Flow ---
def build_react_flow_elements(matches):
    nodes = []
    edges = []
    y_gap = 120
    x_gap = 220
    node_id = 0
    prev_round_node_ids = []
    for round_idx, round_matches in enumerate(matches):
        round_node_ids = []
        for match_idx, match in enumerate(round_matches):
            label = f"{match[0]} vs {match[1]}" if match[1] != "BYE" else f"{match[0]} (BYE)"
            node = {
                "id": str(node_id),
                "data": {"label": label},
                "position": {"x": round_idx * x_gap, "y": match_idx * y_gap},
                "type": "default"
            }
            nodes.append(node)
            round_node_ids.append(node_id)
            # Connect to previous round
            if round_idx > 0 and match_idx < len(prev_round_node_ids):
                edges.append({
                    "id": f"e{prev_round_node_ids[match_idx]}-{node_id}",
                    "source": str(prev_round_node_ids[match_idx]),
                    "target": str(node_id)
                })
            node_id += 1
        prev_round_node_ids = round_node_ids
    return nodes, edges

if st.session_state.matches:
    st.header("Bracket Visualization")
    nodes, edges = build_react_flow_elements(st.session_state.matches)
    # Removed fit_view=True, not supported by current streamlit-react-flow
    react_flow(nodes, edges, style={"width": "100%", "height": "500px", "background": "#f0f2f6"})

    # Winner selection UI (keep as before, below the visualization)
    for i, round_matches in enumerate(st.session_state.matches):
        st.write(f"**Round {i+1}**")
        for j, match in enumerate(round_matches):
            if i == st.session_state.current_round:
                winner = st.selectbox(f"Match {j+1} Winner", [match[0], match[1]])
                if st.button(f"Submit Winner for Match {j+1}"):
                    st.session_state.winners[f"Match {j+1}"] = winner
                    if i < len(st.session_state.matches) - 1:
                        next_round_match_index = j // 2
                        next_round_match = st.session_state.matches[i + 1][next_round_match_index]
                        if j % 2 == 0:
                            st.session_state.matches[i + 1][next_round_match_index] = (winner, next_round_match[1])
                        else:
                            st.session_state.matches[i + 1][next_round_match_index] = (next_round_match[0], winner)
                    if j == len(round_matches) - 1:
                        st.session_state.current_round += 1
            else:
                st.write(f"Match {j+1}: {match[0]} vs {match[1]}")
                if f"Match {j+1}" in st.session_state.winners:
                    st.write(f"Winner: {st.session_state.winners[f'Match {j+1}']}")
