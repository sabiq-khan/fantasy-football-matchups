#!/usr/bin/env python3
from typing import List, Tuple
import random
import copy
from csv import DictWriter
from itertools import permutations


# CSV
CSV_COLUMNS: List[str] = ["WEEK", "TEAM1", "TEAM2"]


class MatchupCreator:
    def __init__(self, west_division: List[str], east_division: List[str], south_division: List[str], interdivisional_weeks: List[int], intradivisional_weeks: List[int], playoff_weeks: List[int]):
        # Keeping this list 1-indexed for simplicity so week == index
        self.west_division: List[str] = west_division
        self.east_division: List[str] = east_division
        self.south_division: List[str] = south_division
        self.interdivisional_weeks: List[int] = interdivisional_weeks
        self.intradivisional_weeks: List[int] = intradivisional_weeks
        self.playoff_weeks: List[int] = playoff_weeks

        self.all_division_teams: List[str] = (
            self.west_division + self.east_division + self.south_division)
        random.shuffle(self.all_division_teams)
        self.all_possible_matchups: List[Tuple[str]] = list(
            permutations(self.all_division_teams, 2))

        # Keeping this list 1-indexed for simplicity so week == index
        self.all_seasonal_matchups: List[List[Tuple[str]]] = [
            [] for i in range(18)]

    def already_playing_this_week(self, current_week: int, team: str) -> bool:
        for matchup in self.all_seasonal_matchups[current_week]:
            if team in matchup:
                return True

        return False

    def intradivisional_matchup_exists_twice(self, current_week: int, team1: str, team2: str) -> bool:
        count: int = 0
        for week in self.intradivisional_weeks:
            if (week > current_week):
                break
            if (week <= current_week) and (((team1, team2) in self.all_seasonal_matchups[week]) or ((team2, team1) in self.all_seasonal_matchups[week])):
                count += 1
            if count == 2:
                return True

        return False

    def interdivisional_matchup_exists(self, current_week: int, team1: str, team2: str) -> bool:
        for week in self.interdivisional_weeks:
            if (week > current_week):
                break
            if (week <= current_week) and (((team1, team2) in self.all_seasonal_matchups[week]) or ((team2, team1) in self.all_seasonal_matchups[week])):
                return True

        return False

    def teams_in_different_divisions(self, team1: str, team2: str) -> bool:
        if ((team1 in self.west_division) and (team2 in self.west_division)) or ((team1 in self.east_division) and (team2 in self.east_division)) or ((team1 in self.south_division) and (team2 in self.south_division)):
            return False

        return True

    def is_valid_interdivisional_matchup(self, week: int, team1: str, team2: str):
        if (team1 != team2) and (not self.already_playing_this_week(week, team1)) and (not self.already_playing_this_week(week, team2)) and (self.teams_in_different_divisions(team1, team2)) and (not self.interdivisional_matchup_exists(week, team1, team2)):
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

    def create_interdivisional_matchups(self, week: int):
        while len(self.all_seasonal_matchups[week]) < 6:
            self.all_seasonal_matchups[week] = []
            random.shuffle(self.all_possible_matchups)
            for matchup in self.all_possible_matchups:
                team1: str = matchup[0]
                team2: str = matchup[1]
                if self.is_valid_interdivisional_matchup(week, team1, team2):
                    self.all_seasonal_matchups[week].append(matchup)

    def create_all_seasonal_matchups(self):
        for week in range(1, 18):
            if week in self.interdivisional_weeks:
                self.create_interdivisional_matchups(week)
            elif week in self.intradivisional_weeks:
                self.create_intradivisional_matchups(week, self.west_division)
                self.create_intradivisional_matchups(week, self.east_division)
                self.create_intradivisional_matchups(week, self.south_division)

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
