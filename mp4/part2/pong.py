import random
import math

ball_x = 0.5
ball_y = 0.5
velocity_x = 0.03
velocity_y = 0.01
paddle_height = 0.2
paddle_y = (0.5 - paddle_height/2)
paddle_x = 1
num_bounces = 0
game_running = True
num_games = 0

board_state = [ball_x, ball_y, velocity_x, velocity_y, paddle_y]
game_board = [[" " for i in range(12)] for j in range(12)]

# Variables for Q learning
learning_rate = 0.1
discount_factor = 0.5
r_prime = 0
# Prev State, Action, and Reward
s = None
a = None
r = 0

Q = {}
N = {}


def update_game():
    # has the agent tried to move the paddle out of bounds?
    global paddle_y
    global ball_x
    global ball_y
    global velocity_x
    global velocity_y
    if paddle_y < 0:
        paddle_y = 0
    if (paddle_y + paddle_height) > 1:
        paddle_y = 1 - paddle_height

    # move the ball
    ball_x += velocity_x
    ball_y += velocity_y

    # has the ball hit the left wall?
    if ball_x < 0:
        ball_x = -ball_x
        velocity_x = -velocity_x

    # has the ball hit the top/bottom walls?
    if ball_y < 0:
        ball_y = -ball_y
        velocity_y = -velocity_y
    if ball_y > 1:
        ball_y = 2 - ball_y
        velocity_y = -velocity_y

    # has the ball hit the paddle?
    if ball_x >= 1 and (ball_y > paddle_y and ball_y < (paddle_y + paddle_height)):
        global num_bounces
        num_bounces += 1
        ball_x = 2 * paddle_x - ball_x
        rand_U = random.uniform(-0.015, 0.015)
        rand_V = random.uniform(-0.03, 0.03)

        velocity_x = -velocity_x + rand_U
        velocity_y = velocity_y + rand_V
        global r_prime
        r_prime = 1

    elif ball_x >= 1:
        global game_running
        game_running = False

    # check velocity requirements
    if math.fabs(velocity_x) < 0.03:
        if velocity_x < 0:
            velocity_x = -0.03
        else:
            velocity_x = 0.03

    if math.fabs(velocity_y) > 1:
        if velocity_y < 0:
            velocity_y = -1
        else:
            velocity_y = 1

    if math.fabs(velocity_x) > 1:
        if velocity_x < 0:
            velocity_x = -1
        else:
            velocity_x = 1


def update_game_state():
    board_state[0] = int(ball_x * 12)
    board_state[1] = int(ball_y * 12)
    if velocity_x < 0:
        board_state[2] = -1
    else:
        board_state[2] = 1
    if math.fabs(velocity_y) < 0.015:
        board_state[3] = 0
    elif velocity_y < 0:
        board_state[3] = -1
    else:
        board_state[3] = 1

    if paddle_y == (1-paddle_height):
        board_state[4] = 11
    else:
        board_state[4] = int(12 * paddle_y/(1 - paddle_height))

    board_x = board_state[0]
    board_y = board_state[1]

    global game_board
    game_board = [[" " for i in range(12)] for j in range(12)]
    print("Board x: " + str(board_x))
    print("Board y: " + str(board_y))
    game_board[board_y][board_x] = "O"


def print_board():
    print("========================== Board ===========================")
    for row in game_board:
        print(row)
    print("============================================================")
    print("\n")


def init_tables():
    for i in range(12):
        for j in range(12):
            for x in range(2):
                # +1, -1
                # 0,   1
                for y in range(3):
                    # +1, 0, -1
                    # 0,  1,  2
                    for paddle_pos in range(12):
                        for action in range(3):
                            # Actions
                            # -1, 0, 1
                            #  0, 1, 2
                            hashed_tuple = hash((i, j, x, y, paddle_pos, action))
                            Q[hashed_tuple] = 0
                            N[hashed_tuple] = 0
    terminal_state = hash((-1, -1, -1, -1, -1, -1, -1))
    Q[terminal_state] = -1


def q_learning_algo(s_prime):
    print(s_prime)
    global paddle_x
    global ball_x
    global s
    global a
    global r
    global r_prime
    # Terminal State Check
    if ball_x > paddle_x:
        prev_state_hash = hash(tuple(list(s).append(a)))
        Q[prev_state_hash] = r_prime
    if s is not None:
        prev_state_hash = hash(tuple(list(s).append(a)))
        N[prev_state_hash] += 1
        possible_actions = []
        for i in range(3):
            action = hash(tuple(list(s_prime).append(i)))
            possible_actions.append(Q[action])
        Q[prev_state_hash] = Q[prev_state_hash] + (learning_rate * N[prev_state_hash]) * (r + discount_factor * max(possible_actions) - Q[prev_state_hash])
    s = s_prime
    final_actions = []
    for i in range(3):
        action = hash(tuple(list(s_prime).append(i)))
        final_actions.append(Q[action])
    a = final_actions.index(max(final_actions))
    update_learning_decay()
    r = r_prime
    r_prime = 0
    return a


def update_learning_decay():
    # C / (C + N(s, a)
    global s
    global a
    global learning_rate
    current_state_action = hash(tuple(list(s).append(a)))
    learning_rate = learning_rate / (N[current_state_action] * learning_rate)


def reset_states():
    global ball_x
    global ball_y
    global velocity_x
    global velocity_y
    global paddle_x
    global paddle_height
    global paddle_y
    global num_bounces
    global game_running
    global num_games
    ball_x = 0.5
    ball_y = 0.5
    velocity_x = 0.03
    velocity_y = 0.01
    paddle_height = 0.2
    paddle_y = (0.5 - paddle_height / 2)
    paddle_x = 1
    num_bounces = 0
    game_running = True
    num_games += 1


init_tables()
while game_running:
    update_game_state()
    current_state = tuple(board_state)
    print(current_state)
    move_paddle = q_learning_algo(current_state)
    if move_paddle == 0:
        print("Going Down")
        paddle_y -= 0.04
    elif move_paddle == 1:
        print("Staying")
    else:
        print("Going Up")
        paddle_y += 0.04
    update_game()
    if game_running:
        print_board()
    else:
        print("Game Over!")
        #reset_states()
