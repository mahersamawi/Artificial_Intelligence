import random
import math

ball_x = 0.5
ball_y = 0.5
velocity_x = 0.03
velocity_y = 0.01
paddle_height = 0.2
paddle_y = (0.5 - paddle_height/2)
paddle_x = 1
game_running = True
num_games = 0

max_bounces = 0
num_bounces = 0
total_bounces = 0

board_state = [ball_x, ball_y, velocity_x, velocity_y, paddle_y]
game_board = [[" " for i in range(12)] for j in range(12)]

# Variables for Q learning
learning_rate = 1
discount_factor = 0.9
r_prime = 0
learning_rate_const = 1

# Prev State, Action, and Reward
s = None
a = None
r = 0

Q = {}
N = {}

# variables for exploration function
r_plus = 1 # "optimistic estimate of the best possible reward obtainable in any state"
Ne = 20 # make the agent try each action-pair state at least Ne times

# debugging flag
debugging = False
def update_game():
    # has the agent tried to move the paddle out of bounds?
    global paddle_y
    global ball_x
    global ball_y
    global velocity_x
    global velocity_y
    global num_bounces
    global r_prime
    global debugging

    if paddle_y < 0:
        if debugging == True:
            print("Paddle went too high")
        paddle_y = 0
    if (paddle_y + paddle_height) > 1:
        if debugging == True:
            print("Paddle went too low")
        paddle_y = 1 - paddle_height

    # move the ball
    ball_x += velocity_x
    ball_y += velocity_y

    # has the ball hit the left wall?
    if ball_x < 0:
        if debugging == True:
            print("Ball bounced off the left wall")
        ball_x = -ball_x
        velocity_x = -velocity_x

    # has the ball hit the top/bottom walls?
    if ball_y < 0:
        if debugging == True:
            print("Ball bounced off the top wall")
        ball_y = -ball_y
        velocity_y = -velocity_y
    if ball_y > 1:
        if debugging == True:
            print("Ball bounced off the bottom wall")
        ball_y = 2 - ball_y
        velocity_y = -velocity_y

    # has the ball hit the paddle?
    if ball_x >= 1 and (ball_y > paddle_y and ball_y < (paddle_y + paddle_height)):
        if debugging == True:
            print("Ball hit the paddle!")
        num_bounces += 1
        ball_x = 2 * paddle_x - ball_x
        rand_U = random.uniform(-0.015, 0.015)
        rand_V = random.uniform(-0.03, 0.03)

        velocity_x = -velocity_x + rand_U
        velocity_y = velocity_y + rand_V
        r_prime = 1
    elif ball_x >  1:
        r_prime = -1

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
            # From -1 to 0
            velocity_x = -1
        else:
            velocity_x = 1


def update_game_state():
    global board_state
    board_state[0] = int(ball_x * 12)
    board_state[1] = int(ball_y * 12)
    board_x = board_state[0]
    board_y = board_state[1]
    # print("Board x: " + str(board_x))
    # print("Board y: " + str(board_y))

    if velocity_x < 0:
        # Either -1 or 1
        board_state[2] = 0
    else:
        board_state[2] = 1
    if math.fabs(velocity_y) < 0.015:
        # velocity_y can be -1, 0, 1
        board_state[3] = 1
    elif velocity_y < 0:
        board_state[3] = 0
    else:
        board_state[3] = 2

    if paddle_y == (1-paddle_height):
        board_state[4] = 11
    else:
        board_state[4] = int(12 * paddle_y/(1 - paddle_height))


    


def print_board():
    global game_board
    global board_state 

    game_board = [[" " for i in range(12)] for j in range(12)]
    board_col = board_state[0]
    board_row = board_state[1]
    paddle_row = board_state[4]
    print("X: " + str(board_col) + " Y:" + str(board_row))
    if (board_col > 11):
        game_board[board_row][11] = "X"
    else:
        game_board[board_row][board_col] = "O"
    print("========================== Board ===========================")
    i = 0
    for row in game_board:
        if i == paddle_row:
            print(row, end="")
            print(" | ")
        else:
            print(row)
        i += 1
    print("============================================================")
    print("\n")


def init_tables():
    for i in range(13):
        for j in range(12):
            for x in range(2):
                # -1, +1
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


    for i in range(12):
        # j is hardcoded to 12 for last column
        for x in range(2):
            for y in range(3):
                for paddle_pos in range(12):
                    # action is hardcoded to 3
                    hashed_tuple = hash((i, 12, x, y, paddle_pos, 3))

