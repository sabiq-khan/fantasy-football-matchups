## Fantasy Football Matchup Script
This script creates random matchups of 4 teams from 3 fantasy football divisions.

The following rules are taken into account:
- During weeks 1, 2, 4, 6, 8, 10, 12, and 14, only teams from different divisions are matched up. These matchups can only occur once the entire season.
- During weeks 3, 5, 7, 9, 11, and 13, only teams from the same division are matched up. These matchups can occur only twice the entire season.

## Installation
1) `git clone` this repo, download it as a `.zip`, or download the `matchups.py` file.
2) Ensure you have Python 3.10+ installed.

## Usage
1) Navigate to the directory containing the `matchups.py` script and run `chmod u+x matchups.py`.
2) Run the script with `./matchups.py`.

The output will be written to a `matchups.csv` file in the same directory as the script. This file can be opened in Excel on Windows, Numbers on Mac, and LibreOffice Calc on Linux for ease of viewing.

## Known Issues
- For 3 sets of 4 teams, 48 unique interdivisional matchups should be possible, yet signficantly fewer than this are produced.
