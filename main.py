# Welcome to
# __________         __    __  .__                               __
# \______   \_____ _/  |__/  |_|  |   ____   ______ ____ _____  |  | __ ____
#  |    |  _/\__  \\   __\   __\  | _/ __ \ /  ___//    \\__  \ |  |/ // __ \
#  |    |   \ / __ \|  |  |  | |  |_\  ___/ \___ \|   |  \/ __ \|    <\  ___/
#  |________/(______/__|  |__| |____/\_____>______>___|__(______/__|__\\_____>
#
# This file can be a nice home for your Battlesnake logic and helper functions.
#
# To get you started we've included code to prevent your Battlesnake from moving backwards.
# For more info see docs.battlesnake.com

import random
from typing import Any, Union


# info is called when you create your Battlesnake on play.battlesnake.com
# and controls your Battlesnake's appearance
# TIP: If you open your Battlesnake URL in a browser you should see this data
def info() -> dict[str, str]:
    print("INFO")

    return {
        "apiversion": "1",
        "author": "jburkinshaw",
        "color": "#89CFF0",
        "head": "snowman",
        "tail": "weight",
    }


# start is called when your Battlesnake begins a game
def start(game_state: dict[str, Any]):
    print("GAME START")


# end is called when your Battlesnake finishes a game
def end(game_state: dict[str, Any]):
    print("GAME OVER\n")


def avoid_opponent_collisions(
    my_head: dict[str, int], opponents: list[dict], is_move_safe: dict[str, bool]
):
    """Prevent collisions with opponent snake bodies"""
    for opponent in opponents:
        opponent_body = opponent["body"]

        # Check each possible move against opponent bodies
        for move in ["up", "down", "left", "right"]:
            new_pos = get_new_head_position(my_head, move)

            # Check if new position collides with any opponent body part
            for body_part in opponent_body:
                if new_pos["x"] == body_part["x"] and new_pos["y"] == body_part["y"]:
                    is_move_safe[move] = False


def handle_head_to_head_collisions(
    my_head: dict[str, int],
    my_length: int,
    opponents: list[dict],
    is_move_safe: dict[str, bool],
):
    """Handle head-to-head collisions - logic to attack if longer, avoid if shorter or equal"""
    for opponent in opponents:
        opponent_head = opponent["body"][0]
        print(f"opponent head: {opponent_head}")
        opponent_length = len(opponent["body"])

        # Check each possible move for potential head-to-head collision
        for move in ["up", "down", "left", "right"]:
            new_pos = get_new_head_position(my_head, move)

            # Check if opponent could move to the same position
            opponent_possible_moves = get_possible_opponent_moves(opponent_head)

            if new_pos in opponent_possible_moves:
                # If we're shorter than or equal length, avoid the move
                if my_length <= opponent_length:
                    is_move_safe[move] = False
                # If we're longer, it's a safe move and we win head-to-head


def get_possible_opponent_moves(opponent_head: dict[str, int]) -> list[dict[str, int]]:
    """Get all possible positions an opponent colud move to next turn"""
    return [
        {"x": opponent_head["x"], "y": opponent_head["y"] + 1},  # up
        {"x": opponent_head["x"], "y": opponent_head["y"] - 1},  # down
        {"x": opponent_head["x"] - 1, "y": opponent_head["y"]},  # left
        {"x": opponent_head["x"] + 1, "y": opponent_head["y"]},  # right
    ]


def avoid_backwards_move(
    my_head: dict[str, int], my_neck: dict[str, int], is_move_safe: dict[str, bool]
):
    """Prevent the Battlesnake from moving backwards into its neck."""
    if my_neck["x"] < my_head["x"]:  # Neck is left of head, don't move left
        is_move_safe["left"] = False
    elif my_neck["x"] > my_head["x"]:  # Neck is right of head, don't move right
        is_move_safe["right"] = False
    elif my_neck["y"] < my_head["y"]:  # Neck is below head, don't move down
        is_move_safe["down"] = False
    elif my_neck["y"] > my_head["y"]:  # Neck is above head, don't move up
        is_move_safe["up"] = False


def avoid_walls(
    my_head: dict[str, int],
    board_width: int,
    board_height: int,
    is_move_safe: dict[str, bool],
):
    """Prevent the Battlesnake from moving out of bounds."""
    if my_head["x"] == 0:
        is_move_safe["left"] = False
    elif my_head["x"] == board_width - 1:
        is_move_safe["right"] = False

    if my_head["y"] == 0:
        is_move_safe["down"] = False
    elif my_head["y"] == board_height - 1:
        is_move_safe["up"] = False


def avoid_self_collision(
    my_head: dict[str, int],
    my_body: list[dict[str, int]],
    is_move_safe: dict[str, bool],
):
    """Prevent the Battlesnake from colliding with itself."""
    # Check UP move: new head would be at (current_x, current_y + 1)
    new_head_up = {"x": my_head["x"], "y": my_head["y"] + 1}
    if new_head_up in my_body:
        is_move_safe["up"] = False

    # Check DOWN move: new head would be at (current_x, current_y - 1)
    new_head_down = {"x": my_head["x"], "y": my_head["y"] - 1}
    if new_head_down in my_body:
        is_move_safe["down"] = False

    # Check LEFT move: new head would be at (current_x - 1, current_y)
    new_head_left = {"x": my_head["x"] - 1, "y": my_head["y"]}
    if new_head_left in my_body:
        is_move_safe["left"] = False

    # Check RIGHT move: new head would be at (current_x + 1, current_y)
    new_head_right = {"x": my_head["x"] + 1, "y": my_head["y"]}
    if new_head_right in my_body:
        is_move_safe["right"] = False


