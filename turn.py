import pygame

class Turn():
    def __init__(self, player_color):
        self.sequence = []
        self.turn_number = 0
        self.player = player_color
        self.current_move = "wh"

    def next_turn(self, piece, fi1, fi2):
        #TODO: store move in array: i.e. rXd4 
            
