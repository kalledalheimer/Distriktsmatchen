import argparse
import data_parser
import individual_scorer
import relay_scorer

INDIVIDUAL_RESULTS_FILE = 'doc/Distrmatch_2019-08-06_190806_1620_efter målgång.meosxml'
RELAY_RESULTS_FILE = 'doc/Distrmatch_stafett_2019-08-07_190807_2100_justerad.meosxml'
CONFIG_FILE = 'config.json'

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Calculate Distriktsmatchen results.")
    parser.add_argument('--individual', action='store_true', help='Calculate individual race results.')
    parser.add_argument('--relay', action='store_true', help='Calculate relay race results.')
    parser.add_argument('--all', action='store_true', help='Calculate both individual and relay race results (default).')
    args = parser.parse_args()

    if not (args.individual or args.relay or args.all):
        args.all = True # Default to --all if no arguments are provided

    print("Distriktsmatchen Results Calculator")

    # Load configuration
    district_config = data_parser.load_district_config(CONFIG_FILE)

    if args.individual or args.all:
        # Individual race
        club_to_district_ind = data_parser.parse_club_list(INDIVIDUAL_RESULTS_FILE)
        classes = data_parser.parse_class_list(INDIVIDUAL_RESULTS_FILE)
        individual_results = data_parser.parse_individual_results(INDIVIDUAL_RESULTS_FILE, classes)
        individual_scores = individual_scorer.calculate_individual_scores(individual_results, club_to_district_ind, district_config)

        # Print results
        print("\n--- Individual Race Results ---")
        # Sort by score ascending (lower is better)
        for district, score in sorted(individual_scores.items(), key=lambda item: item[1]):
            print(f"{district}: {score} points")

    if args.relay or args.all:
        # Relay race
        club_to_district_relay = data_parser.parse_club_list(RELAY_RESULTS_FILE)
        relay_results = data_parser.parse_relay_results(RELAY_RESULTS_FILE)
        relay_scores = relay_scorer.calculate_relay_scores(relay_results, club_to_district_relay, district_config)

        # Print results
        print("\n--- Relay Race Results ---")
        # Sort by score descending (higher is better)
        for district, score in sorted(relay_scores.items(), key=lambda item: item[1], reverse=True):
            print(f"{district}: {score} points")
