import json
import re
import pandas as pd
import numpy as np

# Normalize Data
with open('data/topscorers.json', encoding="utf8") as data_file:
    data = json.load(data_file)


def flatten_json(y):
    out = {}

    def flatten(x, name=''):
        if type(x) is dict:
            for a in x:
                flatten(x[a], name + a + '.')
        elif type(x) is list:
            i = 0
            for a in x:
                flatten(a, name + str(i) + '.')
                i += 1
        else:
            out[name[:-1]] = x
    flatten(y)
    return out


flat = flatten_json(data)
results = pd.DataFrame()
special_cols = []

columns_list = list(flat.keys())
for item in columns_list:
    try:
        row_idx = re.findall(r'\.(\d+)\.', item)[0]
    except:
        special_cols.append(item)
        continue
    column = re.findall(r'\.\d+\.(.*)', item)[0]

    row_idx = int(row_idx)
    value = flat[item]

    results.loc[row_idx, column] = value

for item in special_cols:
    results[item] = flat[item]

topScorers = results[
    ["player.name",
     "player.age",
     "player.birth.country",
     "statistics.0.games.position",
     "statistics.0.team.name",
     "statistics.0.games.appearences",
     "statistics.0.shots.total",
     "statistics.0.shots.on",
     "statistics.0.goals.total",
     "statistics.0.goals.assists",
     "statistics.0.cards.yellow",
     "statistics.0.cards.yellowred",
     "statistics.0.cards.red"]
]


# topScorers["player.age"] = topScorers["player.age"].astype(np.int64)
# topScorers["statistics.0.games.appearences"] = topScorers["statistics.0.games.appearences"].astype(
#     np.int64)
topScorers["statistics.0.shots.total"] = topScorers["statistics.0.shots.total"].astype(
    np.int64)
topScorers["statistics.0.shots.on"] = topScorers["statistics.0.shots.on"].astype(
    np.int64)

# Percentage of shots that are on target.
topScorers["statistics.0.shots.percentage"] = round(
    ((topScorers["statistics.0.shots.on"] / topScorers["statistics.0.shots.total"]) * 100), 2)

# How many average shots are made across games.
topScorers["statistics.0.shots.avpergame"] = round(
    ((topScorers["statistics.0.shots.total"] / topScorers["statistics.0.games.appearences"])), 2)

# Percentage of goals that are made of the shots taken.
topScorers["statistics.0.goals.percentage"] = round(
    ((topScorers["statistics.0.goals.total"] / topScorers["statistics.0.shots.total"]) * 100), 2)


topScorers["statistics.0.cards.rulebreaker"] = topScorers["statistics.0.cards.yellow"] + \
    (topScorers["statistics.0.cards.yellowred"] * 1.5) + \
    (topScorers["statistics.0.cards.red"] * 2)

topScorers.to_pickle("./data/topScorersCleaned.pkl")
