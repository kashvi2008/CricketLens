from flask import Flask, render_template, request
import pandas as pd

from career_stats import get_career_stats
from season_analysis import get_season_analysis
from trend_analysis import career_trend
from peak_season import peak_season
from boundary_analysis import boundary_percentage
from predict_next_season import predict_next_season
from orange_cap import predict_top_batsmen
from purple_cap import predict_top_bowlers
from winner_prediction import predict_ipl_winner
from team_analysis import analyze_team 

app = Flask(__name__)

deliveries = pd.read_csv("ball_by_ball_data.csv")
batting_progress = pd.read_csv("ipl_batting_career_progression.csv")
bowling_progress = pd.read_csv("ipl_bowling_career_progression.csv")

teams = sorted(
    batting_progress["team"].dropna().unique()
)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/player", methods=["GET", "POST"])
def player():

    players = sorted(deliveries["batter"].dropna().unique())
    result = None

    if request.method == "POST":

        player_name = request.form["player"]

        player_data = deliveries[
            deliveries["batter"] == player_name
        ]

        career_data = batting_progress[
            batting_progress["player_name"].str.contains(
                player_name,
                case=False,
                regex=False,
                na=False
            )
        ]

        if career_data.empty:
            career_data = batting_progress[
                batting_progress["player_name"].str.contains(
                    player_name.split()[-1],
                    case=False,
                    regex=False,
                    na=False
                )
            ]

        stats = get_career_stats(deliveries, player_name)
        boundary = boundary_percentage(player_data)

        if not career_data.empty:

            analysis = get_season_analysis(career_data)
            trend = career_trend(career_data)
            peak = peak_season(career_data)
            predicted_runs = predict_next_season(career_data)

        else:
            analysis = {
                "best_year": "N/A",
                "worst_year": "N/A"
            }
            trend = "No Data"
            peak = {
                "season": "N/A",
                "runs": 0
            }
            predicted_runs = 0

        result = {
            "player": player_name,
            "stats": stats,
            "analysis": analysis,
            "trend": trend,
            "peak": peak,
            "boundary": boundary,
            "predicted_runs": predicted_runs
        }

    return render_template(
        "player.html",
        players=players,
        result=result
    )

@app.route("/orange-cap")
def orange_cap():
    predictions = predict_top_batsmen(batting_progress)
    return render_template("orange_cap.html", predictions=predictions)

@app.route("/purple-cap")
def purple_cap():
    predictions = predict_top_bowlers(bowling_progress)
    return render_template("purple_cap.html", predictions=predictions)

@app.route("/winner")
def winner():
    predictions = predict_ipl_winner(
        batting_progress,
        bowling_progress
    )
    return render_template("winner.html", predictions=predictions)

@app.route("/team-analysis", methods=["GET", "POST"])
def team_analysis():

    result = None

    if request.method == "POST":
        team = request.form["team"]

        result = analyze_team(
            team,
            batting_progress,
            bowling_progress
        )

    return render_template(
        "team_analysis.html",
        teams=teams,
        result=result
    )

if __name__ == "__main__":
    app.run(debug=True)
