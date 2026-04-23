import json
import random
from typing import Dict, List

POINTS_TABLE = [25, 18, 15, 12, 10, 8, 6, 4, 2, 1]

def load_season_data(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)

def calculate_driver_score(driver: Dict, team_perf: int, track: Dict, randomness: float):

    driver_base = (
            driver["experience"] * 0.15 +
            driver["racecraft"]  * 0.25 +
            driver["awareness"]  * 0.10 +
            driver["pace"]       * 0.50
    )

    team_factor = team_perf * 0.5
    track_factor = track["track_pace_factor"] * 5
    random_factor = random.uniform(-1, 1) * (randomness * 15)

    return driver_base + team_factor + track_factor + random_factor

def simulate_race(drivers: List[Dict], teams: Dict[str, int], track: Dict, randomness: float, dnf_rate: float):
    results = []

    for d in drivers:
        dnf_chance = dnf_rate + (100 - d["awareness"]) * 0.0005
        dnf = random.random() < dnf_chance

        if dnf:
            score = -9999
        else:
            score = calculate_driver_score(d, teams[d["team"]], track, randomness)

        results.append({
            "name": d["name"],
            "team": d["team"],
            "score": score,
            "dnf": dnf
        })

    results.sort(key=lambda x: x["score"], reverse=True)
    return results

def apply_points(standings: Dict, results: List[Dict]):
    for i, result in enumerate(results):
        points = POINTS_TABLE[i] if i < len(POINTS_TABLE) and not result["dnf"] else 0
        standings[result["name"]] += points

def apply_constructor_points(constructors: Dict, results: List[Dict]):
    for i, result in enumerate(results):
        if i < len(POINTS_TABLE) and not result["dnf"]:
            constructors[result["team"]] += POINTS_TABLE[i]

def print_table(title: str, data: Dict):
    print("\n" + title)
    print("-" * len(title))
    print(f"{'Position':<10} {'Name/Team':<25} {'Points':<10}")

    sorted_items = sorted(data.items(), key=lambda x: x[1], reverse=True)

    for x, (name, pts) in enumerate(sorted_items, 1):
        print(f"{x:<10} {name:<25} {pts:<10}")

def main():
    filepath = "season_data.json"  # Make sure this file is in the same folder

    try:
        data = load_season_data(filepath)
    except FileNotFoundError:
        print(f"Could not find '{filepath}'. Make sure it's in the same folder as this script.")
        return

    drivers = data["drivers"]
    teams = data["teams"]
    tracks = data["tracks"]
    settings = data["settings"]

    driver_points = {d["name"]: 0 for d in drivers}
    constructor_points = {team: 0 for team in teams}

    for track in tracks:
        results = simulate_race(
            drivers,
            teams,
            track,
            randomness=settings["randomness"],
            dnf_rate=settings["dnf_base_rate"]
        )
        apply_points(driver_points, results)
        apply_constructor_points(constructor_points, results)

    print_table("Driver Standings", driver_points)
    print_table("Constructor Standings", constructor_points)

if __name__ == "__main__":
    main()