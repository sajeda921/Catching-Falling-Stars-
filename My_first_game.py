import tkinter as tk
import random

class FallingStarsGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Catch Falling Stars")
        self.root.geometry("500x500")
        self.canvas = tk.Canvas(root, width=500, height=500)
        self.canvas.pack()

        # Variables for the catcher
        self.catcher_width = 60
        self.catcher_height = 20
        self.catcher_x = 220
        self.catcher = None

        # List to store the current falling stars and their speeds
        self.stars = []

        # Score and label
        self.score = 0
        self.high_score = 0  # Variable to store the highest score
        self.score_label = tk.Label(root, text=f"Score: {self.score}", font=('Helvetica', 14), bg='black', fg='white')
        self.score_label.place(x=10, y=10)  # Position the score label in the top-left corner

        # Highest score label
        self.high_score_label = tk.Label(root, text=f"High Score: {self.high_score}", font=('Helvetica', 14), bg='black', fg='white')
        self.high_score_label.place(x=350, y=10)  # Position the high score label in the top-right corner

        # Key bindings
        self.root.bind("<Left>", self.move_left)
        self.root.bind("<Right>", self.move_right)

        # Flag to track if the game is over
        self.game_over = False

        # Start the game loop
        self.restart_button = None  # Initially set the restart button to None
        self.start_game()

    def start_game(self):
        """Initialize or reset the game."""
        self.canvas.delete("all")  # Clear the canvas
        self.draw_background_gradient()  # Draw the background
        self.draw_background_stars()  # Draw static stars in the background

        # Reset the score and position
        self.score = 0
        self.score_label.config(text=f"Score: {self.score}")

        self.catcher_x = 220
        self.catcher = self.canvas.create_rectangle(self.catcher_x, 480, self.catcher_x + self.catcher_width, 480 + self.catcher_height, fill=self.random_color())

        self.stars = []  # Clear the falling stars
        self.game_over = False  # Reset game over flag

        # Hide restart button if it's visible
        if self.restart_button:
            self.restart_button.place_forget()  # Hide the restart button

        self.create_star()  # Create the first star
        self.update_game()  # Start the falling stars

    def draw_background_gradient(self):
        """Draw a black gradient background on the canvas."""
        for i in range(500):
            # Calculate the gray level (0 to 255)
            gray_level = int((i / 500) * 255)
            color = f"#{gray_level:03x}{gray_level:03x}{gray_level:03x}"
            self.canvas.create_line(0, i, 500, i, fill=color)

    def random_color(self):
        """Generate a bright RGB color."""
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        return f"#{r:02x}{g:02x}{b:02x}"

    def draw_background_stars(self):
        """Draw random static stars in the background with random colors."""
        for _ in range(100):
            x = random.randint(0, 500)
            y = random.randint(0, 500)
            size = random.randint(1, 3)
            color = self.random_color()
            self.canvas.create_oval(x, y, x + size, y + size, fill=color, outline=color)

    def move_left(self, event):
        """Move the catcher left."""
        if not self.game_over and self.catcher_x > 0:
            self.catcher_x -= 20
            self.canvas.coords(self.catcher, self.catcher_x, 480, self.catcher_x + self.catcher_width, 480 + self.catcher_height)

    def move_right(self, event):
        """Move the catcher right."""
        if not self.game_over and self.catcher_x < 440:
            self.catcher_x += 20
            self.canvas.coords(self.catcher, self.catcher_x, 480, self.catcher_x + self.catcher_width, 480 + self.catcher_height)

    def create_star(self):
        """Create a falling star with a random color and speed."""
        x = random.randint(20, 480)
        y = random.randint(-150, -50)
        speed = random.randint(10, 20)  # Random speed between 10 and 20
        # Define a star shape with 5 points (to look like a star)
        star_points = [
            x, y - 15,  # Top point
            x + 5, y - 5,  # Upper-right point
            x + 15, y - 5,  # Right point
            x + 7, y + 5,  # Lower-right point
            x + 10, y + 15,  # Right-bottom point
            x, y + 10,  # Bottom point
            x - 10, y + 15,  # Left-bottom point
            x - 7, y + 5,  # Lower-left point
            x - 15, y - 5,  # Left point
            x - 5, y - 5  # Upper-left point
        ]
        color = self.random_color()
        star = {"star": self.canvas.create_polygon(star_points, fill=color, outline=color), "speed": speed}
        self.stars.append(star)

    def update_game(self):
        """Update the position of the falling stars and check for collisions."""
        if self.game_over:
            return  # Stop the game loop if the game is over
        
        for star in self.stars[:]:
            self.canvas.move(star["star"], 0, star["speed"])  # Move the current star according to its speed
            star_coords = self.canvas.coords(star["star"])

            # If the star falls off the screen, create a new one
            if star_coords[1] > 500:
                self.canvas.delete(star["star"])
                self.stars.remove(star)
                self.create_star()
                self.game_over = True
                self.display_game_over()  # Display Game Over if a star falls off the screen

            # Check for collision with the catcher
            if (star_coords[2] > self.catcher_x and star_coords[0] < self.catcher_x + self.catcher_width) and star_coords[3] >= 480:
                self.score += 1
                self.canvas.delete(star["star"])
                self.stars.remove(star)
                self.create_star()

        # Update score label
        self.score_label.config(text=f"Score: {self.score}")

        # Update highest score if the current score exceeds it
        if self.score > self.high_score:
            self.high_score = self.score
            self.high_score_label.config(text=f"Highest Score: {self.high_score}")

        # Continue the game loop
        self.root.after(50, self.update_game)

    def display_game_over(self):
        """Display the Game Over message in the center of the screen."""
        self.canvas.create_text(250, 250, text="GAME OVER", font=('Helvetica', 30), fill="red")
        
        # Create the restart button only when game over occurs
        self.restart_button = tk.Button(self.root, text="Restart", font=('Helvetica', 14), command=self.restart_game)
        self.restart_button.place(x=200, y=300)  # Position the restart button below GAME OVER

    def restart_game(self):
        """Restart the game when the restart button is pressed."""
        self.restart_button.place_forget()  # Hide the restart button when restarting the game
        self.start_game()  # Start a new game

# Create the main window and start the game
root = tk.Tk()
game = FallingStarsGame(root)
root.mainloop()
