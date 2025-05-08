import tkinter as tk
import random

class DotDodgerGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Dot Dodger")
        self.canvas_width = 400
        self.canvas_height = 600
        self.canvas = tk.Canvas(root, width=self.canvas_width, height=self.canvas_height, bg="black")
        self.canvas.pack()

        # Player attributes
        self.player_size = 30
        self.player = self.canvas.create_rectangle(185, 570, 215, 600, fill="cyan")
        self.player_speed = 20

        # Game settings
        self.enemies = []
        self.enemy_size = 20
        self.enemy_speed = 10
        self.spawn_interval = 1500  # in ms
        self.move_interval = 50  # in ms

        self.score = 0
        self.game_over = False
        self.score_text = self.canvas.create_text(10, 10, anchor="nw", fill="white", font=("Arial", 16), text="Score: 0")

        self.root.bind("<Left>", self.move_left)
        self.root.bind("<Right>", self.move_right)

        self.spawn_enemy()
        self.move_enemies()
        self.update_score()

    def move_left(self, event):
        if not self.game_over:
            self.canvas.move(self.player, -self.player_speed, 0)

    def move_right(self, event):
        if not self.game_over:
            self.canvas.move(self.player, self.player_speed, 0)

    def spawn_enemy(self):
        if not self.game_over:
            x = random.randint(0, self.canvas_width - self.enemy_size)
            enemy = self.canvas.create_oval(x, 0, x + self.enemy_size, self.enemy_size, fill="red")
            self.enemies.append(enemy)
            self.root.after(self.spawn_interval, self.spawn_enemy)

    def move_enemies(self):
        if self.game_over:
            return
        for enemy in list(self.enemies):
            self.canvas.move(enemy, 0, self.enemy_speed)
            if self.check_collision(enemy):
                self.end_game()
                return
            if self.canvas.coords(enemy)[1] > self.canvas_height:
                self.enemies.remove(enemy)
                self.canvas.delete(enemy)
        self.root.after(self.move_interval, self.move_enemies)

    def check_collision(self, enemy):
        player_coords = self.canvas.coords(self.player)
        enemy_coords = self.canvas.coords(enemy)
        overlap = not (
            player_coords[2] < enemy_coords[0] or
            player_coords[0] > enemy_coords[2] or
            player_coords[3] < enemy_coords[1] or
            player_coords[1] > enemy_coords[3]
        )
        return overlap

    def update_score(self):
        if not self.game_over:
            self.score += 1
            self.canvas.itemconfig(self.score_text, text=f"Score: {self.score}")
            self.root.after(500, self.update_score)

    def end_game(self):
        self.game_over = True
        self.canvas.create_text(
            self.canvas_width // 2,
            self.canvas_height // 2,
            text="Game Over",
            fill="white",
            font=("Arial", 32)
        )


# Run the game
def run_game():
    root = tk.Tk()
    game = DotDodgerGame(root)
    root.mainloop()

run_game()
