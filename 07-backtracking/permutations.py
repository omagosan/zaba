def permutations(n: int) -> None:
    """Vypise permutace n prvku - ilustrace backtrackingu."""
    solution_vector = [-1] * n
    _permutations_backtracking(solution_vector, 0)

def _permutations_backtracking(solution_vector: list[int], k: int) -> None:
    n = len(solution_vector)
    if k == n:
        print(solution_vector)
        return
    for value in range(n):
        if value in solution_vector:
            continue
        solution_vector[k] = value
        _permutations_backtracking(solution_vector, k + 1)
        solution_vector[k] = -1

permutations(5)
