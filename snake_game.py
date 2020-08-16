from random import randint
import tkinter as tk
from PIL import Image , ImageTk
import numpy as np

MOVE_INCREMENT = 20
MOVES_PER_SECOND = 15
GAME_SPEED = 1000 // MOVES_PER_SECOND

class Snake(tk.Canvas):
    def __init__(self):
        super().__init__(width = 600, height = 620, background= 'black', highlightthickness = 0)
        self.snake_positions = [(100,100),(80,100),(60,100)]
        self.food_positions = self.set_new_food_positions()
        self.score = 0
        self.direction = 'Right'`
        self.bind_all('<Key>', self.on_key_press)

        self.load_assets()
        self.create_objects()
        self.after(GAME_SPEED, self.perform_action)

    def load_assets(self):
        try:
            self.snake_body_image = Image.open('./snake.png')
            self.snake_body = ImageTk.PhotoImage(self.snake_body_image)

            self.food_image = Image.open('./food.png')
            self.food = ImageTk.PhotoImage(self.food_image)
        except IOError as error:
            print(error)
            root.destroy


    def create_objects(self):
        self.create_text(
            45, 12, text = f"Score: {self.score}", tag = 'score', fill = '#fff', font = ('TkDefaultFont', 14)
        )
        for x_positions,y_positions in self.snake_positions:
            self.create_image(x_positions,y_positions,tag = 'snake', image = self.snake_body)

        self.create_image(*self.food_positions , image = self.food , tag = 'food')
        self.create_rectangle(7, 27, 593, 613, outline = '#525d69')

    def move_snake(self):
        head_x_position , head_y_position = self.snake_positions[0]

        if self.direction == 'Left':
            new_head_position = (head_x_position - MOVE_INCREMENT, head_y_position)
        elif self.direction == 'Right':
            new_head_position = (head_x_position + MOVE_INCREMENT, head_y_position)
        elif self.direction == 'Up':
            new_head_position = (head_x_position , head_y_position - MOVE_INCREMENT )
        elif self.direction == 'Down':
            new_head_position = (head_x_position , head_y_position + MOVE_INCREMENT )


        self.snake_positions = [new_head_position ] + self.snake_positions[:-1]

        for segment, position in zip(self.find_withtag('snake'), self.snake_positions):
            self.coords(segment, position)

    def perform_action(self):
        if self.check_collisions():
            self.end_game()
            return
        self.check_food_collision()
        self.move_snake()
        self.after(GAME_SPEED, self.perform_action)

    def check_collisions(self):
        head_x_position , head_y_position = self.snake_positions[0]
        
        return(
            head_x_position in (0,600)
            or head_y_position in (20 , 620)
            or (head_x_position , head_y_position) in self.snake_positions[1:]
        )

    def on_key_press(self, e):
        new_direction = e.keysym
        all_direction = ('Up', 'Down', 'Left', 'Right')
        opposites = ({'Up', 'Down'} , {'Left', 'Right'})

        if (new_direction in all_direction
            and {new_direction, self.direction} not in opposites    
        ):
            self.direction = new_direction

    def check_food_collision(self):
        if self.snake_positions[0] == self.food_positions:
            self.score +=1
            self.snake_positions.append(self.snake_positions[-1])
            self.create_image(
                *self.snake_positions[-1], image = self.snake_body, tag = 'snake'
            )

            self.food_positions = self.set_new_food_positions()
            self.coords(self.find_withtag('food'), *self.food_positions)

            score = self.find_withtag('score')
            self.itemconfigure(score , text= f'Score: {self.score}', tag = 'score')

    def set_new_food_positions(self):
        while True:
            x_positions = randint(1, 29) * MOVE_INCREMENT
            y_positions = randint(3, 30) * MOVE_INCREMENT
            food_positions = (x_positions, y_positions)

            if food_positions not in self.snake_positions:
                return food_positions

    def end_game(self):
        self.delete(tk.ALL)
        self.create_text(
            self.winfo_width() / 2,
            self.winfo_height() / 2,
            text = f'Game Over ! Your Score is {self.score}',
            fill = '#fff',
            font = ('TkDefaultFont', 24)

        )

root = tk.Tk()
root.title('Snake Game')
root.resizable(False, False)

board = Snake()
board.pack()


root.mainloop()
