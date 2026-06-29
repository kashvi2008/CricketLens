def get_season_analysis(career_data):

    best_season = career_data.loc[
        career_data["runs_scored"].idxmax()
    ]

    worst_season = career_data.loc[
        career_data["runs_scored"].idxmin()
    ]

    highest_average = career_data.loc[
        career_data["batting_average"].idxmax()
    ]

    return {

        "best_year":
        best_season["season"],

        "best_runs":
        best_season["runs_scored"],

        "worst_year":
        worst_season["season"],

        "worst_runs":
        worst_season["runs_scored"],

        "peak_avg_year":
        highest_average["season"],

        "peak_avg":
        highest_average["batting_average"]

    }
