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

board_state = [ball_x, ball_y, velocity_x, velocity_y, paddle_y]
game_board = [[" " for i in range(12)] for j in range(12)]

def update_game():
	# has the agent tried to move the paddle out of bounds?
	global paddle_y
	global ball_x
	global ball_y
	global velocity_x
	global velocity_y
	if (paddle_y < 0):
		paddle_y = 0
	if ((paddle_y + paddle_height) > 1 ):
		paddle_y = 1 - paddle_height

	# move the ball
	ball_x += velocity_x
	ball_y += velocity_y

	# has the ball hit the left wall?
	if (ball_x < 0):
		ball_x = -ball_x
		velocity_x = -velocity_x

	# has the ball hit the top/bottom walls?
	if (ball_y < 0):
		ball_y = -ball_y
		velocity_y = -velocity_y
	if (ball_y > 1):
		ball_y = 2 - ball_y
		velocity_y = -velocity_y

	# has the ball hit the paddle?
	if (ball_x >= 1 and (ball_y > paddle_y and ball_y < (paddle_y + paddle_height))):
		num_bounces += 1
		ball_x = 2 * paddle_x - ball_x
		rand_U = random.uniform(-0.015, 0.015)
		rand_V = random.uniform(-0.03, 0.03)

		velocity_x = -velocity_x + rand_U
		velocity_y = velocity_y + rand_V
	elif(ball_x >= 1):
		global game_running
		game_running = False


	# check velocity requirements
	if (math.fabs(velocity_x) < 0.03):
		if (velocity_x < 0):
			velocity_x = -0.03
		else:
			velocity_x = 0.03

	if (math.fabs(velocity_y) > 1):
		if (velocity_y < 0):
			velocity_y = -1
		else:
			velocity_y = 1

	if (math.fabs(velocity_x) > 1):
		if (velocity_x < 0):
			velocity_x = -1
		else:
			velocity_x = 1

def update_game_state():
	board_state[0] = int(ball_x * 12)
	board_state[1] = int(ball_y * 12)
	if (velocity_x < 0):
		board_state[2] = -1
	else:
		board_state[2] = 1
	if (math.fabs(velocity_y) < 0.015):
		board_state[3] = 0
	elif (velocity_y < 0):
		board_state[3] = -1
	else:
		board_state[3] = 1

	if (paddle_y == (1-paddle_height)):
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

while(game_running):
	update_game()
	if (game_running):
		update_game_state()
		print_board()
	else:
		print("Game Over!")
