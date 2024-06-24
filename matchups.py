#!/usr/bin/env python3
from typing import List, Tuple
import random
import copy
from csv import DictWriter

# DIVISIONS
WEST_DIVISION: List[str] = ["49ers", "Seahawks", "Rams", "Cardinals"]
EAST_DIVISION: List[str] = ["Buccaneers", "Saints", "Falcons", "Panthers"]
SOUTH_DIVISION: List[str] = ["Cowboys", "Eagles", "Giants", "Commanders"]

# WEEKS
INTERDIVISIONAL_WEEKS: List[int] = [1, 2, 4, 6, 8, 10, 12, 14]
INTRADIVISIONAL_WEEKS: List[int] = [3, 5, 7, 9, 11, 13]
PLAYOFF_WEEKS: List[int] = [15, 16, 17]

# CSV
CSV_COLUMNS: List[str] = ["WEEK", "TEAM1", "TEAM2"]


class MatchupCreator:
    def __init__(self):
        # Keeping this list 1-indexed for simplicity so week == index
        self.all_seasonal_matchups: List[List[Tuple[str]]] = [[]]

    def intradivisional_matchup_exists_twice(self, current_week: int, team1: str, team2: str) -> bool:
        count: int = 0
        for week in INTRADIVISIONAL_WEEKS:
            if (week > current_week):
                break
            if (week <= current_week) and (((team1, team2) in self.all_seasonal_matchups[week]) or ((team2, team1) in self.all_seasonal_matchups[week])):
                count += 1
            if count == 2:
                return True

        return False

    def interdivisional_matchup_exists(self, current_week: int, team1: str, team2: str) -> bool:
        for week in INTERDIVISIONAL_WEEKS:
            if (week > current_week):
                break
            if (week <= current_week) and (((team1, team2) in self.all_seasonal_matchups[week]) or ((team2, team1) in self.all_seasonal_matchups[week])):
                return True

        return False

    def create_intradivisional_matchups(self, week: int, division: List[str]):
        teams: List[str] = copy.deepcopy(division)
        while len(teams) > 0:
            match_index: int = random.randrange(1, len(teams))
            team1: str = teams[0]
            team2: str = teams[match_index]
            if not self.intradivisional_matchup_exists_twice(current_week=week, team1=team1, team2=team2):
                matchup: Tuple[str] = (team1, team2)
                self.all_seasonal_matchups[week].append(matchup)
                teams.pop(match_index)
                teams.pop(0)

    def create_interdivisional_matchups(self, week: int, west_division: List[str] = WEST_DIVISION, east_division: List[str] = EAST_DIVISION, south_division: List[str] = SOUTH_DIVISION):
        west_teams: List[str] = copy.deepcopy(west_division)
        east_teams: List[str] = copy.deepcopy(east_division)
        south_teams: List[str] = copy.deepcopy(south_division)

        league: List[List[str]] = [west_teams, east_teams, south_teams]

        while (len(league[0]) > 0) or (len(league[1]) > 0) or (len(league[2]) > 0):
            division1: List[str] = league[0]
            division2: List[str] = league[1]

            team1_index: int = random.randrange(0, len(division1))
            team1: str = division1[team1_index]

            team2_index: int = random.randrange(0, len(division2))
            team2: str = division2[team2_index]

            if not self.interdivisional_matchup_exists(current_week=week, team1=team1, team2=team2):
                matchup: Tuple[str] = (team1, team2)
                self.all_seasonal_matchups[week].append(matchup)

            division1.pop(team1_index)
            division2.pop(team2_index)

            league = league[1:] + league[:1]

    def create_all_seasonal_matchups(self):
        for week in range(1, 18):
            self.all_seasonal_matchups.append([])
            if week in INTERDIVISIONAL_WEEKS:
                self.create_interdivisional_matchups(week)
            if week in INTRADIVISIONAL_WEEKS:
                self.create_intradivisional_matchups(week, WEST_DIVISION)
                self.create_intradivisional_matchups(week, EAST_DIVISION)
                self.create_intradivisional_matchups(week, SOUTH_DIVISION)

    def write_matchups_to_csv(self):
        with open("matchups.csv", "w", newline="") as csvfile:
            writer: DictWriter = DictWriter(f=csvfile, fieldnames=CSV_COLUMNS)
            writer.writeheader()
            for week in range(1, 18):
                for matchup in self.all_seasonal_matchups[week]:
                    writer.writerow(
                        {
                            CSV_COLUMNS[0]: f"WEEK {week}",
                            CSV_COLUMNS[1]: matchup[0],
                            CSV_COLUMNS[2]: matchup[1]
                        }
                    )


def main():
    matchup_creator: MatchupCreator = MatchupCreator()
    matchup_creator.create_all_seasonal_matchups()
    matchup_creator.write_matchups_to_csv()


if __name__ == "__main__":
    main()
