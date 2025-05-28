# 경로 추천 함수 (룰 기반)
def recommend_best_path(paths, user_type):
    # {"slope": ,
    # "sidewalk": ,
    # "stairs": ,
    # "safety": ,
    # "elevator": },
    weights = {
        #검증 필요...
        "elderly": {"slope": 3, "sidewalk": 2, "stairs": 5, "safety": 4},
        "wheelchair": {"slope": 4, "sidewalk": 5, "stairs": 10, "safety": 3},
        "stroller": {"slope": 3, "sidewalk": 4, "stairs": 7, "safety": 3},
    }
    w = weights[user_type]
    best = None
    best_score = -9999

    for p in paths:
        score = (
            -p["slope"] * w["slope"]
            + (w["sidewalk"] if p["sidewalk"] else 0)
            - (w["stairs"] if p["stairs"] else 0)
            + p["safety_score"] * w["safety"]
        )
        if score > best_score:
            best = p
            best_score = score

    return best