from datetime import datetime
import requests
import json


with open("leaderboard.json", "r", encoding="utf-8") as f:
    players_levels = json.load(f)


BASE_URL = "https://api.demonlist.org/level/classic/list"
response = requests.get(BASE_URL)
if response.status_code != 200:
    print(f"Error {response.status_code}: {response.text}")

data = response.json().get("data", [])
if not data:
    print("No levels found.")

all_levels = response.json().get("data", []).get("levels", [])

with open("top.txt", "w", encoding="utf-8") as f:
    f.write(str(all_levels))

all_levels = [lvl for lvl in all_levels if lvl.get("id") != 2299]

def get_pos(level_name: str) -> int:
    for lvl in all_levels:
        if lvl["name"].lower() == level_name.lower():
            return lvl.get("placement")
    print(f"!!! Level doesnt exist : {level_name}")
    raise

def sort_levels(levels: list[str]) -> list[str]:
    return sorted(levels, key=get_pos)

def sort_levels_dict(levels: dict[str, str]) -> dict[str, str]:
    return dict(sorted(levels.items(), key=lambda item: get_pos(item[0])))

def hardest_level_pos(levels: list[str] | dict[str, str]) -> int:
    if isinstance(levels, dict):
        return min(get_pos(lvl) for lvl in levels.keys())
    else:
        return min(get_pos(lvl) for lvl in levels)

players_levels_sorted = dict(
    sorted(
        players_levels.items(),
        key=lambda item: hardest_level_pos(item[1])
    )
)

final_message = ""
place_emojis = ["1. 🥇", "2. 🥈", "3. 🥉"]

rank = 1

for player, levels in players_levels_sorted.items():

    if isinstance(levels, dict):
        levels = sort_levels_dict(levels)
    else:
        levels = sort_levels(levels)

    emoji = place_emojis[rank-1] if rank <= 3 else f"{rank}."

    line = f"{emoji} {player} - "

    formatted_levels = []

    if isinstance(levels, dict):
        for lvl, mode in levels.items():
            pos = get_pos(lvl)
            entry = f"{lvl} (#{pos})"
            if mode == "mobile":
                entry = f"__{entry}__"
            formatted_levels.append(entry)
    else:
        for lvl in levels:
            pos = get_pos(lvl)
            formatted_levels.append(f"{lvl} (#{pos})")

    line += ", ".join(formatted_levels)
    final_message += line + "\n"
    rank += 1

result = f"""
# Server Leaderbord by Hardest
{final_message}
{datetime.now().strftime("%d/%m/%y")} positions from https://demonlist.org/
__mobile 60Hz completions underlined__

(extreme demons only)
(you need to have a recording)
(tell me if i forgot something)
(message cuts because of discord's length limit)
"""  # <@&1401222222668107948> <@&1401221967146651648>

print(result)

with open("result.txt", "w", encoding="utf-8") as f:
    f.write(result)
