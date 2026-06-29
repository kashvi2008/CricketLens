from sklearn.linear_model import LinearRegression
import numpy as np

def predict_top_bowlers(bowling_data):

    latest_season = bowling_data["season"].max()

    latest = (
        bowling_data
        .groupby("player_name")["season"]
        .max()
    )

    active_players = latest[
        latest >= latest_season - 1
    ].index

    predictions = []

    for player in active_players:

        player_df = bowling_data[
            bowling_data["player_name"] == player
        ].sort_values("season")

        if len(player_df) < 3:
            continue

        X = player_df["season"].values.reshape(-1, 1)
        y = player_df["total_wickets"].values

        model = LinearRegression()
        model.fit(X, y)

        next_year = np.array(
            [[latest_season + 1]]
        )

        predicted_wickets = int(
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

            "predicted_wickets": predicted_wickets

        })

    predictions = sorted(

        predictions,

        key=lambda x: x["predicted_wickets"],

        reverse=True

    )

    return predictions[:10]
