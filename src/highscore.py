import hjson


def update_highscore_file(path: str, score: int) -> None:
    with open(path, "w") as f:
        hjson.dump({'highscore': score}, f, ensure_ascii=False, indent=4)