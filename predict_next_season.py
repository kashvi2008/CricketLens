from sklearn.linear_model import LinearRegression
import numpy as np

def predict_next_season(career_data):

    if career_data.empty or len(career_data) < 2:
        return 0

    seasons = (
        career_data["season"]
        .values
        .reshape(-1, 1)
    )

    runs = career_data[
        "runs_scored"
    ].values

    model = LinearRegression()

    model.fit(
        seasons,
        runs
    )

    next_year = np.array(
        [[career_data["season"].max() + 1]]
    )

    prediction = model.predict(
        next_year
    )

    return int(prediction[0])
