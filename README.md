# 🚗 Pick the Safer Road Game 🏁

**Road Safety AI Game** - Test your intuition about road safety with an AI-powered prediction model!

## 🎮 Game Overview

**Pick the Safer Road** is an interactive web game where players compete against time to identify which of two road scenarios is safer. The game uses a trained machine learning model to predict accident rates based on road conditions.

### 🎯 How to Play

1. **Click "START GAME"** - A timer begins
2. **Analyze two road scenarios** with different conditions (weather, lighting, road type, etc.)
3. **Choose the safer road** before time runs out
4. **Earn points based on speed** - Quick answers = more points
5. **Win at 50 points** - Complete 10 rounds or reach 50 points first
6. **Track your winning streak** - How many games can you win in a row?

### 📊 Scoring System

- **Maximum: 10 points per round** for correct answers
- **Time-based deduction**: -1 point per 10 seconds
- **Minimum: 0 seconds** (wrong answers = 0 points)
- **Winning threshold: 50 points** across all rounds
- **Instant win**: Game stops immediately after reaching 50 points

### 🏆 Features

- ⏱️ **Time pressure** - Race against the clock to maximize points
- 🎲 **Random scenarios** - Ensures significantly different predictions
- 📊 **Score tracking** - Total score, round counter, points needed
- 🔥 **Winning streak** - Highlighted metric showing consecutive wins
- 🎉 **Instant win detection** - Game ends as soon as 50 points reached
- 📈 **Round-by-round breakdown** - See your score history
- 🎨 **Beautiful UI** - Colorful, responsive design with gradients

---

## 🚀 Live Server

🌐 **Play Now:** https://road-accident-vseuhvwqersrexrv7fxncg.streamlit.app/

The game is live and ready to play! No installation needed - just click and start playing.

---

## 🛠️ Setup Instructions

### Prerequisites

- **Conda** (Anaconda or Miniconda installed)
- **Git** (for cloning the repository)
- **Python 3.10** (specified in environment.yml)

### Step 1: Clone the Repository

```bash
git clone https://github.com/Poushali-02/road-accident.git
cd road-accident
```

### Step 2: Create Conda Environment

Using the provided `environment.yml`:

```bash
conda env create -f environment.yml
```

This will create a conda environment named `accident` with all required dependencies at their exact versions.

### Step 3: Activate the Environment

```bash
conda activate accident
```

You should see `(accident)` in your terminal prompt.

### Step 4: Install requirements


### Step 5: Run the Application

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

---

## 📦 Project Structure

```
road-accident/
├── app.py                          # Main Streamlit application
├── preprocessing.py                # Data preprocessing functions
├── model.py                        # Model loading and prediction
├── data.py                         # Road/weather categories
├── model.keras                     # Trained TensorFlow model (~100MB)
├── pipeline.pkl                    # Preprocessing pipeline
├── requirements.txt                # Pip dependencies
├── environment.yml                 # Conda environment specification
├── runtime.txt                     # Python version for deployment
├── README.md                       # This file
└── DEPLOYMENT_CHECKLIST.md         # Deployment guide
```

---

## 🔧 Requirements

### Python Packages (Auto-installed via Conda)

| Package | Version | Purpose |
|---------|---------|---------|
| streamlit | latest | Web framework for interactive UI |
| tensorflow | 2.18.0 | Deep learning framework for predictions |
| scikit-learn | 1.2.2 | Machine learning utilities |
| pandas | 2.2.3 | Data manipulation |
| numpy | 1.26.4 | Numerical computing |
| joblib | 1.5.1 | Model serialization |
| tf-keras | 2.18.0 | Keras API for TensorFlow |
| dill | 0.3.8 | Enhanced pickling for pipeline |

### System Requirements

- **OS**: Windows, macOS, Linux
- **Python**: 3.10
- **RAM**: 2GB minimum (model loading)
- **Storage**: ~500MB (model + dependencies)

---

## 🎯 Understanding the Game

### Road Attributes

Each road scenario has these attributes:

