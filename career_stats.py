def get_career_stats(deliveries, player):

    player_data = deliveries[
        deliveries["batter"] == player
    ]

    if player_data.empty:
        return {
            "runs": 0,
            "innings": 0,
            "average": 0,
            "strike_rate": 0,
            "highest_score": 0,
            "fifties": 0,
            "hundreds": 0
        }

    total_runs = player_data["batter_runs"].sum()

    balls_faced = len(player_data)

    strike_rate = (
        total_runs / balls_faced * 100
        if balls_faced > 0
        else 0
    )

    dismissals = deliveries[
        deliveries["player_out"] == player
    ].shape[0]

    average = (
        total_runs / dismissals
        if dismissals > 0
        else total_runs
    )

    innings_scores = (
        player_data.groupby("match_id")["batter_runs"]
        .sum()
    )

    highest_score = innings_scores.max()

    fifties = (
        (innings_scores >= 50)
        & (innings_scores < 100)
    ).sum()

    hundreds = (
        innings_scores >= 100
    ).sum()

    innings = (
        player_data["match_id"]
        .nunique()
    )

    return {
        "runs": total_runs,
        "innings": innings,
        "average": average,
        "strike_rate": strike_rate,
        "highest_score": highest_score,
        "fifties": fifties,
        "hundreds": hundreds
    }
