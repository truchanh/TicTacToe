import time
import random as rd
import pygame as pg
start = time.time()
pg.init()

##let's define some colours constant
BLACK = 0,0,0
WHITE = 255,255,255
RED = 255,0,0
GREEN = 0,255,0
BLUE = 0,0,255
CYAN = 0,255,255
MAGENTA = 255,0,255
YELLOW = 255,255,0

BACKGROUND_COLOR = '#14bdac'
LINE_COLOR = '#0da192'
X_COLOR = '#545454'
O_COLOR = '#f2ebd3'

##basic setup video modes
FPS = 30
LINE_W = 15
MARGIN = 20
CELLSIZE = 100
dims = CELLSIZE*3, CELLSIZE*3
flags = pg.DOUBLEBUF|pg.HWSURFACE
bpp = pg.display.mode_ok(dims,flags)
win = pg.display.set_mode(dims,flags,bpp)

player_pos = []
comp_pos = []
##initialize a 2-dimension board using list-comprehension technique
board = [['' for j in range(3)] for i in range(3)]
# print(board)



def is_free_space(b):
	space_left = [i.count('') for i in b]
	return any(space_left)


def draw_figure(player,column,row):
	if player == 'x':
		x1 = column*CELLSIZE+MARGIN           ##left
		x2 = column*CELLSIZE+CELLSIZE-MARGIN  ##right
		y1 = row*CELLSIZE+MARGIN              ##top
		y2 = row*CELLSIZE+CELLSIZE-MARGIN     ##bottom
		pg.draw.line(win,X_COLOR,(x1,y1),(x2,y2),LINE_W)  ##(left,top) to (right,bottom)
		pg.draw.line(win,X_COLOR,(x2,y1),(x1,y2),LINE_W)  ##(right,top) to (left,bottom)
	elif player == 'o':
		cx = column*CELLSIZE+CELLSIZE/2  ##centered vertically
		cy = row*CELLSIZE+CELLSIZE/2     ##centered horizontally
		center = cx, cy
		radius = (CELLSIZE-MARGIN)/2
		pg.draw.circle(win,O_COLOR,center,radius,LINE_W)


def display_game_over_screen(winner):
	font = pg.font.SysFont('comicsansms',32)
	if winner is not None:
		if winner == 'x':
			message = 'You win'
			color = GREEN
		elif winner == 'o':
			message = 'You lose'
			color = BLUE
	else:
		message = 'That\'s a draw!'
		color = MAGENTA
	text_surf = font.render(message,True,color)
	text_rect = text_surf.get_rect(center=win.get_rect().center)
	bg_surf = pg.Surface((text_rect.w+10,text_rect.h+10))
	bg_surf.set_alpha(190)  ##set the transparency effect on the background behind the text
	bg_rect = bg_surf.get_rect(topleft=(text_rect.left-5,text_rect.top-5))
	win.blit(bg_surf, bg_rect)
	win.blit(text_surf, text_rect)


def on_mousebuttondown(event):
	if event.button == 1:  ##only left-click allowed
		m_col, m_row = event.pos[0]//CELLSIZE, event.pos[1]//CELLSIZE  ##get the mouse click position format (column,row)
		return m_col,m_row


def main():
	winner = None
	block_move = False
	switch_turn = False
	done = False
	while not done:
		# print(board)
		for e in pg.event.get():
			if e.type in (pg.QUIT, pg.WINDOWCLOSE):
				done = True
			elif e.type == pg.MOUSEBUTTONDOWN:
				mc,mr = on_mousebuttondown(e)  ##capture the returned value
				if not block_move:
					if (mc,mr) not in player_pos and (mc,mr) not in comp_pos:
						board[mr][mc] = 'x'
						player_pos.append((mc,mr))
						switch_turn = True

		win.fill(BACKGROUND_COLOR)
		##draw the 3x3 size grid board (only 2 lines on each dimension)
		for i in range(1,3,1):  ##loop 2 times from 1..2
			p = i*CELLSIZE-(LINE_W*.125)  ##because we don't want to draw any lines at the screen edges: left and right, top and bottom
			pg.draw.line(win,LINE_COLOR,(p,0),(p,300),5)  ##two vertical lines
			pg.draw.line(win,LINE_COLOR,(0,p),(300,p),5)  ##two horizontal lines

		##draw the player
		for col,row in player_pos:
			draw_figure('x',col,row)

		for col,row in comp_pos:
			draw_figure('o',col,row)

		if switch_turn and not block_move:
			cc = rd.randint(0,2)
			cr = rd.randint(0,2)
			if (cc,cr) not in comp_pos and (cc,cr) not in player_pos:
				board[cr][cc] = 'o'
				comp_pos.append((cc,cr))
				switch_turn = False


		######################### DETERMINE WINNER ############################
		##horizontal check -
		for row in board:
			if row.count('x') == 3:
				winner = 'x'
			elif row.count('o') == 3:
				winner = 'o'

		##vertical check |
		for i in range(len(board)):
			if board[0][i] == 'x' and board[1][i] == 'x' and board[2][i] == 'x':
				winner = 'x'
			elif board[0][i] == 'o' and board[1][i] == 'o' and board[2][i] == 'o':
				winner = 'o'

		##diagonal strike x
		if board[0][0] == board[1][1] == board[2][2] == 'x' or\
		   board[0][2] == board[1][1] == board[2][0] == 'x':
			winner = 'x'
		elif board[0][0] == board[1][1] == board[2][2] == 'o' or\
		     board[0][2] == board[1][1] == board[2][0] == 'o':
			winner = 'o'

		################## DISPLAY RESULT AND END THE GAME ######################
		if winner is not None:
			if winner == 'x':
				block_move = True
				# print('='*40)
				# print('Hooray! you win:D'.upper())
				# print('='*40)
				display_game_over_screen(winner)
			elif winner == 'o':
				block_move = True
				# print('='*40)
				# print('Oh no you lose:('.upper())
				# print('='*40)
				display_game_over_screen(winner)

		if not is_free_space(board):
			block_move = True
			if winner is None:
				# print('='*40)
				# print('That\'s a draw'.upper())
				# print('='*40)
				display_game_over_screen(winner)

		pg.display.flip()  ##update everything you've drawn onto the screen surface(win)
		pg.time.Clock().tick(FPS)  ##limits the framerate
	pg.quit()
if __name__ == '__main__':
	main()
end = time.time()
print('finished in %.4f'%(end-start),'sec')