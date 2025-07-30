import json
import xml.etree.ElementTree as ET

def load_district_config(file_path):
    """Loads the district configuration from a JSON file."""
    with open(file_path, 'r') as f:
        return json.load(f)

def parse_club_list(file_path):
    """Parses the club list from the XML file and returns a dictionary mapping club IDs to district IDs."""
    tree = ET.parse(file_path)
    root = tree.getroot()
    
    club_to_district = {}
    
    for club_element in root.findall('.//Club'):
        id_element = club_element.find('Id')
        if id_element is not None:
            club_id = id_element.text
            district_id_element = club_element.find('oData/District')
            if district_id_element is not None:
                district_id = district_id_element.text
                club_to_district[club_id] = district_id
            
    return club_to_district

def parse_class_list(file_path):
    """Parses the class list from the XML file and returns a dictionary of classes."""
    tree = ET.parse(file_path)
    root = tree.getroot()
    
    classes = {}
    
    for class_element in root.findall('.//Class'):
        id_element = class_element.find('Id')
        if id_element is not None:
            class_id = id_element.text
            name_element = class_element.find('Name')
            if name_element is not None:
                class_name = name_element.text
                classes[class_id] = {'name': class_name, 'runners': []}
        
    return classes

def parse_individual_results(file_path, classes):
    """Parses the individual race XML file and returns a list of runners."""
    tree = ET.parse(file_path)
    root = tree.getroot()
    
    for runner_element in root.findall('.//Runner'):
        class_id_element = runner_element.find('Class')
        if class_id_element is not None:
            class_id = class_id_element.text
            if class_id in classes:
                runner = {}
                runner['name'] = runner_element.find('Name').text
                runner['club_id'] = runner_element.find('Club').text
                runner['status'] = runner_element.find('Status').text
                classes[class_id]['runners'].append(runner)
            
    # Calculate placement within each class
    for class_id in classes:
        runners_in_class = classes[class_id]['runners']
        runners_in_class.sort(key=lambda r: (r['status'] != '1', r.get('finish_time', 99999)))
        for i, runner in enumerate(runners_in_class):
            runner['placement'] = i + 1
            
    return classes

def parse_relay_results(file_path):
    """Parses the relay race XML file and returns a list of teams."""
    tree = ET.parse(file_path)
    root = tree.getroot()
    
    teams = []
    
    for team_element in root.findall('.//Team'):
        team = {}
        team['name'] = team_element.find('Name').text
        team['club_id'] = team_element.find('Club').text
        team['status'] = team_element.find('Status').text
        teams.append(team)
        
    # Calculate placement
    teams.sort(key=lambda t: (t['status'] != '1', t.get('finish_time', 99999)))
    for i, team in enumerate(teams):
        team['placement'] = i + 1
        
    return teams


