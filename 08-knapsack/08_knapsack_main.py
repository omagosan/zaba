import functools

def load_data(path: str) -> tuple[list[float], list[int]]:
    ratings: list[float] = []
    durations: list[int] = []

    with open(path) as f:
        for line in f:
            parts = line.split(" ")

            rating = float(parts[0])
            ratings.append(rating)

            mins, secs = parts[1].split(":")
            duration = int(mins) * 60 + int(secs)
            durations.append(duration)

    return ratings, durations

def knapsack(idx: int, max_duration: int, ratings: list[float], durations: list[int]) -> float:
    # idx je ten prvek o kterem rozhoduji
    # return: nejlepsi suma hodnoceni

    if idx == len(ratings):
        return 0.0

    if max_duration == 0:
        return 0.0

    if durations[idx] > max_duration:
        return knapsack(idx + 1, max_duration, ratings, durations)

    left_branch_rating = ratings[idx] + knapsack(idx + 1, max_duration - durations[idx], ratings, durations)
    right_branch_rating = knapsack(idx + 1, max_duration, ratings, durations)

    return max(left_branch_rating, right_branch_rating)

@functools.cache
def knapsack_cached(idx: int, max_duration: int, ratings: tuple[float], durations: tuple[int]) -> float:
    # idx je ten prvek o kterem rozhoduji
    # return: nejlepsi suma hodnoceni

    if idx == len(ratings):
        return 0.0

    if max_duration == 0:
        return 0.0

    if durations[idx] > max_duration:
        return knapsack(idx + 1, max_duration, ratings, durations)

    left_branch_rating = ratings[idx] + knapsack(idx + 1, max_duration - durations[idx], ratings, durations)
    right_branch_rating = knapsack(idx + 1, max_duration, ratings, durations)

    return max(left_branch_rating, right_branch_rating)

if __name__ == "__main__":
    ratings, durations = load_data("08-knapsack/data/songs copy.txt")

    for r, d in zip(ratings, durations):
        print(f"{r}: {d}")

    # best_rating = knapsack(0, 4 * 60, ratings, durations)
    best_rating = knapsack_cached(0, 4 * 60, tuple(ratings), tuple(durations))
    print(best_rating)





