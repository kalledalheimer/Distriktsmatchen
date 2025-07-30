import argparse
import datetime
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

import data_parser
import individual_scorer
import relay_scorer

INDIVIDUAL_RESULTS_FILE = 'doc/Distrmatch_2019-08-06_190806_1620_efter målgång.meosxml'
RELAY_RESULTS_FILE = 'doc/Distrmatch_stafett_2019-08-07_190807_2100_justerad.meosxml'
CONFIG_FILE = 'config.json'

def generate_pdf_report(individual_scores=None, relay_scores=None):
    doc = SimpleDocTemplate(f"Distriktsmatchen_Results_{datetime.datetime.now().year}.pdf", pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    # Headline
    story.append(Paragraph(f"Distriktsmatchen {datetime.datetime.now().year}", styles['h1']))
    story.append(Spacer(1, 0.2 * 100))

    if individual_scores:
        story.append(Paragraph("--- Resultat Individuell Tävling ---", styles['h2']))
        for district, score in sorted(individual_scores.items(), key=lambda item: item[1]):
            story.append(Paragraph(f"{district}: {score} poäng", styles['Normal']))
        story.append(Spacer(1, 0.2 * 100))

    if relay_scores:
        story.append(Paragraph("--- Resultat Stafett ---", styles['h2']))
        for district, score in sorted(relay_scores.items(), key=lambda item: item[1], reverse=True):
            story.append(Paragraph(f"{district}: {score} poäng", styles['Normal']))
        story.append(Spacer(1, 0.2 * 100))

    doc.build(story)
    print(f"\nPDF report generated: Distriktsmatchen_Results_{datetime.datetime.now().year}.pdf")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Calculate Distriktsmatchen results.")
    parser.add_argument('--individual', action='store_true', help='Calculate individual race results.')
    parser.add_argument('--relay', action='store_true', help='Calculate relay race results.')
    parser.add_argument('--all', action='store_true', help='Calculate both individual and relay race results (default).')
    parser.add_argument('--individual-file', type=str, default=INDIVIDUAL_RESULTS_FILE, help='Path to the individual race XML results file.')
    parser.add_argument('--relay-file', type=str, default=RELAY_RESULTS_FILE, help='Path to the relay race XML results file.')
    parser.add_argument('--pdf', action='store_true', help='Generate a PDF report of the results.')
    args = parser.parse_args()

    if not (args.individual or args.relay or args.all):
        args.all = True # Default to --all if no arguments are provided

    print("Distriktsmatchen Results Calculator")

    individual_scores = None
    relay_scores = None

    # Load configuration
    district_config = data_parser.load_district_config(CONFIG_FILE)

    if args.individual or args.all:
        # Individual race
        club_to_district_ind = data_parser.parse_club_list(args.individual_file)
        classes = data_parser.parse_class_list(args.individual_file)
        individual_results = data_parser.parse_individual_results(args.individual_file, classes)
        individual_scores = individual_scorer.calculate_individual_scores(individual_results, club_to_district_ind, district_config)

        # Print results to console
        print("\n--- Individual Race Results ---")
        for district, score in sorted(individual_scores.items(), key=lambda item: item[1]):
            print(f"{district}: {score} points")

    if args.relay or args.all:
        # Relay race
        club_to_district_relay = data_parser.parse_club_list(args.relay_file)
        relay_results = data_parser.parse_relay_results(args.relay_file)
        relay_scores = relay_scorer.calculate_relay_scores(relay_results, club_to_district_relay, district_config)

        # Print results to console
        print("\n--- Relay Race Results ---")
        for district, score in sorted(relay_scores.items(), key=lambda item: item[1], reverse=True):
            print(f"{district}: {score} points")

    if args.pdf:
        generate_pdf_report(individual_scores, relay_scores)
