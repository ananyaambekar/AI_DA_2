import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Arrow
import time

class PuzzleVisualizer:
    def __init__(self):
        self.goal_board = np.array([
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 0]
        ])
        
    def manhattan_distance(self, current, goal):
        distance = 0
        for i in range(1, 9):  # Skip empty tile (0)
            curr_pos = np.where(current == i)
            goal_pos = np.where(goal == i)
            distance += abs(curr_pos[0][0] - goal_pos[0][0]) + \
                       abs(curr_pos[1][0] - goal_pos[1][0])
        return distance

    def get_possible_moves(self, board):
        moves = []
        zero_pos = np.where(board == 0)
        row, col = zero_pos[0][0], zero_pos[1][0]
        
        for dr, dc in [(-1,0), (1,0), (0,-1), (0,1)]:
            new_row, new_col = row + dr, col + dc
            if 0 <= new_row < 3 and 0 <= new_col < 3:
                new_board = board.copy()
                new_board[row, col], new_board[new_row, new_col] = \
                    new_board[new_row, new_col], new_board[row, col]
                score = self.manhattan_distance(new_board, self.goal_board)
                moves.append((score, new_board, (new_row, new_col)))
        return moves

    def visualize_board(self, board, title, show_moves=True):
        fig, ax = plt.subplots(figsize=(8, 8))
        ax.set_title(title, pad=20, fontsize=14)
        
        # Draw the grid
        for i in range(3):
            for j in range(3):
                ax.add_patch(Rectangle((j, 2-i), 1, 1, fill=False))
                if board[i, j] != 0:
                    ax.text(j + 0.5, 2-i + 0.5, str(board[i, j]), 
                           ha='center', va='center', fontsize=20)
                else:
                    ax.add_patch(Rectangle((j, 2-i), 1, 1, fill=True, 
                               color='lightgray'))
        
        if show_moves:
            # Show possible moves and their Manhattan distances
            moves = self.get_possible_moves(board)
            current_score = self.manhattan_distance(board, self.goal_board)
            ax.text(-0.5, 3.2, f'Current Manhattan Distance: {current_score}', 
                   fontsize=12)
            
            for score, new_board, (new_row, new_col) in moves:
                zero_pos = np.where(board == 0)
                start_y, start_x = 2-zero_pos[0][0], zero_pos[1][0]
                end_y, end_x = 2-new_row, new_col
                
                # Draw arrows for possible moves
                dx = end_x - start_x
                dy = end_y - start_y
                arrow_color = 'red' if score > current_score else \
                            ('yellow' if score == current_score else 'green')
                ax.add_patch(Arrow(start_x + 0.5, start_y + 0.5, dx*0.4, dy*0.4,
                                 width=0.2, color=arrow_color))
                ax.text(end_x + 0.5, end_y + 0.2, f'MD: {score}', 
                       ha='center', va='center', fontsize=10)

        ax.set_xlim(-0.5, 3.5)
        ax.set_ylim(-0.5, 3.5)
        ax.axis('off')
        plt.tight_layout()
        return fig

def demonstrate_failures():
    visualizer = PuzzleVisualizer()
    
    # Local Maximum Example
    local_max = np.array([
        [1, 2, 3],
        [4, 5, 6],
        [0, 7, 8]
    ])
    fig1 = visualizer.visualize_board(
        local_max,
        'Local Maximum Example\nAny move increases Manhattan distance'
    )
    
    # Plateau Example
    plateau = np.array([
        [1, 2, 3],
        [4, 5, 0],
        [7, 8, 6]
    ])
    fig2 = visualizer.visualize_board(
        plateau,
        'Plateau Example\nAll moves result in same Manhattan distance'
    )
    
    # Misleading Heuristic Example
    misleading = np.array([
        [1, 2, 3],
        [8, 0, 4],
        [7, 6, 5]
    ])
    fig3 = visualizer.visualize_board(
        misleading,
        'Misleading Heuristic Example\nReaching goal requires temporarily increasing distance'
    )
    
    plt.show()

if __name__ == "__main__":
    demonstrate_failures()