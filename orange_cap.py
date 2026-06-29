from sklearn.linear_model import LinearRegression
import numpy as np

def predict_top_batsmen(batting_data):

    latest_season = batting_data["season"].max()

    latest = (
        batting_data
        .groupby("player_name")["season"]
        .max()
    )

    active_players = latest[
        latest >= latest_season - 1
    ].index

    predictions = []

    for player in active_players:

        player_df = batting_data[
            batting_data["player_name"] == player
        ].sort_values("season")

        if len(player_df) < 3:
            continue

        X = player_df["season"].values.reshape(-1, 1)
        y = player_df["runs_scored"].values

        model = LinearRegression()
        model.fit(X, y)

        next_year = np.array(
            [[latest_season + 1]]
        )

        predicted_runs = int(
            max(
                0,
                model.predict(next_year)[0]
            )
        )

        team = (
            player_df
            .iloc[-1]["team"]
        )

        predictions.append({

            "player": player,

            "team": team,

            "predicted_runs": predicted_runs

        })

    predictions = sorted(

        predictions,

        key=lambda x: x["predicted_runs"],

        reverse=True

    )

    return predictions[:10]
