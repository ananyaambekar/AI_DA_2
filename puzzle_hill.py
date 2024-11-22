import numpy as np

# Define puzzle state
class PuzzleState:
    def __init__(self, board):
        self.board = np.array(board)
        self.size = len(board)
    
    def find_zero(self):
        return np.argwhere(self.board == 0)[0]

    def move(self, direction):
        zero_pos = self.find_zero()
        new_board = self.board.copy()
        if direction == 'up' and zero_pos[0] > 0:
            new_board[zero_pos[0], zero_pos[1]], new_board[zero_pos[0] - 1, zero_pos[1]] = new_board[zero_pos[0] - 1, zero_pos[1]], new_board[zero_pos[0], zero_pos[1]]
        elif direction == 'down' and zero_pos[0] < self.size - 1:
            new_board[zero_pos[0], zero_pos[1]], new_board[zero_pos[0] + 1, zero_pos[1]] = new_board[zero_pos[0] + 1, zero_pos[1]], new_board[zero_pos[0], zero_pos[1]]
        elif direction == 'left' and zero_pos[1] > 0:
            new_board[zero_pos[0], zero_pos[1]], new_board[zero_pos[0], zero_pos[1] - 1] = new_board[zero_pos[0], zero_pos[1] - 1], new_board[zero_pos[0], zero_pos[1]]
        elif direction == 'right' and zero_pos[1] < self.size - 1:
            new_board[zero_pos[0], zero_pos[1]], new_board[zero_pos[0], zero_pos[1] + 1] = new_board[zero_pos[0], zero_pos[1] + 1], new_board[zero_pos[0], zero_pos[1]]
        return PuzzleState(new_board)

    def __eq__(self, other):
        return np.array_equal(self.board, other.board)

    def __hash__(self):
        return hash(self.board.tobytes())

    def __repr__(self):
        return str(self.board)

# Define heuristic functions
def manhattan_distance(state, goal):
    distance = 0
    for x in range(state.size):
        for y in range(state.size):
            value = state.board[x, y]
            if value != 0:
                goal_pos = np.argwhere(goal.board == value)[0]
                distance += abs(x - goal_pos[0]) + abs(y - goal_pos[1])
    return distance

def misplaced_tiles(state, goal):
    return np.sum(state.board != goal.board) - 1

# Implement hill climbing
def hill_climbing(start, goal, heuristic):
    current = start
    steps = 0
    print("Initial State:")
    print(current)
    print("\nStarting Hill Climbing...\n")

    while current != goal:
        neighbors = [current.move('up'), current.move('down'), current.move('left'), current.move('right')]
        neighbors = [neighbor for neighbor in neighbors if neighbor.board.tolist() != current.board.tolist()]
        if not neighbors:
            break

        neighbor = min(neighbors, key=lambda state: heuristic(state, goal))
        if heuristic(neighbor, goal) >= heuristic(current, goal):
            break

        current = neighbor
        steps += 1

        print(f'Step {steps}:')
        print(current)
        print()

    print("Hill Climbing Completed.")
    return current, steps

# Test different initial configurations
def test_hill_climbing(initial_board, goal_board, heuristic):
    start_state = PuzzleState(initial_board)
    goal_state = PuzzleState(goal_board)

    print(f"Testing with initial configuration:\n{start_state}\n")

    final_state, total_steps = hill_climbing(start_state, goal_state, heuristic)
    if final_state == goal_state:
        print('Final State:')
        print(final_state)
        print(f'Total Steps: {total_steps}\n')
        print('-' * 40)
    else:
        print('Failed to reach the goal state.\n')
        print('-' * 40)

# Different initial configurations
initial_boards = [
    [
        [1, 2, 3],
        [4, 0, 5],
        [7, 8, 6]
    ],
    [
        [1, 2, 3],
        [4, 5, 6],
        [0, 7, 8]
    ],
    [
        [1, 2, 3],
        [0, 5, 6],
        [4, 7, 8]
    ],
    [
        [1, 2, 3],
        [7, 0, 6],
        [5, 4, 8]
    ]
]

goal_board = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 0]
]

print("Using Manhattan Distance Heuristic:\n")
for initial_board in initial_boards:
    test_hill_climbing(initial_board, goal_board, manhattan_distance)

print("Using Misplaced Tiles Heuristic:\n")
for initial_board in initial_boards:
    test_hill_climbing(initial_board, goal_board, misplaced_tiles)
