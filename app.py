import streamlit as st
from preprocessing import preprocess, generate_random_scenario
from model import prediction
from data import Categories
import time

# Page config
st.set_page_config(page_title="Road Safety Game", page_icon="🚗", layout="wide")

# Custom CSS for better styling
st.markdown("""
    <style>
    .game-title {
        text-align: center;
        color: #FF6B6B;
        font-size: 3em;
        font-weight: bold;
        margin-bottom: 10px;
    }
    .game-subtitle {
        text-align: center;
        color: #4ECDC4;
        font-size: 1.2em;
        margin-bottom: 30px;
    }
    .scenario-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .scenario-card.safe {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
    }
    .scenario-card.risky {
        background: linear-gradient(135deg, #eb3349 0%, #f45c43 100%);
    }
    .game-stats {
        display: flex;
        justify-content: space-around;
        margin: 20px 0;
        padding: 15px;
        background-color: #f0f2f6;
        border-radius: 10px;
    }
    .stat-item {
        text-align: center;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

def display_scenario(scen, title):
    if scen is None:
        return
    
    with st.container():
        st.markdown(f"### 🛣️ {title}")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"**🚗 Road Type:** `{scen['road_type'].upper()}`")
            st.markdown(f"**🛑 Lanes:** `{scen['num_lanes']}`")
            st.markdown(f"**🔀 Curvature:** `{scen['curvature']:.2f}`")
            st.markdown(f"**⚡ Speed Limit:** `{scen['speed_limit']} km/h`")
        
        with col2:
            st.markdown(f"**☀️ Lighting:** `{scen['lighting'].upper()}`")
            st.markdown(f"**🌦️ Weather:** `{scen['weather'].upper()}`")
            st.markdown(f"**🚨 Road Signs:** `{'✓ YES' if scen['road_signs_present'] else '✗ NO'}`")
            st.markdown(f"**🏙️ Public Road:** `{'✓ YES' if scen['public_road'] else '✗ NO'}`")
        
        col3, col4 = st.columns(2)
        with col3:
            st.markdown(f"**🕐 Time of Day:** `{scen['time_of_day'].upper()}`")
            st.markdown(f"**🎉 Holiday:** `{'✓ YES' if scen['holiday'] else '✗ NO'}`")
        
        with col4:
            st.markdown(f"**📚 School Season:** `{'✓ YES' if scen['school_season'] else '✗ NO'}`")
            st.markdown(f"**📊 Reported Accidents:** `{scen['num_reported_accidents']}`")

def check_guess(choice):
    st.session_state.guessed = True
    correct = st.session_state.correct
        
    # Calculate time-based score
    if st.session_state.round_start_time is not None:
        elapsed_time = time.time() - st.session_state.round_start_time
        # Score calculation: 10 points max, decreases by 1 point per 10 seconds
        # Minimum 0 points if takes > 100 seconds
        time_score = max(0, 10 - (elapsed_time / 10))
    else:
        time_score = 10
    
    # Only add to score if answer is correct
    if choice == correct:
        st.session_state.round_scores.append(time_score)
        st.session_state.score += time_score
    else:
        st.session_state.round_scores.append(0)
    
    # Display result with animation
    result_placeholder = st.empty()
    
    if choice == correct:
        with result_placeholder.container():
            st.balloons()
            st.success("🎉🎉🎉 CORRECT! You picked the safer road! 🎉🎉🎉")
            st.markdown(f"<h3 style='color: #11998e; text-align: center;'>You earned {time_score:.1f} points! ⚡</h3>", unsafe_allow_html=True)
    else:
        with result_placeholder.container():
            st.error("❌ WRONG! The other road was safer. Better luck next time! 💪")
            st.markdown("<h3 style='color: #eb3349; text-align: center;'>0 points this round 📖</h3>", unsafe_allow_html=True)
    
    # Display comparison
    st.markdown("---")
    st.markdown("### 📊 Accident Prediction Comparison")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="Road 1 Predicted Accidents", 
                 value=f"{st.session_state.pred1:.2f}",
                 delta=None,
                 delta_color="inverse")
    with col2:
        st.metric(label="Road 2 Predicted Accidents",
                 value=f"{st.session_state.pred2:.2f}",
                 delta=None,
                 delta_color="inverse")
    
    safer_road = 1 if st.session_state.pred1 < st.session_state.pred2 else 2
    danger_diff = abs(st.session_state.pred1 - st.session_state.pred2)
    st.info(f"🏆 Road {safer_road} is safer with {danger_diff:.2f} fewer predicted accidents!")
    # Display round time
    if st.session_state.round_start_time is not None:
        st.markdown(f"⏱️ **Time taken:** {elapsed_time:.1f} seconds")
    
    # Check if winning score reached - INSTANT WIN
    if st.session_state.score >= WINNING_SCORE:
        st.session_state.game_over = True
        st.session_state.game_won = True
        st.session_state.winning_streak += 1
    
    # Check if game is complete (only if score < WINNING_SCORE)
    elif st.session_state.games_played >= TOTAL_ROUNDS:
        st.session_state.game_over = True
        st.session_state.game_won = False
            
# Streamlit app
st.markdown("<h1 class='game-title'>🚗 Pick the Safer Road Game 🏁</h1>", unsafe_allow_html=True)
st.markdown("<p class='game-subtitle'>Test your intuition about road safety! Can you predict which road is safer? 🎮</p>", unsafe_allow_html=True)

# Initialize score tracking
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'games_played' not in st.session_state:
    st.session_state.games_played = 0
if 'round_start_time' not in st.session_state:
    st.session_state.round_start_time = None
if 'round_scores' not in st.session_state:
    st.session_state.round_scores = []
if 'game_over' not in st.session_state:
    st.session_state.game_over = False
if 'game_won' not in st.session_state:
    st.session_state.game_won = None
if 'winning_streak' not in st.session_state:
    st.session_state.winning_streak = 0

TOTAL_ROUNDS = 10
WINNING_SCORE = 50  # Winning threshold

def start_game():
    while True:
        scenario1 = generate_random_scenario(Categories.road_type_categories, 
                                            Categories.lighting_categories, 
                                            Categories.weather_categories, 
                                            Categories.time_of_day_categories)

        scenario2 = generate_random_scenario(Categories.road_type_categories, 
                                            Categories.lighting_categories, 
                                            Categories.weather_categories, 
                                            Categories.time_of_day_categories)

        pred1 = prediction(preprocess(scenario1))
        pred2 = prediction(preprocess(scenario2))

        # Ensure predictions differ by at least 0.5 (adjust threshold as needed)
        if abs(pred1 - pred2) > 0.05:
            break
    
    # Store in session state
    st.session_state.scenario1 = scenario1
    st.session_state.scenario2 = scenario2
    st.session_state.pred1 = pred1
    st.session_state.pred2 = pred2
    st.session_state.correct = 1 if pred1 < pred2 else 2
    st.session_state.guessed = False

# Display score and round info
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("🏆 Total Score", f"{st.session_state.score:.1f}")
with col2:
    st.metric("📊 Round", f"{st.session_state.games_played}/{TOTAL_ROUNDS}")
with col3:
    st.metric("🎯 Target", f"{WINNING_SCORE}")
with col4:
    # Highlighted winning streak metric
    st.markdown("""
    <div style='background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%); 
                padding: 20px; border-radius: 10px; text-align: center; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);'>
        <h4 style='margin: 0; color: #8B4513;'>🔥 WINNING STREAK</h4>
        <h2 style='margin: 5px 0; color: #8B4513;'>{}</h2>
    </div>
    """.format(st.session_state.winning_streak), unsafe_allow_html=True)

st.markdown("---")

# Show game over screen if applicable
if st.session_state.game_over:
    st.markdown("<h2 style='text-align: center; color: #FF6B6B;'>🎮 GAME OVER! 🎮</h2>", unsafe_allow_html=True)
    
    if st.session_state.game_won:
        st.balloons()
        st.success(f"🏆 🏆 🏆 YOU WON! 🏆 🏆 🏆")
        st.markdown(f"<h2 style='text-align: center; color: #11998e;'>Final Score: {st.session_state.score:.1f}/{TOTAL_ROUNDS * 10}</h2>", unsafe_allow_html=True)
        st.markdown(f"<h3 style='text-align: center; color: #11998e;'>You reached the winning threshold of {WINNING_SCORE} points in just {st.session_state.games_played} rounds! 🌟</h3>", unsafe_allow_html=True)
        
        # Highlighted winning streak
        st.markdown("""
        <div style='background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%); 
                    padding: 30px; border-radius: 15px; text-align: center; margin: 20px 0; box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);'>
            <h2 style='margin: 0; color: #8B4513;'>🔥 WINNING STREAK 🔥</h2>
            <h1 style='margin: 10px 0; color: #8B4513; font-size: 4em;'>{}</h1>
        </div>
        """.format(st.session_state.winning_streak), unsafe_allow_html=True)
    else:
        st.error(f"❌ Game Over - You didn't reach the winning score")
        st.markdown(f"<h2 style='text-align: center; color: #eb3349;'>Final Score: {st.session_state.score:.1f}/{TOTAL_ROUNDS * 10}</h2>", unsafe_allow_html=True)
        st.markdown(f"<h3 style='text-align: center; color: #eb3349;'>You needed {WINNING_SCORE} points to win, but scored only {st.session_state.score:.1f}</h3>", unsafe_allow_html=True)
        # Reset winning streak on loss
        st.session_state.winning_streak = 0
    
    st.markdown("---")
    st.markdown("### 📈 Round-by-Round Scores:")
    for i, score in enumerate(st.session_state.round_scores, 1):
        st.write(f"Round {i}: {score:.1f} points")
    
    if st.button("🔄 START NEW GAME", key="new_game", use_container_width=True):
        st.session_state.score = 0
        st.session_state.games_played = 0
        st.session_state.round_scores = []
        st.session_state.game_over = False
        st.session_state.game_won = None
        if 'scenario1' in st.session_state:
            del st.session_state.scenario1
        st.rerun()
else:
    # Start game button
    if st.button("🎲 START GAME 🎲", key="start_btn", help="Click to begin a new challenge!"):
        start_game()
        st.session_state.round_start_time = time.time()
        st.session_state.games_played += 1
        st.rerun()
    
if 'scenario1' in st.session_state and st.session_state.scenario1 is not None:
    st.markdown("### 🚀 CHOOSE YOUR PATH 🚀")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Road Option 1️⃣")
        display_scenario(st.session_state.scenario1, "ROAD 1")
        if st.button("🚗 CHOOSE ROAD 1", key="choose1", disabled=st.session_state.guessed, 
                    help="Click to pick this road as safer", use_container_width=True):
            check_guess(1)
    
    with col2:
        st.markdown("#### Road Option 2️⃣")
        display_scenario(st.session_state.scenario2, "ROAD 2")
        if st.button("🚗 CHOOSE ROAD 2", key="choose2", disabled=st.session_state.guessed,
                    help="Click to pick this road as safer", use_container_width=True):
            check_guess(2)
    
    if st.session_state.guessed:
        st.markdown("---")
        if st.session_state.games_played < TOTAL_ROUNDS:
            col1, col2 = st.columns([1, 1])
            with col1:
                if st.button("🔄 PLAY AGAIN 🔄", key="play_again", 
                            help="Click for a new challenge!", use_container_width=True):
                    start_game()
                    st.session_state.round_start_time = time.time()
                    st.session_state.games_played += 1
                    st.rerun()
            with col2:
                if st.button("🏠 STOP GAME 🏠", key="stop", 
                            help="End current game", use_container_width=True):
                    st.session_state.game_over = True
                    st.rerun()
        else:
            st.info("🎮 All 10 rounds completed! Check your final score above.")

st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: #666; margin-top: 50px;'>
    <h3>💡 How does this work?</h3>
    <p>The AI model analyzes road conditions like weather, lighting, road type, and more to predict accident risk.<br>
    Your goal: Use your intuition to pick the safer road before seeing the predictions!</p>
    <p style='font-size: 0.9em; color: #999;'>🛣️ Lower predicted accidents = Safer road 🛣️</p>
    </div>
""", unsafe_allow_html=True)