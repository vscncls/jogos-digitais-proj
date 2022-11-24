from datetime import datetime
import json


class Score:
    def __init__(self, coins: int, enemies_killed: int, time: datetime) -> None:
        self.coins = coins
        self.enemies_killed = enemies_killed
        self.time = time
        self.name = "Unknown"


class Scoreboard:
    __filename = "scoreboard.json"

    def __init__(self) -> None:
        self.scorebaord: list[Score] = []
        self.restore_from_file()

    def restore_from_file(self):
        try:
            with open(self.__filename) as scorebaord_file:
                scoreboard_raw = json.loads(scorebaord_file.read())
                for score in scoreboard_raw:
                    self.scorebaord.append(
                        Score(
                            score["coins"],
                            score["enemies_killed"],
                            datetime.fromisoformat(score["time"]),
                        )
                    )
        except FileNotFoundError:
            pass

    def add_score(self, score: Score):
        self.scorebaord.append(score)

    def scores(self):
        return reversed(sorted(self.scorebaord, key = lambda val: val.enemies_killed + (val.coins * 2)))

    # not ideal butttttt
    def persist(self):
        with open(self.__filename, "w") as scoreboard_file:
            raw_data = []
            for score in self.scorebaord:
                raw_data.append(
                    {
                        "coins": score.coins,
                        "enemies_killed": score.enemies_killed,
                        "time": score.time.isoformat(),
                    }
                )
            scoreboard_file.write(json.dumps(raw_data))