def exploration_function(u, n):
    global Ne
    global r_plus
    if (n < Ne):
        return r_plus
    else:
        return u

def q_learning_algo(s_prime):
    global paddle_x
    global ball_x
    global s
    global a
    global r
    global r_prime
    global game_running

    # Terminal State Check
    if ball_x > paddle_x:
        # set -1 to all S/action pairs 
        # for i in range(3):    
        #     s_action = s + (i,)
        #     prev_state_hash = hash(s_action)
        #     Q[prev_state_hash] = -1
        s_action = s + (3,) 
        prev_state_hash = hash(s_action)
        Q[prev_state_hash] = -1
        game_running = False

    if s is not None:
        # print("Not None")
        s_action = s + (a,)
        prev_state_hash = hash(s_action)
        N[prev_state_hash] += 1
        possible_actions = []
        for i in range(3):
            s_prime_action = s_prime + (i,)
            action = hash(s_prime_action)
            if action not in Q:
                print(s_prime_action)
            possible_actions.append(Q[action])
        term2 = (learning_rate * N[prev_state_hash])
        term3 = (r + (discount_factor * max(possible_actions)) - Q[prev_state_hash])
        # term3 = (r + (discount_factor * max(possible_actions)))
        val = Q[prev_state_hash] + term2 * term3
        Q[prev_state_hash] = val
        update_learning_decay()

    s = s_prime
    final_actions = []
    final_NSAs = []
    for i in range(3):
        s_prime_action = s_prime + (i,)
        hashed = hash(s_prime_action)
        final_actions.append(Q[hashed])
        final_NSAs.append(N[hashed])

    # exploration function (where we decide what action we want to perform)
    
    # greedy approach
    # a = final_actions.index(max(final_actions))

    # random approach
    # a = random.choice([0, 1, 2])

    # actual exploration function
    exploration_actions = []
    for i in range(3):
        exploration_actions.append(exploration_function(final_actions[i], final_NSAs[i]))

    a = exploration_actions.index(max(exploration_actions))
    # if num_games < 1000:
    #     a = random.choice([0, 1, 2])
    r = r_prime
    r_prime = 0
    return a


def update_learning_decay():
    # C / (C + N(s, a)
    global s
    global a
    global learning_rate
    global learning_rate_const
    c = learning_rate_const
    s_action = s + (a,)
    current_state_action = hash(s_action)
    num_times = N[current_state_action]
    # print("Action: " + str(s_action) + " with NSA val: " + str(num_times))
    learning_rate = c / (num_times * c)
    # print("learning rate: " + str(learning_rate))


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
while game_running and num_games < 20000:
    # print("Num games is " + str(num_games))
    update_game_state()
    current_state = tuple(board_state)
    # print("Current Board State")
    # print(current_state)
    move_paddle = q_learning_algo(current_state)
    #print("Move paddle is: " + str(move_paddle))
    if move_paddle == 0:
        # print("Going Down")
        paddle_y -= 0.04
    elif move_paddle == 1:
        pass
        # print("Staying")
    else:
        # print("Going Up")
        paddle_y += 0.04
    update_game()
    if game_running:
        pass
        #print_board()
    else:
        if num_bounces > max_bounces:
            max_bounces = num_bounces
        # if (num_games % 1000 == 0):
        #     print("Game Over! Num bounces:  " + str(num_bounces))
        total_bounces += num_bounces
        reset_states()

print("Training average number of bounces per game: " + str(total_bounces/num_games))
print("Training max bounces: " + str(max_bounces))

# test run
debugging = False
reset_states()
num_games = 0
total_bounces = 0
while game_running and num_games < 100:
    update_game_state()
    #print_board()
    current_state = tuple(board_state)
    move_paddle = q_learning_algo(current_state)
    #print("Move paddle is: " + str(move_paddle))
    if move_paddle == 0:
        # print("Going Down")
        paddle_y -= 0.04
    elif move_paddle == 1:
        pass
        # print("Staying")
    else:
        # print("Going Up")
        paddle_y += 0.04
    update_game()
    if game_running:
        pass
        #print_board()
    else:
        if num_bounces > max_bounces:
            max_bounces = num_bounces
        # print("Game Over! Num bounces:  " + str(num_bounces))
        total_bounces += num_bounces
        reset_states()
print("Testing average number of bounces per game: " + str(total_bounces/num_games))
print("Testing max bounces: " + str(max_bounces))