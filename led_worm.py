import serial
import time
import random

ROW_SIZE = 8
COLUMN_SIZE = 8

DIRECTION_UP = 0
DIRECTION_DOWN = 1
DIRECTION_LEFT = 2
DIRECTION_RIGHT = 3

class LEDWorm:
    
    def __init__(self, length):
        self.body_length = length
        self.head_pos = [0,0] # x:0 y:0
        self.direction = DIRECTION_RIGHT
        self.body_list = [[0,0]]
        self.body_list_index = 0
        self.matrix = [[0 for i in range(COLUMN_SIZE)] for j in range(ROW_SIZE)]

    def _reset(self):
        self.head_pos = [0,0] # x:0 y:0
        self.direction = DIRECTION_RIGHT
        self.body_list = [[0,0]]
        self.body_list_index = 0
        self.matrix = [[0 for i in range(COLUMN_SIZE)] for j in range(ROW_SIZE)]
        
    def _possible_moves(self):
        possible_moves = []
        x_pos = self.head_pos[0]
        y_pos = self.head_pos[1]
        if (x_pos + 1 < COLUMN_SIZE):
            if (self.matrix[x_pos+1][y_pos] == 0):
                possible_moves.append(DIRECTION_RIGHT)
        if (x_pos - 1 >= 0):
            if (self.matrix[x_pos-1][y_pos] == 0):
                possible_moves.append(DIRECTION_LEFT)
        if (y_pos + 1 < ROW_SIZE):
            if (self.matrix[x_pos][y_pos+1] == 0):
                possible_moves.append(DIRECTION_DOWN)
        if (y_pos - 1 >= 0):
            if (self.matrix[x_pos][y_pos-1] == 0):
                possible_moves.append(DIRECTION_UP)

        if (self.direction == DIRECTION_UP):
            if DIRECTION_DOWN in possible_moves:
                possible_moves.remove(DIRECTION_DOWN)
        elif (self.direction == DIRECTION_DOWN):
            if DIRECTION_UP in possible_moves:
                possible_moves.remove(DIRECTION_UP)
        elif (self.direction == DIRECTION_LEFT):
            if DIRECTION_RIGHT in possible_moves:
                possible_moves.remove(DIRECTION_RIGHT)
        elif (self.direction == DIRECTION_RIGHT):
            if DIRECTION_LEFT in possible_moves:
                possible_moves.remove(DIRECTION_LEFT)
        
        return possible_moves

    def update(self):
        
        # Choose move
        possible_moves = self._possible_moves()
        if len(possible_moves) == 0:
            # If no possible move, reset all information
            self._reset()
            return    
        move = random.choice(possible_moves)

        # Update head position and direction
        if (move == DIRECTION_UP):
            new_head_x = self.head_pos[0]
            new_head_y = self.head_pos[1] - 1
        elif (move == DIRECTION_DOWN):
            new_head_x = self.head_pos[0]
            new_head_y = self.head_pos[1] + 1
        elif (move == DIRECTION_LEFT):
            new_head_x = self.head_pos[0] - 1
            new_head_y = self.head_pos[1]
        elif (move == DIRECTION_RIGHT):
            new_head_x = self.head_pos[0] + 1
            new_head_y = self.head_pos[1]
        self.head_pos = [new_head_x, new_head_y]
        self.direction = move

        # Update body list and matrix
        if len(self.body_list) < self.body_length:
            self.body_list.append([new_head_x, new_head_y])
            self.body_list_index = (self.body_list_index + 1) % self.body_length
        else:
            tail_index = (self.body_list_index + 1) % self.body_length
            tail_x = self.body_list[tail_index][0]
            tail_y = self.body_list[tail_index][1]
            self.matrix[tail_x][tail_y] = 0
            self.body_list_index = (self.body_list_index + 1) % self.body_length
            self.body_list[self.body_list_index] = [new_head_x, new_head_y]

        for elem in self.body_list:
            self.matrix[elem[0]][elem[1]] = 1
        
    def get_matrix(self):
        return self.matrix
    

if __name__ == '__main__':

    ser = serial.Serial('COM4',115200,timeout=100)

    LEDWorm1 = LEDWorm(6)

    time.sleep(2)

    while(1):
        LEDWorm1.update()
        matrix = LEDWorm1.get_matrix()
        for row in matrix:
            tmp_str = ""
            for elem in row:
                tmp_str += str(elem)
            ser.write(tmp_str+"\n")
            time.sleep(0.08)

    ser.close()
