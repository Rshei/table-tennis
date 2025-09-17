import streamlit as st
import math
import random
import json

st.title("Tournament Bracket Generator")

st.header("Participant Registration")

# 3. Add a number input widget for the number of participants
num_participants = st.number_input("Define the number of participants:", min_value=2, value=20, step=1, key='num_participants_input')

# 4. Use Streamlit's session state to store the list of registered participants
if 'registered_participants' not in st.session_state:
    st.session_state.registered_participants = []

# 5. Add a text input widget for participant names
participant_name = st.text_input("Enter Participant Name:", key='participant_name_input')

# 6. Add a button labeled "Add Participant"
add_participant_button = st.button("Add Participant", key='add_participant_button')

# 7. Implement logic for adding participants
if add_participant_button:
    name = participant_name.strip()
    if not name:
        st.error("Please enter a name.")
    elif len(st.session_state.registered_participants) >= num_participants:
        st.warning(f"Maximum of {int(num_participants)} participants reached.")
    elif name in st.session_state.registered_participants:
        st.warning(f"Participant '{name}' is already registered.")
    else:
        st.session_state.registered_participants.append(name)
        st.success(f"Participant '{name}' added.")
        # Clear the text input field after adding a participant
        st.session_state.participant_name_input = "" # Clear the input widget using its key


# Display the list of registered participants
st.subheader(f"Registered Participants: {len(st.session_state.registered_participants)}/{int(num_participants)}")
if st.session_state.registered_participants:
    st.write(", ".join(st.session_state.registered_participants))
else:
    st.write("No participants registered yet.")

# Define the bracket generation function
def generate_tournament_bracket(participant_names):
    """
    Generates a single-elimination tournament bracket structure.

    Args:
        participant_names: A list of strings, where each string is a participant's name.

    Returns:
        A dictionary representing the tournament rounds and their pairings.
    """
    num_participants = len(participant_names)
    if num_participants < 2:
        return {"Round 1": []} # Not enough participants for a tournament

    # 1. Determine the number of byes
    next_power_of_2 = 2**math.ceil(math.log2(num_participants))
    num_byes = next_power_of_2 - num_participants
    num_first_round_matches = num_participants - num_byes

    # 3. Randomly shuffle the list of participants
    shuffled_participants = participant_names[:] # Create a copy to avoid modifying the original list
    random.shuffle(shuffled_participants)

    # 4. Separate the participants into those who receive byes and those who will play in the first round
    participants_with_byes = shuffled_participants[:num_byes]
    participants_first_round = shuffled_participants[num_byes:]

    # 5. Generate the pairings for the first round matches
    first_round_pairings = []
    for i in range(0, len(participants_first_round), 2):
        if i + 1 < len(participants_first_round): # Ensure there's a pair
             first_round_pairings.append([participants_first_round[i], participants_first_round[i+1]]) # Use list for mutability
        elif len(participants_first_round) % 2 != 0: # Handle case with odd number of first round participants
             first_round_pairings.append([participants_first_round[i], 'Bye']) # This shouldn't happen with correct bye calculation, but as a safeguard


    # 6. Structure the subsequent rounds
    tournament_rounds = {'Round 1': first_round_pairings}

    current_round_participants = participants_with_byes + [f'Winner of Round 1 Match {i+1}' for i in range(len(first_round_pairings))]
    # Shuffle for the next round - this simulates random seeding or outcomes for subsequent rounds
    random.shuffle(current_round_participants)

    round_num = 2
    while len(current_round_participants) > 1:
        next_round_pairings = []
        for i in range(0, len(current_round_participants), 2):
            if i + 1 < len(current_round_participants):
                next_round_pairings.append([current_round_participants[i], current_round_participants[i+1]]) # Use list for mutability
            else:
                # Handle case where there's an odd number of participants (a bye in this round)
                next_round_pairings.append([current_round_participants[i], 'Bye'])

        round_name = f'Round {round_num}'
        tournament_rounds[round_name] = next_round_pairings

        # Prepare participants for the next round - winners of current round matches
        current_round_participants = [f'Winner of {round_name} Match {i+1}' for i in range(len(next_round_pairings))]
        random.shuffle(current_round_participants) # Shuffle for the next round
        round_num += 1

    # Add the final winner placeholder if the loop finished with one participant
    if len(current_round_participants) == 1:
         tournament_rounds[f'Round {round_num-1} Final'] = [[current_round_participants[0], 'Champion']] # Or a similar final representation


    return tournament_rounds


# Add a "Create Match Table" button
# Implement logic to enable the button when participant count is met
create_bracket_button = st.button(
    "Create Match Table",
    disabled=len(st.session_state.registered_participants) != num_participants,
    key='create_bracket_button'
)

st.header("Tournament Bracket")

# Add a state variable to trigger bracket re-render
if 'rerun_bracket' not in st.session_state:
    st.session_state.rerun_bracket = False

# Modify the logic associated with the "Create Match Table" button
if create_bracket_button:
    # 8. Store the generated bracket structure in st.session_state
    st.session_state.tournament_bracket = generate_tournament_bracket(st.session_state.registered_participants)
    st.success("Tournament bracket generated!")
    st.session_state.rerun_bracket = True # Trigger re-render


