def boundary_percentage(player_data):

    fours = (
        player_data["batter_runs"] == 4
    ).sum()

    sixes = (
        player_data["batter_runs"] == 6
    ).sum()

    boundaries = fours + sixes

    total_balls = len(player_data)

    percentage = (
        boundaries / total_balls * 100
        if total_balls > 0
        else 0
    )

    return {

        "fours": fours,
        "sixes": sixes,

        "boundary_percentage":
        percentage

    }
