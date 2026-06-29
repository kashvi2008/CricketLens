def peak_season(career_data):

    peak = career_data.loc[
        career_data["runs_scored"].idxmax()
    ]

    return {

        "season":
        peak["season"],

        "runs":
        peak["runs_scored"]

    }
