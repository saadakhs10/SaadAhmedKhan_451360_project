import tkinter as tk
import random

class Snake_Game:
    def __init__(self, saad):
        # Initialize the main window
        self.saad = saad
        self.saad.title("Snake Game")
        self.saad.geometry("400x400")
        self.saad.resizable(False, False)

        # Create the canvas for the game
        self.canvas = tk.Canvas(self.saad, bg="gray", width=400, height=400)
        self.canvas.pack()

        player_start_location = (100, 100)  # Change the starting location for the player snake
        ai_start_location = (300, 300)  # Change the starting location for the AI snake

        # Create instances of Snake for player and AI with different starting locations
        self.player_snake = Snake(self.canvas, "green", "Player", player_start_location)
        self.ai_snake = Snake(self.canvas, "black", "AI", ai_start_location)

        # Initialize food, obstacles, and scores
        self.food = None
        self.obstacles = self.create_obstacles()
        self.player_score = 3
        self.ai_score = 3

        # Create labels to display scores
        self.player_score_label = self.canvas.create_text(50, 10, text=f"Saad Score: {self.player_score}", font=("Helvetica", 12), fill="white")
        self.ai_score_label = self.canvas.create_text(350, 10, text=f"AI Score: {self.ai_score}", font=("Helvetica", 12), fill="white")

        # Bind the key press event to the change_direction method for player's snake
        self.saad.bind("<KeyPress>", self.change_direction)

        # Flag to indicate if the game is over
        self.game_over_flag = False

        # Start the game update loop
        self.update()

    def create_food(self):
        # Create food at a random location on the canvas
        while True:
            x = random.randint(0, 39) * 10
            y = random.randint(0, 39) * 10
            # Ensure food doesn't overlap with the player's or AI's snake or previous food
            if (
                (x, y) not in self.player_snake.segments
                and (x, y) not in self.ai_snake.segments
                and (self.food is None or (x, y) != self.canvas.coords(self.food)[:2])
            ):
                break
        food = self.canvas.create_rectangle(x, y, x + 10, y + 10, fill="red", tags="food")
        return food

    def create_obstacles(self):
        # Create three obstacles at specific locations on the canvas
        obstacles = [
            self.canvas.create_rectangle(100, 100, 110, 110, fill="blue"),
            self.canvas.create_rectangle(110, 110, 120, 120, fill="blue"),
            self.canvas.create_rectangle(120, 120, 130, 130, fill="blue"),
            self.canvas.create_rectangle(130, 130, 140, 140, fill="blue"),
            self.canvas.create_rectangle(140, 140, 150, 150, fill="blue"),
            self.canvas.create_rectangle(150, 150, 160, 160, fill="blue")
        ]
        return obstacles
       

    def update(self):
        if not self.game_over_flag:
            # Move the player's snake
            self.player_snake.move()
            # Move the AI's snake towards the food
            self.ai_snake.move_towards_food(self.food)

            player_head = self.player_snake.get_head()
            ai_head = self.ai_snake.get_head()

            # Check for collisions with boundaries for the player's snake
            if self.saad.winfo_exists() and self.canvas.winfo_exists():
                if player_head[0] < 0 or player_head[0] >= 400 or player_head[1] < 0 or player_head[1] >= 400:
                    self.game_over("Game Over! Player snake collided with the boundary.")

                # Check for collisions with itself for the player's snake
                if player_head in self.player_snake.segments[1:]:
                    self.game_over("Game Over! Player snake collided with itself.")

                # Check for collisions with obstacles for the player's snake
                for obstacle in self.obstacles:
                    if self.saad.winfo_exists() and self.canvas.winfo_exists():
                        obstacle_coords = self.canvas.coords(obstacle)

                        if player_head[0] == obstacle_coords[0] and player_head[1] == obstacle_coords[1]:
                            self.game_over("Game Over! Player snake collided with an obstacle.")
                            return

                # Check for collisions with boundaries for the AI's snake
                if ai_head[0] < 0 or ai_head[0] >= 400 or ai_head[1] < 0 or ai_head[1] >= 400:
                    self.game_over("Game Over! AI snake collided with the boundary.")

                # Check for collisions with itself for the AI's snake
                if ai_head in self.ai_snake.segments[1:]:
                    self.game_over("Game Over! AI snake collided with itself.")

                # Check for collisions with obstacles for the AI's snake
                for obstacle in self.obstacles:
                    if self.saad.winfo_exists() and self.canvas.winfo_exists():
                        obstacle_coords = self.canvas.coords(obstacle)
                        if ai_head[0] == obstacle_coords[0] and ai_head[1] == obstacle_coords[1]:
                            self.game_over("Game Over! AI snake collided with an obstacle.")
                            return

            # Redraw the snakes on the canvas
            self.canvas.delete("snake")
            self.player_snake.draw()
            self.ai_snake.draw()

            # Create food if it doesn't exist
            if self.food is None:
                self.food = self.create_food()

            # Check for food consumption by the player's snake
            if self.food:
                food_coords = self.canvas.coords(self.food)
                if player_head[0] == food_coords[0] and player_head[1] == food_coords[1]:
                    # Grow the player's snake and update the player's score
                    self.player_snake.grow()
                    self.canvas.delete("food")
                    self.food = None
                    self.player_score += 1
                    self.canvas.itemconfig(self.player_score_label, text=f"Player Score: {self.player_score}")

            # Check for food consumption by the AI's snake
            if self.food:
                food_coords = self.canvas.coords(self.food)
                if ai_head[0] == food_coords[0] and ai_head[1] == food_coords[1]:
                    # Grow the AI's snake and update the AI's score
                    self.ai_snake.grow()
                    self.canvas.delete("food")
                    self.food = None
                    self.ai_score += 1
                    self.canvas.itemconfig(self.ai_score_label, text=f"AI Score: {self.ai_score}")

            # Schedule the next update after 200 milliseconds
            self.saad.after(150, self.update)

    def change_direction(self, event):
        # Change the direction of the player's snake based on the key pressed
        self.player_snake.change_direction(event)

    def game_over(self, message="Game Over!"):
        # Handle the game over event, print the message, and close the window
        print(message)
        self.game_over_flag = True
        self.saad.destroy()

