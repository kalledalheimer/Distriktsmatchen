
import unittest
import os
import sys
from unittest.mock import patch, mock_open

# Add the project root to the sys.path to allow imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import data_parser

class TestDataParser(unittest.TestCase):

    def test_parse_club_list_from_old_format(self):
        xml_data = """
<meosdata version="3.6">
    <ClubList>
        <Club>
            <Id>32</Id>
            <Name>Almby IK</Name>
            <oData>
                <District>17</District>
            </oData>
        </Club>
        <Club>
            <Id>47</Id>
            <Name>Björkfors GOIF</Name>
            <oData>
                <District>24</District>
            </oData>
        </Club>
    </ClubList>
</meosdata>
"""
        with patch('xml.etree.ElementTree.parse') as mock_parse:
            with patch('builtins.open', mock_open(read_data=xml_data)):
                mock_tree = unittest.mock.MagicMock()
                mock_parse.return_value = mock_tree
                mock_root = unittest.mock.MagicMock()
                mock_tree.getroot.return_value = mock_root
                
                # Correctly mock the findall method to return a list of mocked Club elements
                mock_club_elements = []
                for club_id, district_id in [('32', '17'), ('47', '24')]:
                    mock_club = unittest.mock.MagicMock()
                    mock_id = unittest.mock.MagicMock()
                    mock_id.text = club_id
                    mock_district = unittest.mock.MagicMock()
                    mock_district.text = district_id
                    
                    mock_club.find.side_effect = [mock_id, mock_district]
                    mock_club_elements.append(mock_club)
                
                mock_root.findall.return_value = mock_club_elements

                club_to_district = data_parser.parse_club_list_from_old_format("dummy_path")
                
                self.assertEqual(club_to_district, {"32": "17", "47": "24"})

if __name__ == '__main__':
    unittest.main()
