RELAY_POINTS = {
    1: 60, 2: 50, 3: 45, 4: 41, 5: 38, 6: 35, 7: 32, 8: 30, 9: 28, 10: 26,
    11: 24, 12: 22, 13: 20, 14: 18, 15: 16, 16: 15, 17: 14, 18: 13, 19: 12, 20: 11,
    21: 10, 22: 9, 23: 8, 24: 7, 25: 6, 26: 5, 27: 4, 28: 3, 29: 2, 30: 1
}

def calculate_relay_scores(teams, club_to_district, district_config):
    """Calculates the district scores for the relay race."""
    
    district_scores = {district: 0 for district in district_config['districts'].values()}
    
    teams_by_district = {district: [] for district in district_config['districts'].values()}
    for team in teams:
        if team['status'] == '1':
            club_id = team['club_id']
            # This is the key change: the club_id in the team list IS the district id
            district_name = district_config['districts'].get(club_id)
            if district_name:
                teams_by_district[district_name].append(team)

    for district_name, district_teams in teams_by_district.items():
        district_teams.sort(key=lambda t: t['placement'])
        top_5_teams = district_teams[:5]
        for team in top_5_teams:
            placement = team['placement']
            if placement in RELAY_POINTS:
                district_scores[district_name] += RELAY_POINTS[placement]
                            
    return district_scores
