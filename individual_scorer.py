INDIVIDUAL_POINTS = {
    1: 48, 2: 42, 3: 36, 4: 32, 5: 28, 6: 27, 7: 26, 8: 25, 9: 24, 10: 23,
    11: 22, 12: 21, 13: 20, 14: 19, 15: 18, 16: 17, 17: 16, 18: 15, 19: 14, 20: 13,
    21: 12, 22: 11, 23: 10, 24: 9, 25: 8, 26: 7, 27: 6, 28: 5, 29: 4, 30: 3,
    31: 2, 32: 1
}

def calculate_individual_scores(classes, club_to_district, district_config):
    """Calculates the district scores for the individual race."""
    
    district_scores = {district: 0 for district in district_config['districts'].values()}
    
    for class_id, class_data in classes.items():
        class_district_points = {district: 0 for district in district_config['districts'].values()}
        
        runners_by_district = {district: [] for district in district_config['districts'].values()}
        for runner in class_data['runners']:
            if runner['status'] == '1':
                district_id = club_to_district.get(runner['club_id'])
                if district_id:
                    district_name = district_config['districts'].get(district_id)
                    if district_name:
                        runners_by_district[district_name].append(runner)

        for district_name, district_runners in runners_by_district.items():
            district_runners.sort(key=lambda r: r['placement'])
            top_4_runners = district_runners[:4]
            for runner in top_4_runners:
                placement = runner['placement']
                if placement in INDIVIDUAL_POINTS:
                    class_district_points[district_name] += INDIVIDUAL_POINTS[placement]
                                
        # Rank districts within the class
        sorted_districts = sorted(class_district_points.items(), key=lambda item: item[1], reverse=True)
        
        # Award points based on rank, handling ties
        i = 0
        while i < len(sorted_districts):
            j = i
            while j < len(sorted_districts) and sorted_districts[j][1] == sorted_districts[i][1]:
                j += 1
            
            rank_points = sum(range(i + 1, j + 1)) / (j - i)
            for k in range(i, j):
                district_scores[sorted_districts[k][0]] += rank_points
            i = j
            
    return district_scores
