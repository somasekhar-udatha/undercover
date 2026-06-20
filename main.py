import streamlit as st
from game_logic import initialize_game, eliminate_player, check_winner

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Undercover",
    page_icon="🕵️",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ── Global styles ─────────────────────────────────────────────────────────────
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=Space+Mono:wght@400;700&display=swap');

    html, body, [data-testid="stAppViewContainer"] {
        background-color: #0B0D12 !important;
        color: #E2E8F0;
        font-family: 'Space Grotesk', sans-serif;
    }

    #MainMenu, footer, header { visibility: hidden; }
    [data-testid="stToolbar"] { display: none; }
    .block-container { padding-top: 2rem; padding-bottom: 4rem; max-width: 620px; }

    h1, h2, h3 { font-family: 'Space Mono', monospace; }

    /* ── Cards ── */
    .glass-card {
        background: #141924;
        border: 1px solid #1E2433;
        border-radius: 16px;
        padding: 1.75rem 1.5rem;
        text-align: center;
        margin: 0.75rem 0;
    }

    .word-reveal {
        background: #141924;
        border: 1px solid #2A1F5E;
        border-radius: 16px;
        padding: 2rem 1.5rem;
        text-align: center;
        margin: 0.75rem 0;
    }

    .word-big {
        font-family: 'Space Mono', monospace;
        font-size: 2.6rem;
        font-weight: 700;
        color: #8B6FFF;
        letter-spacing: 4px;
        text-transform: uppercase;
        margin: 0.5rem 0;
    }

    .label-sm {
        font-size: 0.68rem;
        letter-spacing: 2.5px;
        text-transform: uppercase;
        color: #3D4761;
        font-family: 'Space Mono', monospace;
    }

    .player-waiting {
        font-size: 1.4rem;
        font-weight: 600;
        color: #E2E8F0;
        margin-bottom: 0.25rem;
    }

    .tap-hint {
        color: #4B5B78;
        font-size: 0.88rem;
        margin-top: 0.4rem;
        line-height: 1.6;
    }

    .winner-title {
        font-family: 'Space Mono', monospace;
        font-size: 2rem;
        font-weight: 700;
        letter-spacing: 2px;
        margin-bottom: 0.4rem;
    }

    .civilian-win { color: #34D399; }
    .imposter-win { color: #F87171; }

    .reveal-pair {
        display: flex;
        justify-content: center;
        gap: 1.5rem;
        margin: 1rem 0;
        flex-wrap: wrap;
    }

    .word-chip {
        background: #1A1330;
        border: 1px solid #2A1F5E;
        border-radius: 10px;
        padding: 0.45rem 1rem;
        font-family: 'Space Mono', monospace;
        font-size: 1rem;
        color: #8B6FFF;
        letter-spacing: 1px;
    }

    .divider {
        border: none;
        border-top: 1px solid #1A1F2E;
        margin: 1.25rem 0;
    }

    /* ── Inputs ── */
    div[data-testid="stTextInput"] input {
        background: #161B27 !important;
        border: 1px solid #1E2433 !important;
        border-radius: 10px !important;
        color: #E2E8F0 !important;
        font-family: 'Space Grotesk', sans-serif !important;
    }

    div[data-testid="stTextInput"] input:focus {
        border-color: #6D4AFF !important;
        box-shadow: 0 0 0 3px rgba(109, 74, 255, 0.15) !important;
    }

    div[data-testid="stRadio"] label {
        color: #C4CCDE !important;
        font-size: 1rem !important;
    }

    /* ── Buttons ── */
    .stButton > button {
        width: 100%;
        background: #6D4AFF !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.65rem 1.5rem !important;
        font-family: 'Space Grotesk', sans-serif !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
        letter-spacing: 0.3px !important;
        transition: opacity 0.12s, transform 0.1s !important;
    }

    .stButton > button:hover {
        opacity: 0.85 !important;
        transform: translateY(-1px) !important;
    }

    .stButton > button:active {
        transform: translateY(0) !important;
    }

    [data-testid="baseButton-secondary"] {
        background: transparent !important;
        border: 1px solid #2A1F5E !important;
        color: #8B6FFF !important;
    }

    [data-testid="baseButton-secondary"]:hover {
        background: #1A1330 !important;
    }

    .stAlert { border-radius: 12px !important; }
    </style>
    """,
    unsafe_allow_html=True,
)


# ── Session state defaults ────────────────────────────────────────────────────
def _init_state():
    defaults = {
        "screen": "registration",
        "players": [],
        "alive_players": [],
        "player_data": {},
        "imposter": None,
        "civilian_word": None,
        "imposter_word": None,
        "current_player_index": 0,
        "card_revealed": False,
        "winner": None,
        "eliminated_player": None,
        "vote_choice": None,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


_init_state()


# ── Helpers ───────────────────────────────────────────────────────────────────
def go_to(screen):
    st.session_state.screen = screen


def start_game_from_players(players):
    result = initialize_game(players)
    st.session_state.players = players
    st.session_state.alive_players = result["alive_players"]
    st.session_state.player_data = result["player_data"]
    st.session_state.imposter = result["imposter"]
    st.session_state.civilian_word = result["civilian_word"]
    st.session_state.imposter_word = result["imposter_word"]
    st.session_state.current_player_index = 0
    st.session_state.card_revealed = False
    st.session_state.winner = None
    st.session_state.eliminated_player = None
    go_to("reveal")


# ── SCREEN 1 — Registration ───────────────────────────────────────────────────
def screen_registration():
    st.markdown(
        """
        <div style='text-align:center; padding: 1rem 0 0.5rem;'>
            <span style='font-size:2.8rem;'>🕵️</span>
            <h1 style='font-size:2.6rem; margin:0.2rem 0 0;'>UNDERCOVER</h1>
            <p style='color:#6B7280; letter-spacing:2px; font-size:0.8rem; font-family:"Space Mono",monospace; margin-top:0.3rem;'>
                WHO AMONG US IS THE IMPOSTER?
            </p>
        </div>
        <hr class='divider'>
        """,
        unsafe_allow_html=True,
    )

    if "reg_players" not in st.session_state:
        st.session_state.reg_players = ["", "", ""]

    st.markdown("**Players**")

    to_remove = None
    for i, name in enumerate(st.session_state.reg_players):
        col1, col2 = st.columns([9, 1])
        with col1:
            st.session_state.reg_players[i] = st.text_input(
                f"Player {i + 1}",
                value=name,
                key=f"reg_input_{i}",
                label_visibility="collapsed",
                placeholder=f"Player {i + 1}",
            )
        with col2:
            if len(st.session_state.reg_players) > 3:
                if st.button("✕", key=f"remove_{i}", help="Remove"):
                    to_remove = i

    if to_remove is not None:
        st.session_state.reg_players.pop(to_remove)
        st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    col_a, col_b = st.columns(2)
    with col_a:
        if st.button("＋ Add Player", type="secondary"):
            st.session_state.reg_players.append("")
            st.rerun()

    with col_b:
        valid_names = [n.strip() for n in st.session_state.reg_players if n.strip()]
        if st.button("Start Game →"):
            if len(valid_names) < 3:
                st.error("Add at least 3 players to start.")
            elif len(valid_names) != len(set(valid_names)):
                st.error("Each player must have a unique name.")
            else:
                start_game_from_players(valid_names)
                st.rerun()

    st.markdown(
        "<p style='text-align:center; color:#374151; font-size:0.8rem; margin-top:2rem;'>Recommended: 4–10 players</p>",
        unsafe_allow_html=True,
    )


# ── SCREEN 2 — Reveal Cards ───────────────────────────────────────────────────
def screen_reveal():
    idx = st.session_state.current_player_index
    alive = st.session_state.alive_players
    all_players = st.session_state.players

    # Only alive players reveal (new round mid-game skips eliminated)
    reveal_order = all_players  # full original order for first reveal

    if idx >= len(reveal_order):
        go_to("discussion")
        st.rerun()
        return

    current_player = reveal_order[idx]

    st.markdown(
        f"""
        <div style='text-align:center; padding: 0.5rem 0 1rem;'>
            <p class='label-sm'>PASS THE DEVICE</p>
            <h2 style='margin:0.2rem 0;'>Card {idx + 1} of {len(reveal_order)}</h2>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if not st.session_state.card_revealed:
        st.markdown(
            f"""
            <div class='glass-card'>
                <p class='player-waiting'>{current_player}</p>
                <p class='tap-hint'>Press the button below to reveal your word.<br>
                <span style='color:#4B5563;'>Make sure no one else is looking.</span></p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("👁  Reveal My Word"):
            st.session_state.card_revealed = True
            st.rerun()
    else:
        word = st.session_state.player_data[current_player]["word"]
        st.markdown(
            f"""
            <div class='word-reveal'>
                <p class='label-sm'>YOUR WORD</p>
                <p class='word-big'>{word}</p>
                <p style='color:#4B5563; font-size:0.82rem; margin-top:0.8rem;'>
                    Remember it — don't reveal it.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("🙈  Hide Card"):
            st.session_state.card_revealed = False
            st.session_state.current_player_index += 1
            st.rerun()


# ── SCREEN 3 — Discussion ─────────────────────────────────────────────────────
def screen_discussion():
    st.markdown(
        """
        <div style='text-align:center; padding:1rem 0;'>
            <span style='font-size:2.5rem;'>🗣️</span>
            <h2 style='margin:0.4rem 0;'>Discuss</h2>
            <p style='color:#6B7280;'>Everyone knows their word now.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""
        <div class='glass-card'>
            <p style='font-size:1.05rem; line-height:1.7;'>
                Talk about your word — without saying it directly.<br>
                <span style='color:#6B7280;'>Find clues. Spot the imposter.</span>
            </p>
            <hr class='divider'>
            <p class='label-sm'>ALIVE PLAYERS ({len(st.session_state.alive_players)})</p>
            <p style='font-size:1.1rem; color:#A78BFA; margin-top:0.3rem;'>
                {"  ·  ".join(st.session_state.alive_players)}
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.button("🗳️  Start Voting"):
        go_to("voting")
        st.rerun()


# ── SCREEN 4 — Voting ─────────────────────────────────────────────────────────
def screen_voting():
    st.markdown(
        """
        <div style='text-align:center; padding:1rem 0;'>
            <span style='font-size:2.2rem;'>🗳️</span>
            <h2 style='margin:0.4rem 0;'>Vote</h2>
            <p style='color:#6B7280;'>Who do you think is the imposter?</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    choice = st.radio(
        "Select a player to eliminate:",
        st.session_state.alive_players,
        label_visibility="collapsed",
    )

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("⬅  Back to Discussion", type="secondary"):
            go_to("discussion")
            st.rerun()
    with col2:
        if st.button("⚡  Eliminate Player"):
            if choice:
                eliminated = choice
                new_alive = eliminate_player(st.session_state.alive_players, eliminated)
                winner = check_winner(new_alive, st.session_state.imposter, eliminated)

                st.session_state.alive_players = new_alive
                st.session_state.eliminated_player = eliminated
                st.session_state.winner = winner
                go_to("result")
                st.rerun()


# ── SCREEN 5 — Elimination Result ────────────────────────────────────────────
def screen_result():
    eliminated = st.session_state.eliminated_player
    winner = st.session_state.winner

    if winner:
        # Game over
        if winner == "civilian":
            title_class = "civilian-win"
            emoji = "🎉"
            headline = "CIVILIANS WIN"
            sub = f"The imposter was caught."
        else:
            title_class = "imposter-win"
            emoji = "🕵️"
            headline = "IMPOSTER WINS"
            sub = f"The imposter survived to the end."

        st.markdown(
            f"""
            <div style='text-align:center; padding:1rem 0 0.5rem;'>
                <span style='font-size:3rem;'>{emoji}</span>
                <h1 class='winner-title {title_class}'>{headline}</h1>
                <p style='color:#9CA3AF;'>{sub}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            f"""
            <div class='glass-card'>
                <p class='label-sm'>IMPOSTER</p>
                <p style='font-size:1.4rem; font-weight:600; color:#F9FAFB; margin:0.3rem 0;'>
                    {st.session_state.imposter}
                </p>
                <hr class='divider'>
                <p class='label-sm'>THE WORDS</p>
                <div class='reveal-pair'>
                    <span class='word-chip'>👥 {st.session_state.civilian_word}</span>
                    <span class='word-chip'>🕵️ {st.session_state.imposter_word}</span>
                </div>
                <p style='color:#4B5563; font-size:0.78rem; margin-top:0.5rem;'>
                    civilians &nbsp;&nbsp;·&nbsp;&nbsp; imposter
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄  New Round", type="secondary"):
                start_game_from_players(st.session_state.players)
                st.rerun()
        with col2:
            if st.button("🏠  New Game"):
                for key in list(st.session_state.keys()):
                    del st.session_state[key]
                st.rerun()

    else:
        # Game continues
        st.markdown(
            f"""
            <div style='text-align:center; padding:1rem 0;'>
                <span style='font-size:2.5rem;'>💀</span>
                <h2 style='margin:0.4rem 0;'>{eliminated} was eliminated.</h2>
                <p style='color:#6B7280;'>But the game isn't over yet.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            f"""
            <div class='glass-card'>
                <p class='label-sm'>REMAINING PLAYERS ({len(st.session_state.alive_players)})</p>
                <p style='font-size:1.1rem; color:#A78BFA; margin-top:0.4rem;'>
                    {"  ·  ".join(st.session_state.alive_players)}
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄  New Round", type="secondary"):
                start_game_from_players(st.session_state.players)
                st.rerun()
        with col2:
            if st.button("🗳️  Next Vote →"):
                go_to("discussion")
                st.rerun()


# ── Router ────────────────────────────────────────────────────────────────────
screen = st.session_state.screen

if screen == "registration":
    screen_registration()
elif screen == "reveal":
    screen_reveal()
elif screen == "discussion":
    screen_discussion()
elif screen == "voting":
    screen_voting()
elif screen == "result":
    screen_result()