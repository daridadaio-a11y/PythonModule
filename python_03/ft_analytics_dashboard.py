def ft_analytics_dashboard():
    player_list = [
        {"name" : "alice", "score": 2300, "active" : "on", "region" : "north", "achievements" : 5},
        {"name" : "bob", "score" : 1800, "active" : "on", "region" : "east", "achievements" : 3},
        {"name" : "charlie", "score" : 2150, "active" : "on", "region" : "central", "achievements" : 7},
        {"name" : "diana", "score" : 2050, "active" : "off", "region" : "north", "achievements" : 0}
    ]
    print("=== Game Analytics Dashboard ===\n")
    high_players_list = [data["name"] for data in player_list if data["score"] > 2000]
    scores_doubled = [score["score"] * 2 for score in player_list]
    active_players = [ap["name"] for ap in player_list if ap["active"] == "on"]
    print("=== List Comprehension Examples ===")
    print(f"High scores (>2000): {high_players_list}")
    print(f"Scores doubled: {scores_doubled}")
    print(f"Active players: {active_players}\n")
    player_scores = {player["name"] : player["score"] for player in player_list if player["active"] == "on"}
    
if __name__ == "__main__":
    ft_analytics_dashboard()