def get_safe_moves(is_move_safe: dict[str, bool]) -> list[str]:
    """Get a list of all safe moves."""
    safe_moves = []
    for move, isSafe in is_move_safe.items():
        if isSafe:
            safe_moves.append(move)
    return safe_moves


def calculate_manhattan_distance(pos1: dict[str, int], pos2: dict[str, int]) -> int:
    """Calculate Manhattan distance between two positions."""
    return abs(pos1["x"] - pos2["x"]) + abs(pos1["y"] - pos2["y"])


def find_closest_food(
    my_head: dict[str, int], food: list[dict[str, int]]
) -> Union[dict[str, int], None]:
    """Find the closest food item to the snake's head."""
    if not food:
        return None

    closest_food = None
    shortest_distance = float("inf")

    for food_item in food:
        distance = calculate_manhattan_distance(my_head, food_item)
        if distance < shortest_distance:
            shortest_distance = distance
            closest_food = food_item

    return closest_food


def get_new_head_position(my_head: dict[str, int], move: str) -> dict[str, int]:
    """Calculate the new head position for a given move."""
    if move == "up":
        return {"x": my_head["x"], "y": my_head["y"] + 1}
    elif move == "down":
        return {"x": my_head["x"], "y": my_head["y"] - 1}
    elif move == "left":
        return {"x": my_head["x"] - 1, "y": my_head["y"]}
    elif move == "right":
        return {"x": my_head["x"] + 1, "y": my_head["y"]}


def find_moves_towards_food(
    my_head: dict[str, int], safe_moves: list[str], closest_food: dict[str, int]
) -> list[str]:
    """Find moves that get the snake closer to the closest food."""
    current_distance = calculate_manhattan_distance(my_head, closest_food)
    best_moves = []

    for move in safe_moves:
        new_pos = get_new_head_position(my_head, move)
        new_distance = calculate_manhattan_distance(new_pos, closest_food)

        # If this move gets us closer to food, it's a good option
        if new_distance < current_distance:
            best_moves.append(move)

    return best_moves


# move is called on every turn and returns your next move
# Valid moves are "up", "down", "left", or "right"
# See https://docs.battlesnake.com/api/example-move for available data
def move(game_state: dict[str, Any]) -> dict[str, str]:
    is_move_safe = {"up": True, "down": True, "left": True, "right": True}

    # Extract game state information
    my_head = game_state["you"]["body"][0]  # Head
    my_neck = game_state["you"]["body"][1]  # Neck
    my_body = game_state["you"]["body"]
    my_length = len(my_body)
    my_health = game_state["you"]["health"]
    board_width = game_state["board"]["width"]
    board_height = game_state["board"]["height"]
    food = game_state["board"]["food"]
    opponents = [
        snake
        for snake in game_state["board"]["snakes"]
        if snake["id"] != game_state["you"]["id"]
    ]

    # Apply safety checks
    avoid_backwards_move(my_head, my_neck, is_move_safe)
    avoid_walls(my_head, board_width, board_height, is_move_safe)
    avoid_self_collision(my_head, my_body, is_move_safe)
    avoid_opponent_collisions(my_head, opponents, is_move_safe)
    handle_head_to_head_collisions(my_head, my_length, opponents, is_move_safe)
    print(f"food: {food}")

    # Get safe moves
    safe_moves = get_safe_moves(is_move_safe)

    # Handle case with no safe moves
    if len(safe_moves) == 0:
        print(f"MOVE {game_state['turn']}: No safe moves detected! Moving down")
        return {"move": "down"}
    # If there's no food on the board, just pick a random safe move
    # Only pursue food if health is less than 50
    health_threshold = 90
    if my_health < health_threshold and len(food) > 0:
        # Find the closest food and moves towards it
        closest_food = find_closest_food(my_head, food)
        best_moves = find_moves_towards_food(my_head, safe_moves, closest_food)

        # Choose the best move (prioritizing food) or fallback to safe moves
        if len(best_moves) > 0:
            next_move = random.choice(
                best_moves
            )  # Random choice if multiple moves are equally good
            print(
                f"MOVE {game_state['turn']}: Health {my_health} < {health_threshold}, moving towards food at {closest_food}: {next_move}"
            )
        else:
            next_move = random.choice(
                safe_moves
            )  # No move gets us closer, pick random safe move
            print(
                f"MOVE {game_state['turn']}: Health {my_health} < {health_threshold}, but no move gets closer to food, random safe move: {next_move}"
            )
    else:
        # Health is threshold or above, or no food available - just pick a random safe move
        next_move = random.choice(safe_moves)
        if my_health >= health_threshold:
            print(
                f"MOVE {game_state['turn']}: Health {my_health} >= {health_threshold}, ignoring food and making random safe move: {next_move}"
            )
        else:
            print(
                f"MOVE {game_state['turn']}: No food available, random safe move: {next_move}"
            )

    print(f"MOVE {game_state['turn']}: {next_move}")
    return {"move": next_move}


# Start server when `python main.py` is run
if __name__ == "__main__":
    from server import run_server

    run_server({"info": info, "start": start, "move": move, "end": end})
