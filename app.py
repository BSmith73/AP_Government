import streamlit as st
import time

# Set page config
st.set_page_config(page_title="AP Gov Jeopardy", layout="wide")

# Custom CSS for Big & Centered Text and Headers
st.markdown("""
    <style>
    .category-header {
        font-size: 28px !important;
        font-weight: bold !important;
        text-align: center !important;
        color: #1E3A8A;
        margin-bottom: 20px;
        min-height: 80px;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    .big-font {
        font-size:50px !important;
        text-align: center;
        font-weight: bold;
        padding: 20px;
    }
    .answer-font {
        font-size:45px !important;
        text-align: center;
        color: #2E86C1;
        background-color: #f0f2f6;
        border-radius: 10px;
        padding: 20px;
        margin-top: 20px;
    }
    .centered-text {
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

# Initialize Session State
if 'view' not in st.session_state: st.session_state.view = 'board'
if 'selected_cell' not in st.session_state: st.session_state.selected_cell = None
if 'answered' not in st.session_state: st.session_state.answered = set()
if 'show_answer' not in st.session_state: st.session_state.show_answer = False
for team in ['a', 'b', 'c', 'd']:
    if f'score_{team}' not in st.session_state: st.session_state[f'score_{team}'] = 0

# Data Structure
data = {
    "Bill of Rights": {
        100: {"q": "Which amendment protects against unlawful searches and seizures?", "a": "4th Amendment."},
        200: {"q": "Name at least one protection from the 5th Amendment.", "a": "Protection against self-incrimination, Right to Due Process, Double Jeopardy protection, or Grand Jury indictment."},
        300: {"q": "Name 4 protections from the 1st amendment. (Double Points if you list all 6).", "a": "Speech, Press, Establishment Clause, Free Exercise Clause, Assembly, and Petition."},
        400: {"q": "Which amendment protects against cruel and unusual punishments?", "a": "8th Amendment."},
        500: {"q": "Which amendment says that we have other rights that are not listed in the constitution?", "a": "9th Amendment."}
    },
    "Clauses: SCOTUS Cases": {
        100: {"q": "What is the relevant clause from McDonald v Chicago? (Double if you can also describe the term and clause for applying the BoR to the states.)", "a": "2nd Amendment. Due Process Clause of the 14th Amendment // Selective Incorporation"},
        200: {"q": "Which clause is relevant to Tinker v Des Moines?", "a": "Freedom of Speech/ 1st Amendment"},
        300: {"q": "What is the relevant clause from Wisconsin v Yoder?", "a": "Free Exercise Clause of the 1st Amendment."},
        400: {"q": "Which case centers around the 6th amendment?", "a": "Gideon v Wainwright"},
        500: {"q": "What three cases are about the Equal Protection Clause?", "a": "Brown v. Board of Education, Shaw v. Reno, Baker v. Carr"}
    },
    "Details: SCOTUS Cases": {
        100: {"q": "Which case involved the Pentagon Papers?", "a": "New York Times Co. v. United States."},
        200: {"q": "Which case’s outcome led to the elimination of several restrictions on guns?", "a": "McDonald v. Chicago"},
        300: {"q": "What case led to the development of the “Public Defender” job?", "a": "Gideon v. Wainwright"},
        400: {"q": "Which case established the clear and present danger test?", "a": "Schenck v. United States."},
        500: {"q": "Name all four cases that involved schools.", "a": "Brown v. Board of Education, Engel v. Vitale, Wisconsin v. Yoder, Tinker v. Des Moines."}
    },
    "Letter from Birmingham Jail": {
        100: {"q": "Why did MLK choose Birmingham Alabama as the place of protest?", "a": "Most segregated city in the country/ history of brutality"},
        200: {"q": "Why does MLK resort to leading protests in Birmingham?", "a": "Failed negotiations/ broken promises to remove segregation signs."},
        300: {"q": "Who is MLK’s letter responding to?", "a": "white clergymen"},
        400: {"q": "What does MLK mean when says “decided to go through a process of self-purification”?", "a": "activists prepared themselves to accept blows without retaliating and to endure the ordeal of jail."},
        500: {"q": "MLK says protests are designed to cause what in a community?", "a": "Tension / Crisis"}
    },
    "Civil Rights": {
        100: {"q": "What is the term for social segregation (not by law)?", "a": "De facto segregation"},
        200: {"q": "Which act sought to eliminate race-based discrimination?", "a": "Civil Rights Act of 1964"},
        300: {"q": "What act (not amendment) led to increased voting rights for Americans?", "a": "Voting Rights Act of 1965."},
        400: {"q": "What part of the Education Amendment Act increased rights for women and girls?", "a": "Title IX"},
        500: {"q": "Which SCOTUS case secured marriage rights for same-sex couples?", "a": "Obergefell v. Hodges"}
    }
}

# --- Game Board View ---
if st.session_state.view == 'board':
    st.markdown("<h1 style='text-align: center;'>⚖️ AP Gov Jeopardy</h1>", unsafe_allow_html=True)
    st.write("")
    
    cols = st.columns(len(data))
    for i, category in enumerate(data.keys()):
        with cols[i]:
            # Big, Bolded, Centered Header
            st.markdown(f"<div class='category-header'>{category}</div>", unsafe_allow_html=True)
            for points in [100, 200, 300, 400, 500]:
                key = f"{category}_{points}"
                if key in st.session_state.answered:
                    st.button("X", key=key, disabled=True, use_container_width=True)
                else:
                    if st.button(f"${points}", key=key, use_container_width=True):
                        st.session_state.selected_cell = (category, points)
                        st.session_state.answered.add(key)
                        st.session_state.show_answer = False
                        st.session_state.view = 'question'
                        st.rerun()
    
    st.markdown("---")
    st.subheader("Scoreboard")
    sc = st.columns(4)
    for i, team in enumerate(['a', 'b', 'c', 'd']):
        with sc[i]:
            st.write(f"**Team {team.upper()}: {st.session_state[f'score_{team}']}**")
            b1, b2 = st.columns(2)
            if b1.button("+100", key=f"{team}_p"): st.session_state[f'score_{team}'] += 100; st.rerun()
            if b2.button("-100", key=f"{team}_m"): st.session_state[f'score_{team}'] -= 100; st.rerun()

    if st.button("RESET GAME", type="primary", use_container_width=True):
        st.session_state.answered = set()
        for t in ['a','b','c','d']: st.session_state[f'score_{t}'] = 0
        st.rerun()

# --- Question View ---
elif st.session_state.view == 'question':
    cat, pts = st.session_state.selected_cell
    q_data = data[cat][pts]
    
    st.markdown(f"<h3 class='centered-text'>{cat} - ${pts}</h3>", unsafe_allow_html=True)
    st.markdown(f"<div class='big-font'>{q_data['q']}</div>", unsafe_allow_html=True)
    
    if not st.session_state.show_answer:
        if st.button("SHOW ANSWER", type="primary", use_container_width=True):
            st.session_state.show_answer = True
            st.rerun()

    if not st.session_state.show_answer:
        timer_placeholder = st.empty()
        for i in range(10, -1, -1):
            timer_placeholder.warning(f"Reading Time: {i}s")
            time.sleep(1)
        for i in range(60, -1, -1):
            timer_placeholder.error(f"TIME REMAINING: {i}s")
            time.sleep(1)
            if i == 0: timer_placeholder.error("TIME IS UP!")

    if st.session_state.show_answer:
        st.markdown(f"<div class='answer-font'>{q_data['a']}</div>", unsafe_allow_html=True)
        if st.button("BACK TO BOARD", use_container_width=True):
            st.session_state.view = 'board'
            st.rerun()
