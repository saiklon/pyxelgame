
Snake Game with Pyxel
Introduction
This is a classic Snake game developed using Pyxel, a retro game engine for Python. The game features simple mechanics where the player controls a snake to eat food, grow in length, and avoid obstacles. The objective is to score as many points as possible without colliding with the snake's own body or the obstacles.

Features
Classic Snake Gameplay: Control the snake using arrow keys to eat food and grow in length.
Obstacles: As the player progresses, obstacles appear on the game board to increase the difficulty.
High Scores: The game tracks high scores and allows players to enter their initials.
Sound and Music: Integrated sound effects and background music for an engaging experience.
Resource File: Uses a Pyxel resource file (splot.pyxres) for sprite graphics.
SQLite Database: High scores are stored in a SQLite database for robustness.
How to Play
Start the Game: Press the SPACE key to start the game from the title screen.
Control the Snake: Use the arrow keys to change the direction of the snake.
Eat Food: Move the snake to the food to eat it and grow in length. Each food item increases the score by 10 points.
Avoid Obstacles: As you reach certain scores, obstacles will appear on the game board. Avoid colliding with these obstacles.
Game Over: The game ends if the snake collides with itself or an obstacle. Press R to enter your initials for the high score list.
High Scores: The game saves and displays the top 5 high scores.
Code Structure
Main Components
Initialization: The game initializes the Pyxel environment, loads resources, and sets up the game state.
Game States: The game transitions between different states such as START, PLAYING, GAME_OVER, and ENTER_INITIALS.
Game Logic: Handles the snake movement, food spawning, obstacle generation, and collision detection.
Drawing Functions: Renders the game elements (snake, food, obstacles, and UI) on the screen.
Sound and Music: Plays sound effects and background music using Pyxel's sound and music capabilities.
Database Integration: Utilizes SQLite to store and retrieve high scores.