| Attribute | Options |
|-----------|---------|
| Road Type | Highway, Urban, Rural |
| Number of Lanes | 1-4 |
| Curvature | 0.0 - 1.0 |
| Speed Limit | 20-100 km/h |
| Lighting | Daylight, Dim, Night |
| Weather | Clear, Foggy, Rainy |
| Road Signs | Yes/No |
| Public Road | Yes/No |
| Time of Day | Morning, Afternoon, Evening |
| Holiday | Yes/No |
| School Season | Yes/No |

### Model Prediction

The AI model analyzes these factors and predicts the expected number of accidents. **Lower predictions = Safer road**.

---

## 🚀 Deployment

### Option 1: Streamlit Cloud (Recommended - Already Live!)

The app is already deployed at:
🌐 https://road-accident-vseuhvwqersrexrv7fxncg.streamlit.app/

### Option 2: Local Deployment

Run locally using the setup instructions above.

### Option 3: Docker Deployment

```bash
docker build -t road-safety-game .
docker run -p 8501:8501 road-safety-game
```

See `DEPLOYMENT_CHECKLIST.md` for more deployment options.

---

## 🎓 How the Model Works

### Training Data
- Kaggle Road Accident Competition dataset
- Features: Road conditions, weather, time factors
- Target: Number of reported accidents

### Preprocessing Pipeline
- Categorical features → Ordinal encoding
- Numerical features → Standard scaling
- Passthrough of certain features

### Model Architecture
- TensorFlow/Keras neural network
- Trained to predict accident count
- Outputs: Expected number of accidents per scenario

---

## 🐛 Troubleshooting

### Issue: Module not found error
```bash
# Ensure environment is activated
conda activate accident

# Verify installation
conda list
```

### Issue: Model.keras not found
```
# Ensure you're in the project root directory
# File should be at: ./model.keras
ls model.keras  # macOS/Linux
dir model.keras # Windows
```

### Issue: Slow predictions on first run
- Normal behavior - model loads on startup (~2-3 seconds)
- Subsequent predictions are cached and faster

### Issue: Port 8501 already in use
```bash
streamlit run app.py --server.port 8502
```

---

## 🤝 Contributing

Contributions welcome! Feel free to:
- Report bugs
- Suggest game improvements
- Optimize model performance
- Enhance UI/UX

---

## 📝 License

This project is part of the Kaggle Road Accident Competition.

---

## 👤 Author

**Poushali-02**
- GitHub: https://github.com/Poushali-02/road-accident
- Repository: road-accident (Kaggle & Stack Overflow competition)

---

## 🎉 Quick Start Summary

```bash
# 1. Clone
git clone https://github.com/Poushali-02/road-accident.git
cd road-accident

# 2. Create environment
conda env create -f environment.yml

# 3. Activate
conda activate accident

# 4. Run
streamlit run app.py

# 5. Play!
# Open browser at http://localhost:8501
```

Or **play directly online:** https://road-accident-vseuhvwqersrexrv7fxncg.streamlit.app/

---

## 📊 Game Statistics Explained

- **🏆 Total Score**: Cumulative points across all rounds
- **📊 Round**: Current round progress (e.g., 3/10)
- **🎯 Target**: Points needed to win (50)
- **🔥 Winning Streak**: Consecutive games won (resets on loss)

---

## 🔥 Tips to Win

1. **Make quick decisions** - Speed = more points
2. **Focus on key factors** - Weather, lighting, road type matter most
3. **Learn from feedback** - See predictions after each answer
4. **Practice patterns** - Similar conditions often have similar risk levels
5. **Beat the clock** - Each second costs you points!

---

## 🎮 Game Flow Diagram

```
START → Generate 2 Scenarios → User Sees Roads → Timer Runs
   ↓                                               ↓
   └─────────────────────── User Chooses Road ────┘
                                  ↓
                         Check if Correct?
                              ↙      ↖
                          YES        NO
                           ↓          ↓
                      Award Points  Award 0
                           ↓          ↓
                         Score ≥ 50?
                         ↙        ↖
                       YES         NO
                        ↓           ↓
                    YOU WIN!  Continue Playing
                        ↓
                   Show Results
                   Winning Streak +1
```

---

**Enjoy the game! Test your road safety intuition! 🚗🎮**



check