class Snake:
    def __init__(self, canvas, color, name, start_location):
        # Initialize the Snake instance
        self.canvas = canvas
        self.color = color
        self.segments = [start_location, (start_location[0] - 10, start_location[1]), (start_location[0] - 20, start_location[1])]
        self.direction = "Right"
        self.name = name

    def move(self):
        # Move the snake based on the current direction
        head = self.get_head()
        if self.direction == "Right":
            new_head = (head[0] + 10, head[1])
        elif self.direction == "Left":
            new_head = (head[0] - 10, head[1])
        elif self.direction == "Up":
            new_head = (head[0], head[1] - 10)
        elif self.direction == "Down":
            new_head = (head[0], head[1] + 10)

        # Insert the new head at the beginning of the segments list
        self.segments.insert(0, new_head)

        # Ensure the segments list doesn't grow beyond the expected size
        if len(self.segments) > 1:
            self.segments.pop()

    def draw(self):
        # Draw the snake on the canvas
        for segment in self.segments:
            self.canvas.create_rectangle(segment[0], segment[1], segment[0] + 10, segment[1] + 10, fill=self.color, tags="snake")

    def get_head(self):
        # Get the head of the snake (first segment)
        return self.segments[0]

    def change_direction(self, event):
        # Change the direction based on the key pressed
        if event.keysym == "Right" and not self.direction == "Left":
            self.direction = "Right"
        elif event.keysym == "Left" and not self.direction == "Right":
            self.direction = "Left"
        elif event.keysym == "Up" and not self.direction == "Down":
            self.direction = "Up"
        elif event.keysym == "Down" and not self.direction == "Up":
            self.direction = "Down"

    def grow(self):
        # Duplicate the tail to make the snake grow
        tail = self.segments[-1]
        self.segments.append(tail)

    def move_towards_food(self, food):
        # Move the snake towards the given food coordinates
        if food and self.canvas.coords(food):
            food_coords = self.canvas.coords(food)
            head = self.get_head()

            # Determine the relative position of the head and food
            dx = food_coords[0] - head[0]
            dy = food_coords[1] - head[1]

            # Adjust the direction based on the relative position of the head and food
            if dx > 0 and not self.direction == "Left":
                self.direction = "Right"
            elif dx < 0 and not self.direction == "Right":
                self.direction = "Left"
            elif dy > 0 and not self.direction == "Up":
                self.direction = "Down"
            elif dy < 0 and not self.direction == "Down":
                self.direction = "Up"

            # Move the snake
            self.move()

            # Check if the snake reaches the food and grow
            if head[0] == food_coords[0] and head[1] == food_coords[1]:
                self.grow()
                self.canvas.delete(food)

# Run the game when the script is executed
if __name__ == "__main__":
    root = tk.Tk()
    game = Snake_Game(root)
    root.mainloop()







