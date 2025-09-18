import streamlit as st
import math

def generate_bracket(participants):
    bracket = []
    n = len(participants)
    rounds = int(math.ceil(math.log2(n)))

    # Generate the bracket
    for i in range(rounds):
        round_matches = []
        for j in range(n // 2):
            round_matches.append((participants[j], participants[n - j - 1]))
        if n % 2 != 0:
            round_matches.append((participants[n // 2], None))
        bracket.append(round_matches)
        n = (n + 1) // 2
        participants = [f"Winner of Match {i+1}" for i in range(n * 2 - 1)]

    return bracket



def main():
    st.title("Tournament Bracket Generator")
    num_participants = st.number_input("Number of Participants", min_value=2, value=8)
    participants = [f"Participant {i+1}" for i in range(num_participants)]

    if st.button("Generate Bracket"):
        bracket = generate_bracket(participants)
        visualize_bracket(bracket)

if __name__ == "__main__":
    main()