# Function to render HTML for bracket visualization with improved CSS and interactivity
def render_bracket_html_improved(bracket_data):
    bracket_json = json.dumps(bracket_data) # Convert Python dict to JSON string

    html_content = f"""
    <style>
    /* Refined Styles */
    body {{
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        line-height: 1.6;
        margin: 0;
        padding: 30px;
        background-color: #e8f5e9; /* Light green background */
        color: #333;
        min-height: 100vh;
    }}

    h2, h3 {{
        color: #d32f2f; /* Darker red for headings */
        text-align: center;
        margin-bottom: 20px;
        font-weight: 600;
    }}

    /* Registration Form Styling - Refined */
    #registration-form {{
        max-width: 550px;
        margin: 30px auto;
        padding: 25px;
        background-color: #fff;
        border-radius: 10px;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.15);
        text-align: center;
        display: flex;
        flex-direction: column;
        gap: 15px;
    }}

    #registration-form label {{
        font-weight: 600;
        color: #4caf50; /* Green color for label */
    }}

    #num-participants {{
        padding: 10px;
        border: 1px solid #a5d6a7;
        border-radius: 5px;
        font-size: 1rem;
        text-align: center;
        width: 80px;
        margin-left: 10px;
    }}


    #participant-name {{
        flex-grow: 1;
        padding: 12px;
        border: 1px solid #a5d6a7;
        border-radius: 5px;
        font-size: 1rem;
        transition: border-color 0.3s ease, box-shadow 0.3s ease;
    }}

     #participant-name:focus {{
         border-color: #4caf50;
         box-shadow: 0 0 8px rgba(76, 175, 80, 0.3);
         outline: none;
     }}


    #add-participant {{
        padding: 12px 20px;
        background-color: #4caf50; /* Green */
        color: white;
        border: none;
        border-radius: 5px;
        cursor: pointer;
        font-size: 1rem;
        transition: background-color 0.3s ease, transform 0.1s ease;
    }}

    #add-participant:hover {{
        background-color: #388e3c; /* Darker green */
        transform: translateY(-2px);
    }}

     #add-participant:active {{
         transform: translateY(0);
     }}


    #participant-list {{
        list-style: none;
        padding: 0;
        margin-top: 20px;
        max-height: 200px;
        overflow-y: auto;
        border-top: 1px solid #c8e6c9;
        padding-top: 15px;
        background-color: #f9fbe7; /* Very light yellowish-green background */
        border-radius: 5px;
    }}

    #participant-list li {{
        background-color: #e8f5e9; /* Light green */
        padding: 10px;
        margin-bottom: 8px;
        border-radius: 5px;
        text-align: left;
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-left: 5px solid #4caf50; /* Green left border */
        transition: background-color 0.2s ease;
    }}

     #participant-list li:hover {{
         background-color: #dcedc8; /* Lighter green on hover */
     }}


    #create-match-table {{
        display: block;
        width: 100%;
        padding: 15px;
        margin-top: 25px;
        background-color: #e53935; /* Red */
        color: white;
        border: none;
        border-radius: 5px;
        cursor: pointer;
        font-size: 1.2rem;
        font-weight: 600;
        transition: background-color 0.3s ease, transform 0.1s ease;
    }}

    #create-match-table:disabled {{
        background-color: #bdbdbd; /* Grayed out */
        cursor: not-allowed;
    }}

    #create-match-table:not(:disabled):hover {{
        background-color: #d32f2f; /* Darker red */
        transform: translateY(-2px);
    }}
     #create-match-table:not(:disabled):active {{
         transform: translateY(0);
     }}


    #registration-feedback {{
        margin-top: 15px;
        font-weight: 600;
        min-height: 1.2em;
    }}
     #registration-feedback[style*="color: green"] {{
         color: #2e7d32 !important; /* Dark green */
     }}
      #registration-feedback[style*="color: red"] {{
         color: #d32f2f !important; /* Dark red */
      }}


    /* Bracket Visualization Styling - Refined */
    #bracket-section {{
        margin: 40px auto;
        padding: 30px;
        background-color: #fff;
        border-radius: 10px;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.15);
    }}

    #current-round-info {{
         font-weight: bold;
         color: #d32f2f; /* Dark red */
         text-align: center;
         margin-bottom: 25px;
         font-size: 1.3rem;
     }}


    .bracket-container {{
        display: flex;
        overflow-x: auto;
        padding: 20px;
        background-color: #f9fbe7; /* Very light yellowish-green background */
        border-radius: 8px;
        box-shadow: inset 0 1px 3px rgba(0,0,0,0.1); /* Inner shadow */
        min-width: fit-content;
        border: 1px solid #c8e6c9;
        gap: 80px; /* Use gap for spacing between rounds */
    }}
    .tournament-round {{
        display: flex;
        flex-direction: column;
        align-items: center;
        position: relative;
        flex-shrink: 0;
    }}
    .round-label {{
        font-weight: bold;
        margin-bottom: 20px;
        color: #c62828; /* Dark red */
        text-align: center;
        width: 100%;
        font-size: 1.1rem;
    }}
    .match {{
        display: flex;
        flex-direction: column;
        margin-bottom: 40px;
        position: relative;
    }}
    .participant {{
        border: 1px solid #a5d6a7; /* Light green border */
        padding: 8px;
        margin: 2px 0;
        background-color: #fff; /* White background */
        width: 140px; /* Slightly wider participant box */
        text-align: center;
        font-size: 13px;
        cursor: pointer;
        transition: background-color 0.2s ease, border-color 0.2s ease;
        z-index: 2;
        box-sizing: border-box;
        font-weight: 500;
        color: #333;
    }}
    .participant:hover {{
        background-color: #dcedc8; /* Lighter green on hover */
        border-color: #4caf50; /* Green border on hover */
    }}
     .bye {{
        font-style: italic;
        color: #666;
        background-color: #f0f0f0;
         cursor: default;
         border-color: #ccc;
     }}
     .winner-placeholder {{
        font-style: italic;
        color: #c62828; /* Dark red for placeholders */
        border-style: dashed;
        background-color: #fce4ec; /* Very light red background */
     }}

     .tournament-winner {{
         font-weight: bold;
         color: #2e7d32; /* Dark green color */
         border-color: #2e7d32;
         border-width: 2px;
         background-color: #e8f5e9; /* Light green background */
     }}


     .round-label {{
         font-weight: bold;
         margin-bottom: 10px;
         position: absolute;
         top: 10px; /* Position below the top padding */
         text-align: center;
         z-index: 2;
         color: #555;
     }}

     /* Add styling for the current round and upcoming matches indication */
     .current-round-indicator {{
         font-weight: bold;
         color: #c62828; /* Dark red */
         text-align: center;
         margin-bottom: 20px;
     }}

     /* Responsive Adjustments (Basic) */
     @media (max-width: 768px) {{
         #registration-form {{
             padding: 15px;
         }}
         #participant-name {{
             width: calc(100% - 100px);
         }}
         #add-participant {{
             padding: 8px 12px;
             font-size: 0.9rem;
         }}
         #create-match-table {{
             padding: 10px;
             font-size: 1rem;
         }}
         .bracket-participant {{
             font-size: 10px;
             padding: 3px;
         }}
          /* Adjust horizontal spacing for smaller screens */
         #bracket-container {{
             min-width: unset; /* Allow container to shrink */
         }}
          .bracket-participant {{
              width: unset; /* Allow participant width to adjust */
          }}
     }}


    </style>
    <div id="registration-form">
        <h2>Tournament Sign-Up!</h2>
        <label for="num-participants">Number of Participants:</label>
        <input type="number" id="num-participants" value="{int(num_participants)}" min="2">
        <input type="text" id="participant-name" placeholder="Enter Your Name Here">
        <button id="add-participant">Add Participant</button>
        <h3>Registered Participants: <span id="participant-count">{len(st.session_state.registered_participants)}/{int(num_participants)}</span></h3>
        <ul id="participant-list">
        {"".join([f"<li>{p}</li>" for p in st.session_state.registered_participants])}
        </ul>
        <button id="create-match-table" {"" if len(st.session_state.registered_participants) == num_participants else "disabled"}>Create Match Table</button>
         <div id="registration-feedback" style="color: red; margin-top: 10px;"></div>
    </div>

    <div id="bracket-section" style="display: {'block' if 'tournament_bracket' in st.session_state else 'none'};">
         <div id="current-round-info" class="current-round-indicator"></div>
         <div id="bracket-container" class="bracket-container">
             <!-- The tournament bracket will be rendered here by JavaScript -->
         </div>
    </div>


    <script>
        const participantNameInput = document.getElementById('participant-name');
        const addParticipantButton = document.getElementById('add-participant');
        const participantList = document.getElementById('participant-list');
        const createMatchTableButton = document.getElementById('create-match-table');
        const participantCountSpan = document.getElementById('participant-count');
        const registrationFeedbackDiv = document.getElementById('registration-feedback');
        const bracketSection = document.getElementById('bracket-section');
        const bracketContainer = document.getElementById('bracket-container');
        const currentRoundInfoDiv = document.getElementById('current-round-info');
        const numParticipantsInput = document.getElementById('num-participants');


        let registeredParticipants = {json.dumps(st.session_state.registered_participants)}; // Initialize with session state
        let maxParticipants = parseInt(numParticipantsInput.value); // Get initial value

        // Function to update the participant count display
        function updateParticipantCount() {{
            participantCountSpan.textContent = `${{registeredParticipants.length}}/${{maxParticipants}}`;
            createMatchTableButton.disabled = registeredParticipants.length !== maxParticipants; // Update button state
        }}

        // Update maxParticipants when the input changes
        numParticipantsInput.addEventListener('change', () => {{
            const newMax = parseInt(numParticipantsInput.value);
            if (newMax >= 2) {{
                maxParticipants = newMax;
                updateParticipantCount();
                // Re-evaluate if the create match table button should be enabled
                 registrationFeedbackDiv.textContent = ''; // Clear feedback on number change
                 registrationFeedbackDiv.style.color = 'red';
            }} else {{
                 numParticipantsInput.value = maxParticipants; // Revert to previous valid value
                 registrationFeedbackDiv.textContent = 'Number of participants must be at least 2.';
                 registrationFeedbackDiv.style.color = 'red';
            }}
        }});


        addParticipantButton.addEventListener('click', () => {{
            const name = participantNameInput.value.trim();
            registrationFeedbackDiv.textContent = ''; // Clear previous feedback

            if (!name) {{
                registrationFeedbackDiv.textContent = 'Please enter a participant name.';
                return;
            }}

            if (registeredParticipants.length >= maxParticipants) {{
                registrationFeedbackDiv.textContent = `Maximum of ${{maxParticipants}} participants reached.`;
                return;
            }}

            if (registeredParticipants.includes(name)) {{
                 registrationFeedbackDiv.textContent = `Participant "${{name}}" is already registered.`;
                 return;
            }}


            registeredParticipants.push(name);
            const listItem = document.createElement('li');
            listItem.textContent = name;
            participantList.appendChild(listItem);
            participantNameInput.value = '';

            updateParticipantCount();

             // No need to explicitly disable/enable here, updateParticipantCount handles it
        }});

        // Allow adding participant by pressing Enter key
        participantNameInput.addEventListener('keypress', (event) => {{
            if (event.key === 'Enter') {{
                event.preventDefault(); // Prevent form submission
                addParticipantButton.click();
            }}
        }});


        createMatchTableButton.addEventListener('click', () => {{
            if (registeredParticipants.length === maxParticipants) {{
                // Send participant data back to Streamlit to generate bracket
                // Use Streamlit.setComponentValue to send data to Python backend
                const dataToSend = {{
                    action: 'create_bracket',
                    participants: registeredParticipants,
                    num_participants: maxParticipants
                }};
                // In a real Streamlit custom component, you'd use Streamlit.setComponentValue
                // For this basic HTML embed, we'll simulate by setting query params
                 const params = new URLSearchParams();
                 params.append('action', 'create_bracket');
                 params.append('participants', JSON.stringify(registeredParticipants));
                 params.append('num_participants', maxParticipants);

                 window.location.search = params.toString(); // Redirect with query params


            }} else {{
                registrationFeedbackDiv.textContent = `Please register ${{maxParticipants}} participants to create the bracket.`;
                registrationFeedbackDiv.style.color = 'red';
            }}
        }});


        // --- Bracket Visualization and Interaction Logic (from previous step, with refinements) ---

         let tournamentRounds = {bracket_json}; // Initialize with bracket data from Streamlit


        // Function to generate the tournament bracket (moved to Python)
        // Function to shuffle array (moved to Python)


        function renderBracket(roundsData) {{
            const container = document.getElementById('bracket-container');
            if (!container) return; // Exit if container not found

            container.innerHTML = ''; // Clear previous content

            tournamentRounds = roundsData; // Update the global tournament data

            const roundNames = Object.keys(tournamentRounds);
            const numRounds = roundNames.length;

            // Calculate dimensions - these might need adjustment based on participant names and number of rounds
            const participantHeight = 30; // Height allocated for each participant line
            const verticalSpacing = 20; // Vertical space between match pairings
            const horizontalSpacing = 150; // Increased horizontal space for better separation

             // Determine total height needed based on the largest round (usually the first or second)
             let maxPairingsInRound = 0;
             for (const roundName in tournamentRounds) {{
                  maxPairingsInRound = Math.max(maxPairingsInRound, tournamentRounds[roundName].length);
             }}
             const totalHeight = maxPairingsInRound * (participantHeight * 2 + verticalSpacing) + verticalSpacing; // Add some buffer


            container.style.position = 'relative';
            // Adjust width based on number of rounds and spacing
            container.style.width = `${{numRounds * horizontalSpacing + 200}}px`;
            container.style.height = `${{totalHeight}}px`;


            let currentX = 50; // Starting x position for the first round

            // Store participant/match element positions to draw connecting lines
            const elementPositions = {{}};

            roundNames.forEach((roundName, roundIndex) => {{
                const pairings = tournamentRounds[roundName];
                const numPairings = pairings.length;

                // Calculate the starting y position to center the round vertically
                const roundHeight = numPairings * (participantHeight * 2 + verticalSpacing);
                let currentY = (totalHeight - roundHeight) / 2;

                // Add round label - moved inside the loop for positioning
                 const roundLabelDiv = document.createElement('div');
                 roundLabelDiv.classList.add('round-label');
                 roundLabelDiv.textContent = roundName;
                 roundLabelDiv.style.position = 'absolute';
                 roundLabelDiv.style.left = `${{currentX + horizontalSpacing / 4}}px`; // Position above the round
                 roundLabelDiv.style.top = `${{-20}}px`; // Adjust vertical position as needed
                 roundLabelDiv.style.textAlign = 'center';
                 roundLabelDiv.style.width = `${{horizontalSpacing / 2}}px`;
                 container.appendChild(roundLabelDiv);


                pairings.forEach((pairing, pairingIndex) => {{
                    const participant1 = pairing[0];
                    const participant2 = pairing[1];

                     // Function to create and position a participant element
                    const createParticipantElement = (name, x, y, isClickable = false, round, matchIndex, participantIndex) => {{
                        const participantDiv = document.createElement('div');
                        participantDiv.classList.add('bracket-participant');
                        participantDiv.textContent = name;
                        participantDiv.style.position = 'absolute';
                        participantDiv.style.left = `${{x}}px`;
                        participantDiv.style.top = `${{y}}px`;
                        participantDiv.style.height = `${{participantHeight}}px`;
                        participantDiv.style.width = `${{horizontalSpacing / 2 - 10}}px`; // Adjust width for padding/border
                        participantDiv.style.cursor = isClickable ? 'pointer' : 'default';

                        if (isClickable) {{
                            participantDiv.dataset.round = round;
                            participantDiv.dataset.matchIndex = matchIndex;
                            participantDiv.dataset.participantIndex = participantIndex;
                            participantDiv.addEventListener('click', handleWinnerClick);
                        }}

                        container.appendChild(participantDiv);
                        return participantDiv;
                    }};

                    // Determine if the pairing is a bye match or a decided match (winner placeholder replaced)
                    const isMatchDecided = !participant1.startsWith('Winner of') && !participant2.startsWith('Winner of') && participant1 !== 'Bye' && participant2 !== 'Bye' && participant2 !== 'Champion';

                    if (roundIndex === 0) {{
                        // Round 1 participants
                         if (participant1 !== 'Bye') {{
                            const participant1Div = createParticipantElement(participant1, currentX, currentY, !isMatchDecided && participant2 !== 'Bye', roundName, pairingIndex, 0);
                             elementPositions[participant1] = {{ x: currentX + horizontalSpacing / 2, y: currentY + participantHeight / 2 }};
                         }} else {{
                              createParticipantElement(participant1, currentX, currentY); // Not clickable
                              elementPositions[participant1] = {{ x: currentX + horizontalSpacing / 2, y: currentY + participantHeight / 2 }};
                         }}

                         if (participant2 !== 'Bye' && participant2 !== 'Champion') {{
                            const participant2Div = createParticipantElement(participant2, currentX, currentY + participantHeight, !isMatchDecided && participant1 !== 'Bye', roundName, pairingIndex, 1);
                             elementPositions[participant2] = {{ x: currentX + horizontalSpacing / 2, y: currentY + participantHeight + participantHeight / 2 }};
                         }} else {{
                             createParticipantElement(participant2, currentX, currentY + participantHeight); // Not clickable
                             elementPositions[participant2] = {{ x: currentX + horizontalSpacing / 2, y: currentY + participantHeight + participantHeight / 2 }};
                         }}

                         // Draw lines for Round 1
                         drawLine(container, currentX + (horizontalSpacing / 2 - 10), currentY + participantHeight / 2, currentX + horizontalSpacing / 2, currentY + participantHeight / 2);
                         drawLine(container, currentX + (horizontalSpacing / 2 - 10), currentY + participantHeight + participantHeight / 2, currentX + horizontalSpacing / 2, currentY + participantHeight + participantHeight / 2);
                         drawLine(container, currentX + horizontalSpacing / 2, currentY + participantHeight / 2, currentX + horizontalSpacing / 2, currentY + participantHeight + participantHeight / 2);

                         const winnerKey = `Winner of Round 1 Match ${{pairingIndex + 1}}`;
                         const winnerY = currentY + participantHeight;
                         elementPositions[winnerKey] = {{ x: currentX + horizontalSpacing, y: winnerY }};

                          // Add a placeholder for the winner
                         const winnerPlaceholderDiv = document.createElement('div');
                         winnerPlaceholderDiv.classList.add('bracket-participant', 'winner-placeholder');
                         winnerPlaceholderDiv.textContent = winnerKey;
                         winnerPlaceholderDiv.style.position = 'absolute';
                         winnerPlaceholderDiv.style.left = `${{currentX + horizontalSpacing / 2 + 10}}px`; // Offset from match line
                         winnerPlaceholderDiv.style.top = `${{winnerY - participantHeight/2}}px`;
                         winnerPlaceholderDiv.style.height = `${{participantHeight}}px`;
                         winnerPlaceholderDiv.style.width = `${{horizontalSpacing / 2 - 10}}px`;
                         container.appendChild(winnerPlaceholderDiv);


                    }} else {{
                        // For subsequent rounds, get positions from the previous round
                        const pos1 = elementPositions[participant1];
                        const pos2 = elementPositions[participant2];

                        if (pos1 && pos2) {{
                            // Draw horizontal lines from previous round positions to the current round's connecting point
                            drawLine(container, pos1.x, pos1.y, currentX, pos1.y);
                            drawLine(container, pos2.x, pos2.y, currentX, pos2.y);


                            // Draw vertical lines to the current match pairing point
                             const matchPairingY1 = currentY + participantHeight / 2;
                             const matchPairingY2 = currentY + participantHeight + participantHeight / 2;

                            drawLine(container, currentX, pos1.y, currentX, matchPairingY1);
                            drawLine(container, currentX, pos2.y, currentX, matchPairingY2);


                            // Draw the vertical line for the match
                            const matchLineX = currentX + horizontalSpacing / 2;
                             drawLine(container, matchLineX, matchPairingY1, matchLineX, matchPairingY2);


                            // Position for the winner of this match
                             const winnerKey = `Winner of ${{roundName}} Match ${{pairingIndex + 1}}`;
                             const winnerY = currentY + participantHeight; // Midpoint of the vertical line
                             elementPositions[winnerKey] = {{ x: currentX + horizontalSpacing, y: winnerY }};

                             // Add the participant elements for the current round's match
                             // Make clickable only if not a placeholder ('Winner of...') and the match is not decided
                             const isParticipant1Placeholder = participant1.startsWith('Winner of');
                             const isParticipant2Placeholder = participant2.startsWith('Winner of');
                             const isMatchFullyDecidedInNextRound = roundIndex < numRounds - 1 &&
                                                                    tournamentRounds[roundNames[roundIndex + 1]].some(nextPairing =>
                                                                        nextPairing.includes(participant1) || nextPairing.includes(participant2) // Check if either participant has already advanced
                                                                    );


                             if (participant1 !== 'Bye' && participant1 !== 'Champion' && !isParticipant1Placeholder && !isMatchFullyDecidedInNextRound) {{
                                 createParticipantElement(participant1, currentX + horizontalSpacing / 2 + 10, currentY, true, roundName, pairingIndex, 0);
                             }} else {{
                                 createParticipantElement(participant1, currentX + horizontalSpacing / 2 + 10, currentY, false, roundName, pairingIndex, 0);
                             }}

                             if (participant2 !== 'Bye' && participant2 !== 'Champion' && !isParticipant2Placeholder && !isMatchFullyDecidedInNextRound) {{
                                 createParticipantElement(participant2, currentX + horizontalSpacing / 2 + 10, currentY + participantHeight, true, roundName, pairingIndex, 1);
                             }} else {{
                                 createParticipantElement(participant2, currentX + horizontalSpacing / 2 + 10, currentY + participantHeight, false, roundName, pairingIndex, 1);
                             }}


                             // Add a placeholder for the winner in the next round
                             if (roundIndex < numRounds - 1) {{ // Don't add winner placeholder for the final round winner
                                const nextRoundName = roundNames[roundIndex + 1];
                                // Find the pairing in the next round that this winner belongs to
                                let nextRoundPairingIndex = -1;
                                let participantInNextRoundIndex = -1; // 0 or 1

                                 for (let i = 0; i < tournamentRounds[nextRoundName].length; i++) {{
                                     const [nextP1, nextP2] = tournamentRounds[nextRoundName][i];
                                     if (nextP1 === winnerKey) {{
                                         nextRoundPairingIndex = i;
                                         participantInNextRoundIndex = 0;
                                         break;
                                     }}
                                      if (nextP2 === winnerKey) {{
                                         nextRoundPairingIndex = i;
                                         participantInNextRoundIndex = 1;
                                         break;
                                      }}
                                 }}

                                 if (nextRoundPairingIndex !== -1) {{
                                    const winnerPlaceholderDiv = document.createElement('div');
                                    winnerPlaceholderDiv.classList.add('bracket-participant', 'winner-placeholder');
                                    winnerPlaceholderDiv.textContent = winnerKey; // Placeholder text
                                    winnerPlaceholderDiv.style.position = 'absolute';
                                    // Position the placeholder relative to the next round's start x and the calculated winner y
                                    const nextRoundStartX = 50 + (roundIndex + 1) * horizontalSpacing;
                                     let nextRoundCurrentY = (totalHeight - tournamentRounds[nextRoundName].length * (participantHeight * 2 + verticalSpacing)) / 2;
                                     let placeholderY = nextRoundCurrentY + nextRoundPairingIndex * (participantHeight * 2 + verticalSpacing) + (participantInNextRoundIndex === 0 ? participantHeight/2 : participantHeight + participantHeight/2);


                                    winnerPlaceholderDiv.style.left = `${{nextRoundStartX + horizontalSpacing / 2 + 10}}px`;
                                    winnerPlaceholderDiv.style.top = `${{placeholderY - participantHeight/2}}px`;

                                    winnerPlaceholderDiv.style.height = `${{participantHeight}}px`;
                                    winnerPlaceholderDiv.style.width = `${{horizontalSpacing / 2 - 10}}px`;
                                    container.appendChild(winnerPlaceholderDiv);
                                 }}
                             }}


                        }} else {{
                            // Handle cases like Byes in later rounds - position directly at the start of their line in the current round
                             if (participant1 !== 'Bye' && participant2 === 'Bye') {{
                                 const participant1Div = createParticipantElement(participant1, currentX + horizontalSpacing / 2 + 10, currentY + participantHeight / 2, true, roundName, pairingIndex, 0);
                                 elementPositions[participant1] = {{ x: currentX + horizontalSpacing / 2, y: currentY + participantHeight / 2 }};

                                 // Draw a line extending from the bye participant
                                  drawLine(container, currentX + (horizontalSpacing / 2 - 10), currentY + participantHeight / 2, currentX + horizontalSpacing / 2, currentY + participantHeight / 2);


                                // Position for the winner of this match (the participant with the bye)
                                 const winnerKey = `Winner of ${{roundName}} Match ${{pairingIndex + 1}}`;
                                 const winnerY = currentY + participantHeight/2;
                                  elementPositions[winnerKey] = {{ x: currentX + horizontalSpacing, y: winnerY }};

                                // Add the participant name as the winner placeholder for a bye
                                 if (roundIndex < numRounds - 1) {{
                                     const nextRoundName = roundNames[roundIndex + 1];
                                     let nextRoundPairingIndex = -1;
                                     let participantInNextRoundIndex = -1;

                                      for (let i = 0; i < tournamentRounds[nextRoundName].length; i++) {{
                                          const [nextP1, nextP2] = tournamentRounds[nextRoundName][i];
                                          if (nextP1 === winnerKey) {{
                                              nextRoundPairingIndex = i;
                                              participantInNextRoundIndex = 0;
                                              break;
                                          }}
                                           if (nextP2 === winnerKey) {{
                                              nextRoundPairingIndex = i;
                                              participantInNextRoundIndex = 1;
                                              break;
                                           }}
                                      }}

                                      if (nextRoundPairingIndex !== -1) {{
                                         const winnerPlaceholderDiv = document.createElement('div');
                                         winnerPlaceholderDiv.classList.add('bracket-participant', 'winner-placeholder');
                                         winnerPlaceholderDiv.textContent = participant1;
                                         winnerPlaceholderDiv.style.position = 'absolute';

                                         const nextRoundStartX = 50 + (roundIndex + 1) * horizontalSpacing;
                                          let nextRoundCurrentY = (totalHeight - tournamentRounds[nextRoundName].length * (participantHeight * 2 + verticalSpacing)) / 2;
                                          let placeholderY = nextRoundCurrentY + nextRoundPairingIndex * (participantHeight * 2 + verticalSpacing) + (participantInNextRoundIndex === 0 ? participantHeight/2 : participantHeight + participantHeight/2);


                                         winnerPlaceholderDiv.style.left = `${{nextRoundStartX + horizontalSpacing / 2 + 10}}px`;
                                         winnerPlaceholderDiv.style.top = `${{placeholderY - participantHeight/2}}px`;

                                         winnerPlaceholderDiv.style.height = `${{participantHeight}}px`;
                                         winnerPlaceholderDiv.style.width = `${{horizontalSpacing / 2 - 10}}px`;
                                         container.appendChild(winnerPlaceholderDiv);
                                      }}
                                 }} else {{
                                     // This is the final round and participant1 has a bye (shouldn't happen in a standard bracket)
                                     // Handle as the tournament winner
                                      const winnerDiv = document.createElement('div');
                                      winnerDiv.classList.add('bracket-participant', 'tournament-winner');
                                      winnerDiv.textContent = `${{participant1}} (Champion)`;
                                      winnerDiv.style.position = 'absolute';
                                      winnerDiv.style.left = `${{currentX + horizontalSpacing / 2 + 10}}px`;
                                      winnerDiv.style.top = `${{currentY + participantHeight / 2}}px`;
                                      winnerDiv.style.height = `${{participantHeight}}px`;
                                      winnerDiv.style.width = `${{horizontalSpacing / 2 - 10}}px`;
                                      container.appendChild(winnerDiv);
                                 }}


                             }}
                             // Handle cases where participant1 is 'Bye' and participant2 is a real player
                             else if (participant1 === 'Bye' && participant2 !== 'Bye' && participant2 !== 'Champion') {{
                                 const participant2Div = createParticipantElement(participant2, currentX + horizontalSpacing / 2 + 10, currentY + participantHeight + participantHeight / 2, true, roundName, pairingIndex, 1);
                                 elementPositions[participant2] = {{ x: currentX + horizontalSpacing / 2, y: currentY + participantHeight + participantHeight / 2 }};

                                 // Draw a line extending from the bye participant
                                  drawLine(container, currentX + (horizontalSpacing / 2 - 10), currentY + participantHeight + participantHeight / 2, currentX + horizontalSpacing / 2, currentY + participantHeight + participantHeight / 2);


                                // Position for the winner of this match (the participant with the bye)
                                 const winnerKey = `Winner of ${{roundName}} Match ${{pairingIndex + 1}}`;
                                 const winnerY = currentY + participantHeight/2; // Should be aligned with participant2's line end
                                  elementPositions[winnerKey] = {{ x: currentX + horizontalSpacing, y: winnerY }};

                                // Add the participant name as the winner placeholder for a bye
                                 if (roundIndex < numRounds - 1) {{
                                     const nextRoundName = roundNames[roundIndex + 1];
                                     let nextRoundPairingIndex = -1;
                                     let participantInNextRoundIndex = -1;

                                      for (let i = 0; i < tournamentRounds[nextRoundName].length; i++) {{
                                          const [nextP1, nextP2] = tournamentRounds[nextRoundName][i];
                                          if (nextP1 === winnerKey) {{
                                              nextRoundPairingIndex = i;
                                              participantInNextRoundIndex = 0;
                                              break;
                                          }}
                                           if (nextP2 === winnerKey) {{
                                              nextRoundPairingIndex = i;
                                              participantInNextRoundIndex = 1;
                                              break;
                                           }}
                                      }}

                                      if (nextRoundPairingIndex !== -1) {{
                                         const winnerPlaceholderDiv = document.createElement('div');
                                         winnerPlaceholderDiv.classList.add('bracket-participant', 'winner-placeholder');
                                         winnerPlaceholderDiv.textContent = participant2;
                                         winnerPlaceholderDiv.style.position = 'absolute';

                                         const nextRoundStartX = 50 + (roundIndex + 1) * horizontalSpacing;
                                          let nextRoundCurrentY = (totalHeight - tournamentRounds[nextRoundName].length * (participantHeight * 2 + verticalSpacing)) / 2;
                                          let placeholderY = nextRoundCurrentY + nextRoundPairingIndex * (participantHeight * 2 + verticalSpacing) + (participantInNextRoundIndex === 0 ? participantHeight/2 : participantHeight + participantHeight/2);


                                         winnerPlaceholderDiv.style.left = `${{nextRoundStartX + horizontalSpacing / 2 + 10}}px`;
                                         winnerPlaceholderDiv.style.top = `${{placeholderY - participantHeight/2}}px`;

                                         winnerPlaceholderDiv.style.height = `${{participantHeight}}px`;
                                         winnerPlaceholderDiv.style.width = `${{horizontalSpacing / 2 - 10}}px`;
                                         container.appendChild(winnerPlaceholderDiv);
                                      }}
                                 }} else {{
                                     // This is the final round and participant2 has a bye (shouldn't happen in a standard bracket)
                                      const winnerDiv = document.createElement('div');
                                      winnerDiv.classList.add('bracket-participant', 'tournament-winner');
                                      winnerDiv.textContent = `${{participant2}} (Champion)`;
                                      winnerDiv.style.position = 'absolute';
                                      winnerDiv.style.left = `${{currentX + horizontalSpacing / 2 + 10}}px`;
                                      winnerDiv.style.top = `${{currentY + participantHeight + participantHeight / 2}}px`;
                                      winnerDiv.style.height = `${{participantHeight}}px`;
                                      winnerDiv.style.width = `${{horizontalSpacing / 2 - 10}}px`;
                                      container.appendChild(winnerDiv);
                                 }}
                             }} else if (participant1 !== 'Bye' && participant2 !== 'Bye' && participant2 !== 'Champion') {{
                                  // This case is handled by the main 'if (pos1 && pos2)' block
                             }}

                        }}

                    currentY += participantHeight * 2 + verticalSpacing; // Move to the next pairing position
                }});

                currentX += horizontalSpacing; // Move to the next round position
            }});

            // Handle the final winner display if there is one
            const lastRoundName = roundNames[numRounds - 1];
            const lastRoundPairings = tournamentRounds[lastRoundName];
            if (lastRoundPairings.length === 1 && lastRoundPairings[0][1] === 'Champion') {{
                const winnerName = lastRoundPairings[0][0];
                const winnerElement = document.createElement('div');
                winnerElement.classList.add('bracket-participant', 'tournament-winner');
                winnerElement.textContent = `${{winnerName}} (Champion)`;
                winnerElement.style.position = 'absolute';
                // Position near the final round
                const finalRoundX = 50 + (numRounds - 1) * horizontalSpacing;
                let finalRoundY = (totalHeight - lastRoundPairings.length * (participantHeight * 2 + verticalSpacing)) / 2;
                 const winnerY = finalRoundY + participantHeight/2;


                winnerElement.style.left = `${{finalRoundX + horizontalSpacing / 2 + 10}}px`;
                winnerElement.style.top = `${{winnerY - participantHeight/2}}px`;
                winnerElement.style.height = `${{participantHeight}}px`;
                winnerElement.style.width = `${{horizontalSpacing / 2 - 10}}px`;
                container.appendChild(winnerElement);
            }}


        }}

         // Helper function to draw lines (can be done with SVG or div borders)
         function drawLine(container, x1, y1, x2, y2) {{
            const line = document.createElement('div');
            line.style.position = 'absolute';
            line.style.backgroundColor = 'black';
            line.style.zIndex = 1; // Ensure lines are behind text

            // Calculate distance and angle
            const distance = Math.sqrt((x2 - x1)**2 + (y2 - y1)**2);
            const angle = Math.atan2(y2 - y1, x2 - x1) * 180 / Math.PI;

            // Set position and size
            line.style.width = `${{distance}}px`;
            line.style.height = `1px`; // Line thickness
            line.style.left = `${{x1}}px`;
            line.style.top = `${{y1}}px`;
            line.style.transformOrigin = '0 0'; // Rotate from the starting point
            line.style.transform = `rotate(${{angle}}deg)`;

            container.appendChild(line);
         }}

         // Function to handle winner clicks
         function handleWinnerClick(event) {{
            const clickedElement = event.target;
            const winnerName = clickedElement.textContent;
            const roundName = clickedElement.dataset.round;
            const matchIndex = parseInt(clickedElement.dataset.matchIndex);
            const participantIndex = parseInt(clickedElement.dataset.participantIndex);

            console.log(`Clicked on: ${{winnerName}}, Round: ${{roundName}}, Match Index: ${{matchIndex}}, Participant Index: ${{participantIndex}}`);

            // Send winner info back to Streamlit to update bracket state
            const winnerData = {{
                winner_name: winnerName,
                round_name: roundName,
                match_index: matchIndex,
                participant_index: participantIndex
            }};
             const params = new URLSearchParams();
             params.append('winner_info', JSON.stringify(winnerData));
             window.location.search = params.toString(); // Redirect with query params

         }}

         // Function to update the current round information display (called from Streamlit)
         function updateCurrentRoundInfo(currentRoundName) {{
             const currentRoundInfoDiv = document.getElementById('current-round-info');
             if (currentRoundInfoDiv) {{
                 currentRoundInfoDiv.textContent = `Current Round: ${{currentRoundName}}`;
             }}
         }}


        // Initial setup - render bracket if data exists
        if (Object.keys(tournamentRounds).length > 0) {{
            renderBracket(tournamentRounds);
            // Update current round info display after rendering
            const roundNames = Object.keys(tournamentRounds);
            let currentRoundDisplay = "Tournament in Progress";
            const finalRoundName = roundNames[roundNames.length - 1];
            const finalPairing = tournamentRounds[finalRoundName][0];

            if (finalPairing && finalPairing[1] === 'Champion' && !finalPairing[0].startsWith('Winner of')) {{
                 currentRoundDisplay = `Tournament Champion: ${{finalPairing[0]}}`;
            }} else {{
                 const firstUnresolvedRoundIndex = roundNames.findIndex(round =>
                     tournamentRounds[round].some(pairing =>
                         (pairing[0].startsWith('Winner of') || pairing[1].startsWith('Winner of'))
                     )
                 );
                 if (firstUnresolvedRoundIndex !== -1) {{
                     currentRoundDisplay = `Current Round: ${{roundNames[firstUnresolvedRoundIndex]}}`;
                 }} else if (Object.keys(tournamentRounds).length > 0) {{
                      // If no unresolved matches but rounds exist, check if the last match is done
                       if (finalRoundName in tournamentRounds && tournamentRounds[finalRoundName].length === 1) {{
                            const lastMatch = tournamentRounds[finalRoundName][0];
                            if (!lastMatch[0].startsWith('Winner of') && !lastMatch[1].startsWith('Winner of') && lastMatch[1] !== 'Champion') {{
                                 currentRoundDisplay = `Tournament Complete: ${{lastMatch[0]}} is the likely winner.`;
                            }}
                       }} else {{
                           currentRoundDisplay = "Tournament Setup Complete";
                       }}

                 }} else {{
                     currentRoundDisplay = "Tournament Setup Complete";
                 }}
            }}
             updateCurrentRoundInfo(currentRoundDisplay);
        }} else {{
            // Hide bracket section if no bracket data
            bracketSection.style.display = 'none';
             document.getElementById('registration-form').style.display = 'block';
        }}

    </script>
"""
    return html_content


# Display the bracket using st.html
if 'tournament_bracket' in st.session_state and st.session_state.tournament_bracket:
    st.subheader("Bracket Visualization:")
    st.html(render_bracket_html_improved(st.session_state.tournament_bracket), height=800) # Increased height for better visibility

# The logic for handling query parameters and updating session state
# is now outside the HTML rendering function and directly in the Streamlit app script.

# This part of the script will run on every rerun
# Handle creation action triggered by the button in HTML
# The HTML button sets query parameters which trigger a rerun, handled above

# Handle winner click action triggered by the click in HTML
# The HTML participant click sets query parameters which trigger a rerun, handled above
