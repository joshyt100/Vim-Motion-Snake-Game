import tkinter as tk
import random


class SnakeGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Snake Game")
        self.master.resizable(False, False)

        self.canvas = tk.Canvas(self.master, width=400, height=400, bg="black")
        self.canvas.pack()

        self.score = 0
        self.delay = 150
        self.snake = [(100, 100), (80, 100), (60, 100)]
        self.direction = "Right"
        self.food = self.create_food()
        self.game_over = False

        self.bind_keys()
        self.draw()
        self.move_snake()

    def bind_keys(self):
        self.master.bind("k", lambda event: self.change_direction("Up"))
        self.master.bind("j", lambda event: self.change_direction("Down"))
        self.master.bind("h", lambda event: self.change_direction("Left"))
        self.master.bind("l", lambda event: self.change_direction("Right"))

    def change_direction(self, direction):
        if direction == "Up" and self.direction != "Down":
            self.direction = "Up"
        elif direction == "Down" and self.direction != "Up":
            self.direction = "Down"
        elif direction == "Left" and self.direction != "Right":
            self.direction = "Left"
        elif direction == "Right" and self.direction != "Left":
            self.direction = "Right"

    def draw(self):
        self.canvas.delete("all")
        self.canvas.create_text(45, 10, text=f"Score: {self.score}", fill="white")

        for segment in self.snake:
            self.canvas.create_rectangle(
                segment[0], segment[1], segment[0] + 20, segment[1] + 20, fill="green"
            )

        self.canvas.create_oval(
            self.food[0], self.food[1], self.food[0] + 20, self.food[1] + 20, fill="red"
        )

        if self.game_over:
            self.canvas.create_text(
                200, 200, text="Game Over", fill="white", font=("Helvetica", 30)
            )
            self.canvas.create_text(
                200, 250, text="Press R to replay", fill="white", font=("Helvetica", 15)
            )

    def move_snake(self):
        if not self.game_over:
            head = self.snake[0]
            if self.direction == "Up":
                new_head = (head[0], head[1] - 20)
            elif self.direction == "Down":
                new_head = (head[0], head[1] + 20)
            elif self.direction == "Left":
                new_head = (head[0] - 20, head[1])
            elif self.direction == "Right":
                new_head = (head[0] + 20, head[1])

            self.snake.insert(0, new_head)

            if self.check_collisions():
                self.game_over = True

            if self.snake[0] == self.food:
                self.score += 10
                self.delay -= 2
                self.food = self.create_food()
            else:
                self.snake.pop()

            self.draw()
            self.master.after(self.delay, self.move_snake)

    def create_food(self):
        while True:
            x = random.randint(0, 19) * 20
            y = random.randint(0, 19) * 20
            if (x, y) not in self.snake:
                return (x, y)

    def check_collisions(self):
        head = self.snake[0]
        if (
            head[0] < 0
            or head[0] >= 400
            or head[1] < 0
            or head[1] >= 400
            or head in self.snake[1:]
        ):
            return True
        return False

    def replay(self):
        self.snake = [(100, 100), (80, 100), (60, 100)]
        self.direction = "Right"
        self.score = 0
        self.delay = 150
        self.food = self.create_food()
        self.game_over = False
        self.move_snake()


if __name__ == "__main__":
    root = tk.Tk()
    game = SnakeGame(root)
    root.bind("r", lambda event: game.replay())
    root.mainloop()
