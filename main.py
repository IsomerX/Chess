import time
import sys, pygame
import math
import pygame as pygame
import numpy as np
import random

pygame.init()

WHITE = (255, 255, 255)

class pic(pygame.sprite.Sprite):
    
    def __init__(self, color, piece, width = 64):
        super().__init__()
        
        self.image = pygame.Surface([width, width])
        self.image.fill(WHITE)
        self.image.set_colorkey(WHITE)
        self.image = pygame.image.load(f"sprites/{color_piece[color]}_{piece.upper()}.png")
        self.image = pygame.transform.scale(self.image, (width,width))
        self.rect = self.image.get_rect()

types = {'K' : 0, 'Q' : 1, 'B' : 2, 'P' : 3, 'N' : 4, 'R' : 5}
types_rev = {0 : 'K', 1 : 'Q', 2 : 'B', 3 : 'P', 4 : 'N', 5 : 'R'}
color_piece = {0 : "white", 1 : "black"}
moves = {
    'bP' : [(1, 0), (2,0)],
    'wP' : [(-1, 0), (-2,0)],
    'K' : [(-1,-1),(-1,0),(-1,1),(0,1),(1,1),(1,0),(1,-1),(0,-1)],
    'N' : [(-2,-1),(-2,1),(2,-1),(2,1),(-1,-2),(1,-2),(-1,2),(1,2)]
}
WHITE = (255, 255, 255)

class piece(pygame.sprite.Sprite):
    Piece = 0
    piece_val = 0
    piece_move_number = 0
    def __init__(self, pos, piece, color, width = 64):
        self.Piece += pos[0]
        self.Piece <<= 3
        self.Piece += pos[1]
        self.Piece <<= 3
        self.Piece += types[piece]
        self.Piece <<= 1
        self.Piece += color
        self.image = pic(color, piece, width)
        self.piece_val = types[piece]
        self.piece_move_number = 0

    def get_piece(self):
        temp = self.Piece
        col = temp & 1
        temp >>= 1

        type_piece = 0
        for i in range(3):
            if(temp & 1):
                type_piece += 2**i
            temp >>= 1

        x = 0
        for i in range(3):
            if(temp & 1):
                x += 2**i
            temp >>= 1

        y = 0
        for i in range(3):
            if(temp & 1):
                y += 2**i
            temp >>= 1
        return ((y, x), type_piece, col)     

    def get_moves(self):
        moves_list = []
        (y, x), type_piece, col = self.get_piece()
        if(types_rev[type_piece] == 'R'):
            for (i,j) in moves['R']:
                dr = y + i
                dc = x + j
                if(dr > 7 or dc > 7 or dr < 0 or dc < 0):
                    continue
                else:
                    moves_list.append((i,j))
        elif(types_rev[type_piece] == 'B'):
            for (i,j) in moves['B']:
                dr = y + i
                dc = x + j
                if(dr > 7 or dc > 7 or dr < 0 or dc < 0):
                    continue
                else:
                    moves_list.append((i,j))
        elif(types_rev[type_piece] == 'N'):
            for (i,j) in moves['B']:
                dr = y + i
                dc = x + j
                if(dr > 7 or dc > 7 or dr < 0 or dc < 0):
                    continue
                else:
                    moves_list.append((i,j))
        elif(types_rev[type_piece] == 'K'):
            for (i,j) in moves['K']:
                dr = y + i
                dc = x + j
                if(dr > 7 or dc > 7 or dr < 0 or dc < 0):
                    continue
                else:
                    moves_list.append((i,j))
        elif(types_rev[type_piece] == 'Q'):
            for (i,j) in moves['B']:
                dr = y + i
                dc = x + j
                if(dr > 7 or dc > 7 or dr < 0 or dc < 0):
                    continue
                else:
                    moves_list.append((i,j))
            for (i,j) in moves['R']:
                dr = y + i
                dc = x + j
                if(dr > 7 or dc > 7 or dr < 0 or dc < 0):
                    continue
                else:
                    moves_list.append((i,j))
        return moves_list
