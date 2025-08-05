import json
import xml.etree.ElementTree as ET

def load_district_config(file_path):
    """Loads the district configuration from a JSON file."""
    with open(file_path, 'r') as f:
        return json.load(f)

def parse_club_list_from_old_format(file_path):
    """Parses the club list from the old XML file format and returns a dictionary mapping club IDs to district IDs."""
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

def parse_club_list(file_path):
    """Parses the club list from the XML file and returns a dictionary mapping club IDs to district IDs."""
    tree = ET.parse(file_path)
    root = tree.getroot()
    
    club_to_district = {}
    
    # Define the namespace for the IOF 3.0 XML format
    ns = {'ns': 'http://www.orienteering.org/datastandard/3.0'}
    
    for organisation_element in root.findall('.//ns:Organisation', ns):
        id_element = organisation_element.find('ns:Id', ns)
        if id_element is not None:
            club_id = id_element.text
            # In the new format, we need to find the district mapping from the old file
            # This will be handled in the main script
            pass
            
    return club_to_district

def parse_class_list(file_path):
    """Parses the class list from the XML file and returns a dictionary of classes."""
    tree = ET.parse(file_path)
    root = tree.getroot()
    
    classes = {}
    ns = {'ns': 'http://www.orienteering.org/datastandard/3.0'}

    for class_element in root.findall('.//ns:Class', ns):
        id_element = class_element.find('ns:Id', ns)
        if id_element is not None:
            class_id = id_element.text
            name_element = class_element.find('ns:Name', ns)
            if name_element is not None:
                class_name = name_element.text
                classes[class_id] = {'name': class_name, 'runners': []}
        
    return classes

def parse_individual_results(file_path, classes):
    """Parses the individual race XML file and returns a list of runners."""
    tree = ET.parse(file_path)
    root = tree.getroot()
    ns = {'ns': 'http://www.orienteering.org/datastandard/3.0'}

    for class_result_element in root.findall('.//ns:ClassResult', ns):
        class_element = class_result_element.find('ns:Class', ns)
        if class_element is not None:
            class_id_element = class_element.find('ns:Id', ns)
            if class_id_element is not None:
                class_id = class_id_element.text
                if class_id in classes:
                    for person_result_element in class_result_element.findall('ns:PersonResult', ns):
                        runner = {}
                        person_element = person_result_element.find('ns:Person', ns)
                        name_element = person_element.find('ns:Name', ns)
                        runner['name'] = name_element.find('ns:Given', ns).text + " " + name_element.find('ns:Family', ns).text
                        
                        organisation_element = person_result_element.find('ns:Organisation', ns)
                        if organisation_element is not None:
                            club_id_element = organisation_element.find('ns:Id', ns)
                            if club_id_element is not None:
                                runner['club_id'] = club_id_element.text

                        result_element = person_result_element.find('ns:Result', ns)
                        status_element = result_element.find('ns:Status', ns)
                        
                        if status_element.text == 'OK':
                            runner['status'] = '1'
                        else:
                            runner['status'] = '0'

                        position_element = result_element.find('ns:Position', ns)
                        if position_element is not None and position_element.text is not None:
                            runner['placement'] = int(position_element.text)
                        else:
                            runner['placement'] = 9999

                        classes[class_id]['runners'].append(runner)

    for class_id in classes:
        runners_in_class = classes[class_id]['runners']
        runners_in_class.sort(key=lambda r: r['placement'])

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


