# Product Requirements Document: Distriktsmatchen Results Calculator

## 1. Introduction

This document outlines the requirements for the Distriktsmatchen Results Calculator, a software application designed to automate the calculation of results for a youth orienteering competition between four Swedish districts: Värmland, Södermanland, Örebro län, and Östergötland. The competition consists of an individual middle-distance race and a relay race, each with its own scoring system.

The application will parse XML result files from the race organizers, calculate the scores according to the rules defined in this document, and present the final standings for both the individual and relay events.

## 2. Functional Requirements

### 2.1. Data Import and Parsing

*   The application must be able to import and parse MEOS XML result files for both the individual and relay races.
*   The application must be able to handle separate files for each race type.
*   The application must extract the following information for each competitor in the individual race:
    *   Full Name
    *   Club
    *   Class (H13, D13, etc.)
    *   Final Placement
*   The application must extract the following information for each team in the relay race:
    *   Team Name
    *   Club
    *   Final Placement

### 2.2. Individual Race Calculation

*   The application must correctly calculate the individual points for each runner based on their placement in their class, according to the following table:

| Placement | Points | Placement | Points | Placement | Points | Placement | Points |
| :-------- | :----- | :-------- | :----- | :-------- | :----- | :-------- | :----- |
| 1         | 48     | 11        | 22     | 21        | 12     | 31        | 2      |
| 2         | 42     | 12        | 21     | 22        | 11     | 32        | 1      |
| 3         | 36     | 13        | 20     | 23        | 10     |           |        |
| 4         | 32     | 14        | 19     | 24        | 9      |           |        |
| 5         | 28     | 15        | 18     | 25        | 8      |           |        |
| 6         | 27     | 16        | 17     | 26        | 7      |           |        |
| 7         | 26     | 17        | 16     | 27        | 6      |           |        |
| 8         | 25     | 18        | 15     | 28        | 5      |           |        |
| 9         | 24     | 19        | 14     | 29        | 4      |           |        |
| 10        | 23     | 20        | 13     | 30        | 3      |           |        |

*   For each of the eight classes, the application must sum the points of the top four runners from each district.
*   The application must rank the districts within each class based on their total points (highest score gets 1 point, second highest gets 2, etc.).
*   In case of a tie in points, the rank points will be shared (e.g., two districts tying for 3rd place will both receive 3.5 points).
*   The application must sum the rank points for each district across all eight classes.
*   The district with the lowest total rank point score wins the individual competition.

### 2.3. Relay Race Calculation

*   The application must correctly calculate the points for each relay team based on their placement, according to the following table:

| Placement | Points | Placement | Points | Placement | Points | Placement | Points | Placement | Points |
| :-------- | :----- | :-------- | :----- | :-------- | :----- | :-------- | :----- | :-------- | :----- |
| 1         | 60     | 7         | 32     | 13        | 20     | 19        | 12     | 25        | 6      |
| 2         | 50     | 8         | 30     | 14        | 18     | 20        | 11     | 26        | 5      |
| 3         | 45     | 9         | 28     | 15        | 16     | 21        | 10     | 27        | 4      |
| 4         | 41     | 10        | 26     | 16        | 15     | 22        | 9      | 28        | 3      |
| 5         | 38     | 11        | 24     | 17        | 14     | 23        | 8      | 29        | 2      |
| 6         | 35     | 12        | 22     | 18        | 13     | 24        | 7      | 30        | 1      |

*   The application must sum the points of the top five teams from each district.
*   The district with the highest total score wins the relay competition.

### 2.4. District Mapping

*   The application must be able to map the club IDs from the XML files to their respective districts.
*   This mapping will be provided in a separate configuration file (e.g., a JSON or CSV file) to allow for easy updates. The initial mapping will be:
    *   Värmland
    *   Södermanland
    *   Örebro län
    *   Östergötland

### 2.5. Output and Reporting

*   The application must display the final results for both the individual and relay races.
*   The results should be presented in a clear and easy-to-understand format, showing the final ranking of the four districts and their total scores.
*   The application should also provide a detailed breakdown of the scores for each class (for the individual race) and each team (for the relay race).

## 3. Non-Functional Requirements

### 3.1. Platform Compatibility

*   The application must be compatible with both macOS and Windows operating systems.

### 3.2. Ease of Use

*   The application should be easy to use for non-technical users.
*   It should provide a simple interface for selecting the XML result files and initiating the calculation process.

### 3.3. Dependencies

*   The application should have minimal external dependencies to ensure easy installation and setup.

### 3.4. Technology Stack

*   The application will be developed in Python, Dart, or C++, with a preference for a language that can be easily packaged into a standalone executable.

## 4. Future Considerations

*   **Web-based Interface:** A future version of the application could feature a web-based interface, allowing users to upload result files and view the results in a browser.
*   **Historical Data:** The application could be extended to store and analyze historical data from previous Distriktsmatchen competitions.
*   **Graphical Visualizations:** The results could be presented using charts and graphs to provide a more engaging user experience.
