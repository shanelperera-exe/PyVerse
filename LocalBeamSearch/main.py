import random

def local_beam_search(initial_states, k, max_iters, objective_fn):
    """
    initial_states: list of k randomly generated starting positions
    k: the beam width (number of states to keep)
    objective_fn: the function we are trying to maximize
    """
    current_states = initial_states

    for iteration in range(max_iters):
        all_successors = []

        # Generate, evaluate and pool neighbours
        for state in current_states:
            for _ in range(5):
                neighbor = state + random.uniform(-10, 10)
                fit = objective_fn(neighbor)
                all_successors.append((neighbor, fit))

        # Sort by fitness from highest to lowest
        all_successors.sort(key=lambda x: x[1], reverse=True)

        # Keep the best k states
        current_states = [item[0] for item in all_successors[:k]]

    return max(current_states, key=objective_fn)


# =====================================================================
# LOCAL TEST RUNNER
# =====================================================================
if __name__ == "__main__":
    random.seed(42)

    # Parabola with maximum at x = 5
    def objective(x):
        return -(x - 5) ** 2 + 100

    initial_states = [-20, 0, 20]
    k = 3
    max_iters = 100

    best_state = local_beam_search(
        initial_states,
        k,
        max_iters,
        objective
    )

    best_fitness = objective(best_state)

    print("Best state:", best_state)
    print("Best fitness:", best_fitness)
    print("Test completed successfully!")

