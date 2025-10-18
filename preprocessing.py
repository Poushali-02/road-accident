import pandas as pd
import numpy as np
from joblib import load

pipeline = load('pipeline.pkl')

def preprocess(data):
    df = pd.DataFrame([data])
    return pipeline.transform(df)


def generate_random_scenario(road_type_categories:list, 
                            lighting_categories:list, 
                            weather_categories:list, 
                            time_of_day_categories:list):
    return {
        'road_type': np.random.choice(road_type_categories),
        'num_lanes': np.random.randint(1, 5),
        'curvature': round(np.random.uniform(0, 1), 2),
        'speed_limit': np.random.randint(20, 101),
        'lighting': np.random.choice(lighting_categories),
        'weather': np.random.choice(weather_categories),
        'road_signs_present': np.random.choice([False, True]),
        'public_road': np.random.choice([False, True]),
        'time_of_day': np.random.choice(time_of_day_categories),
        'holiday': np.random.choice([False, True]),
        'school_season': np.random.choice([False, True]),
        'num_reported_accidents': np.random.randint(0, 11)
    }