class Board:
    pieces = []
    pieces_white = []
    pieces_black = []
    grid = []
    move_list_white = {}
    move_list_black = {}
    to_play = ""
    def __init__(self, start = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'):
        # initialize
        self.pieces = []
        self.pieces_white = []
        self.pieces_black = []
        self.to_play = ""
        self.move_number = 0
        self.grid = []
        self.move_list_white = {}
        self.move_list_black = {}
        fen_list = start.split()
        pos = fen_list[0].split('/')
        self.to_play = fen_list[1]
        self.move_number = int(fen_list[-1])
        rank = 0
        for i in pos:
            x = 0
            for j in i:
                if(j.isnumeric()):
                    x += int(j)
                else:
                    color = j.islower()
                    self.pieces.append(piece((rank, x),j.upper(),color))
                    if(color):
                        self.pieces_black.append(piece((rank, x),j.upper(),color))
                    else:
                        self.pieces_white.append(piece((rank, x),j.upper(),color))
                    x += 1
            rank += 1

        for i in range(8):
            temp = []
            for j in range(8):
                temp.append(" ")
            self.grid.append(temp)

        for i in self.pieces:
            (y, x), ch, col = i.get_piece()
            self.grid[y][x] = i
            # pprint(grid)
    
    def show(self):
        for i in self.grid:
            for j in i:
                if(j == " "):
                    print("_", end = " ")
                else:
                    (y, x), ch, col = j.get_piece()
                    p = types_rev[ch]
                    if(col == 1):
                        print(p.lower(), end = " ")
                    else:
                        print(p, end = " ")
            print("")

    def move_to(self, x1, y1, y2, x2):
        current_piece = self.grid[x1][y1]
        if(current_piece == " "):
            print("No piece here")
            return 
        if(self.grid[y2][x2] != " "):
            return
        # for i in self.grid:
        #     for j in i:
        #         if(j == " "):
        #             print(j, end = " ")
        #         else:
        #             print("_", end = " ")
        #     print("")
        current_piece.piece_move_number += 1
        self.grid[x1][y1] = " "
        self.grid[y2][x2] = current_piece
        temp = current_piece.Piece
        # print(bin(temp))
        for i in range(3):
            if(x2 & 1 << i):
                temp |= 1 << (i + 4)
            else:
                temp &= ~(1 << (i + 4))
            
            if(y2 & 1 << i):
                temp |= 1 << (i + 7)
            else:
                temp &= ~(1 << (i + 7))

        current_piece.Piece = temp
        # for i in self.grid:
        #     for j in i:
        #         if(j == " "):
        #             print(j, end = " ")
        #         else:
        #             print("_", end = " ")
        #     print("")
        # print(bin(temp))

    def gen_moves(self, col):
        self.move_list_white = {}
        self.move_list_black = {}
        for k in self.pieces:
                moves_ = []
                (y, x), type_piece, col = k.get_piece()
                if(types_rev[type_piece] == 'R'):
                    # for (i,j) in moves['R']:
                    #     dr = y + i
                    #     dc = x + j
                    #     if(dr > 7 or dc > 7 or dr < 0 or dc < 0 or self.grid[dr][dc] != " "):
                    #         continue
                    #     else:
                    #         moves_.append((i,j))
                    for ii in range(1,8):
                        if(ii == 0):
                            continue
                        dr = y + ii
                        dc = x
                        if(dr > 7 or dc > 7 or dr < 0 or dc < 0):
                            continue
                        elif(self.grid[dr][dc] != " "):
                            (y1, x1), type_piece1, col1 = self.grid[dr][dc].get_piece()
                            if(col == col1):
                                break
                            moves_.append((ii,0))
                            break
                        else:
                            moves_.append((ii,0))
                    for ii in range(-1,-7, -1):
                        if(ii == 0):
                            continue
                        dr = y + ii
                        dc = x
                        if(dr > 7 or dc > 7 or dr < 0 or dc < 0):
                            continue
                        elif(self.grid[dr][dc] != " "):
                            (y1, x1), type_piece1, col1 = self.grid[dr][dc].get_piece()
                            if(col == col1):
                                break
                            moves_.append((ii,0))
                            break
                        else:
                            moves_.append((ii,0))
                    for ii in range(-1,-7,-1):
                        if(ii == 0):
                            continue
                        dr = y
                        dc = x + ii
                        if(dr > 7 or dc > 7 or dr < 0 or dc < 0):
                            continue
                        elif(self.grid[dr][dc] != " "):
                            (y1, x1), type_piece1, col1 = self.grid[dr][dc].get_piece()
                            if(col == col1):
                                break
                            moves_.append((0,ii))
                            break
                        else:
                            moves_.append((0,ii))
                elif(types_rev[type_piece] == 'B'):
                    # for (i,j) in moves['B']:
                    #     dr = y + i
                    #     dc = x + j
                    #     if(dr > 7 or dc > 7 or dr < 0 or dc < 0 or self.grid[dr][dc] != " "):
                    #         continue
                    #     else:
                    #         moves_.append((i,j))

                    for ii in range(1,8):
                        dr = y + ii
                        dc = x + ii
                        if(dr > 7 or dc > 7 or dr < 0 or dc < 0):
                            continue
                        elif(self.grid[dr][dc] != " "):
                            (y1, x1), type_piece1, col1 = self.grid[dr][dc].get_piece()
                            if(col == col1):
                                break
                            moves_.append((ii,ii))
                            break
                        else:
                            moves_.append((ii,ii))

                    for ii in range(-1,-7,-1):
                        dr = y + ii
                        dc = x + ii
                        if(dr > 7 or dc > 7 or dr < 0 or dc < 0):
                            continue
                        elif(self.grid[dr][dc] != " "):
                            (y1, x1), type_piece1, col1 = self.grid[dr][dc].get_piece()
                            if(col == col1):
                                break
                            moves_.append((ii,ii))
                            break
                        else:
                            moves_.append((ii,ii))



                    for ii in range(1,8):
                        dr = y + ii
                        dc = x - ii
                        if(dr > 7 or dc > 7 or dr < 0 or dc < 0):
                            continue
                        elif(self.grid[dr][dc] != " "):
                            (y1, x1), type_piece1, col1 = self.grid[dr][dc].get_piece()
                            if(col == col1):
                                break
                            moves_.append((ii,-ii))
                            break
                        else:
                            moves_.append((ii,-ii))

                    for ii in range(1,8):
                        dr = y - ii
                        dc = x + ii
                        if(dr > 7 or dc > 7 or dr < 0 or dc < 0):
                            continue
                        elif(self.grid[dr][dc] != " "):
                            (y1, x1), type_piece1, col1 = self.grid[dr][dc].get_piece()
                            if(col == col1):
                                break
                            moves_.append((-ii,ii))
                            break
                        else:
                            moves_.append((-ii,ii))
                elif(types_rev[type_piece] == 'N'):
                    for (i,j) in moves['N']:
                        dr = y + i
                        dc = x + j
                        if(dr > 7 or dc > 7 or dr < 0 or dc < 0 or self.grid[dr][dc] != " "):
                            continue
                        else:
                            moves_.append((i,j))
                elif(types_rev[type_piece] == 'P'):
                    if(col):
                        if(k.piece_move_number == 0):
                            for (i,j) in moves['bP']:
                                dr = y + i
                                dc = x + j
                                if(dr > 7 or dc > 7 or dr < 0 or dc < 0 or self.grid[dr][dc] != " "):
                                    continue
                                else:
                                    moves_.append((i,j))
                        else:
                            (i, j) = moves['bP'][0]
                            dr = y + i
                            dc = x + j
                            if(dr > 7 or dc > 7 or dr < 0 or dc < 0 or self.grid[dr][dc] != " "):
                                continue
                            else:
                                moves_.append((i,j))
                    else:
                        if(k.piece_move_number == 0):
                            for (i,j) in moves['wP']:
                                dr = y + i
                                dc = x + j
                                if(dr > 7 or dc > 7 or dr < 0 or dc < 0 or self.grid[dr][dc] != " "):
                                    continue
                                else:
                                    moves_.append((i,j))
                        else:
                            (i, j) = moves['wP'][0]
                            dr = y + i
                            dc = x + j
                            if(dr > 7 or dc > 7 or dr < 0 or dc < 0 or self.grid[dr][dc] != " "):
                                continue
                            else:
                                moves_.append((i,j))
                elif(types_rev[type_piece] == 'K'):
                    for (i,j) in moves['K']:
                        dr = y + i
                        dc = x + j
                        if(dr > 7 or dc > 7 or dr < 0 or dc < 0 or self.grid[dr][dc] != " "):
                            continue
                        else:
                            moves_.append((i,j))
                elif(types_rev[type_piece] == 'Q'):
                    for ii in range(1,8):
                        dr = y + ii
                        dc = x
                        if(dr > 7 or dc > 7 or dr < 0 or dc < 0):
                            continue
                        elif(self.grid[dr][dc] != " "):
                            (y1, x1), type_piece1, col1 = self.grid[dr][dc].get_piece()
                            if(col == col1):
                                break
                            moves_.append((ii,0))
                            break
                        else:
                            moves_.append((ii,0))
                    
                    for ii in range(-1,-7, -1):
                        dr = y + ii
                        dc = x
                        if(dr > 7 or dc > 7 or dr < 0 or dc < 0):
                            continue
                        elif(self.grid[dr][dc] != " "):
                            (y1, x1), type_piece1, col1 = self.grid[dr][dc].get_piece()
                            if(col == col1):
                                break
                            moves_.append((ii,0))
                            break
                        else:
                            moves_.append((ii,0))
                    for ii in range(1,8):
                        dr = y + ii
                        dc = x + ii
                        if(dr > 7 or dc > 7 or dr < 0 or dc < 0):
                            continue
                        elif(self.grid[dr][dc] != " "):
                            (y1, x1), type_piece1, col1 = self.grid[dr][dc].get_piece()
                            if(col == col1):
                                break
                            moves_.append((ii,ii))
                            break
                        else:
                            moves_.append((ii,ii))

                    for ii in range(-1,-7,-1):
                        dr = y + ii
                        dc = x + ii
                        if(dr > 7 or dc > 7 or dr < 0 or dc < 0):
                            continue
                        elif(self.grid[dr][dc] != " "):
                            (y1, x1), type_piece1, col1 = self.grid[dr][dc].get_piece()
                            if(col == col1):
                                break
                            moves_.append((ii,ii))
                            break
                        else:
                            moves_.append((ii,ii))

                    for ii in range(1,8):
                        dr = y + ii
                        dc = x - ii
                        if(dr > 7 or dc > 7 or dr < 0 or dc < 0):
                            continue
                        elif(self.grid[dr][dc] != " "):
                            (y1, x1), type_piece1, col1 = self.grid[dr][dc].get_piece()
                            if(col == col1):
                                break
                            moves_.append((ii,-ii))
                            break
                        else:
                            moves_.append((ii,-ii))

                    for ii in range(1,8):
                        dr = y - ii
                        dc = x + ii
                        if(dr > 7 or dc > 7 or dr < 0 or dc < 0):
                            continue
                        elif(self.grid[dr][dc] != " "):
                            (y1, x1), type_piece1, col1 = self.grid[dr][dc].get_piece()
                            if(col == col1):
                                break
                            moves_.append((-ii,ii))
                            break
                        else:
                            moves_.append((-ii,ii))
                if(col):
                    self.move_list_white[(y,x)] = moves_
                else:
                    self.move_list_black[(y,x)] = moves_
       
    def random_move(self, col):
        self.gen_moves(col)
        if(not col):
            key, value = random.choice(list(self.move_list_white.items()))
            print(key, value)
            pie = self.move_list_white[key]
            while(pie == []):
                key, value = random.choice(list(self.move_list_white.items()))
                pie = self.move_list_white[key]
            (r, t) = pie[np.random.randint(0,len(self.move_list_white[key]))]
            self.move_to(key[0], key[1], key[0] + r, key[1] + t)
        else:
            key, value = random.choice(list(self.move_list_black.items()))
            print(key, value)
            pie = self.move_list_black[key]
            while(pie == []):
                key, value = random.choice(list(self.move_list_black.items()))
                pie = self.move_list_black[key]
            (r, t) = pie[np.random.randint(0,len(self.move_list_black[key]))]
            self.move_to(key[0], key[1], key[0] + r, key[1] + t)

size = width, height = 512, 512
white = 204, 51, 255
black = 255, 102, 204
hightlight = 192, 192, 192
title = "Chess Board"
width = 64 
original_color = ''
screen = pygame.display.set_mode(size)
pygame.display.set_caption(title)
 
rect_list = list() 

for i in range(0, 8):
    for j in range(0, 8): 
        if i % 2 == 0:
            if j % 2 != 0:
                rect_list.append(pygame.Rect(j * 64, i * 64, 64, 64))
        else:
            if j % 2 == 0: 
                rect_list.append(pygame.Rect(j * 64, i * 64, 64, 64))
 
chess_board_surface = pygame.Surface(size)
chess_board_surface.fill(white)
 
for chess_rect in rect_list:
    pygame.draw.rect(chess_board_surface, black, chess_rect)

board_new = Board()

u = 0
v = 0
original_color = 0
color = 1

def draw():
    global u, v, original_color, color
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                # start = time.time()  
                sys.exit()
                # board_new.random_move(color)
                # color = 1-color
                # print(time.time() - start, "second")
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pos = event.pos
            u = math.floor(pos[0] / width)
            v = math.floor(pos[1] / width)
            original_color = chess_board_surface.get_at((u * width, v * width ))
            pygame.draw.rect(chess_board_surface, hightlight, pygame.Rect((u) * width, (v) * width, 64, 64))
            print(u, v)
            print(board_new.gen_moves())
        elif(event.type == pygame.MOUSEBUTTONUP and event.button == 3):
            pos = event.pos
            x1 = math.floor(pos[0] / width)
            y1 = math.floor(pos[1] / width)
            board_new.move_to(v, u, y1, x1)
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            pos = event.pos
            piece_temp = board_new.grid[v][u]
            # if(piece_temp != " "):
            #     print(piece_temp.get_piece(), bin(piece_temp.Piece))
            pygame.draw.rect(chess_board_surface, original_color, pygame.Rect((u) * width, (v) * width, 64, 64))
    
    board_new.random_move(color)
    color = 1-color

    all_sprites_list = pygame.sprite.Group()
    
    for i in board_new.pieces:
        (y, x), ch, col = i.get_piece()
        i.image.rect.x = x*width
        i.image.rect.y = y*width
        all_sprites_list.add(i.image)

    all_sprites_list.update()

    screen.blit(chess_board_surface, (0, 0))
    all_sprites_list.draw(screen)
    pygame.display.update()
    # time.sleep(0.2)
while 1:
    draw()