import pyxel
import random
import sqlite3

class SnakeGame:
    def __init__(self):
        pyxel.init(160, 160, title="Snake Game")
        pyxel.load("splot.pyxres")  # Cargar el archivo de recursos
        self.high_scores = []
        self.initials = ["A", "A", "A"]
        self.current_initial = 0
        self.setup_database()
        self.load_high_scores()
        self.state = "START"  # Estados posibles: START, PLAYING, GAME_OVER, ENTER_INITIALS
        self.speed = 5
        self.obstacles = []
        self.reset_game()
        self.setup_sounds()
        self.play_music(True, True, True)  # Iniciar la música en la pantalla inicial
        pyxel.run(self.update, self.draw)

    def setup_database(self):
        self.conn = sqlite3.connect('high_scores.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS scores
                              (score INTEGER, initials TEXT)''')
        self.conn.commit()

    def load_high_scores(self):
        self.cursor.execute('SELECT * FROM scores ORDER BY score DESC LIMIT 5')
        self.high_scores = self.cursor.fetchall()

    def save_high_scores(self):
        self.cursor.execute('DELETE FROM scores')
        for score, initials in self.high_scores:
            self.cursor.execute('INSERT INTO scores (score, initials) VALUES (?, ?)', (score, initials))
        self.conn.commit()

    def close_database(self):
        self.conn.close()

    def setup_sounds(self):
        pyxel.sounds[0].set(
            "c3e3g3c4", "t", "7", "vffn", 25
        )
        pyxel.sounds[1].set(
            "g2b2d3g3", "t", "7", "vffn", 25
        )
        pyxel.sounds[2].set(
            "e2e2c2g1 g1g1c2e2 d2d2d2g2 g2g2rr c2c2a1e1 e1e1a1c2 b1b1b1e2 e2e2rr",
            "p",
            "6",
            "vffn fnff vffs vfnn",
            25,
        )
        pyxel.sounds[3].set(
            "r a1b1c2 b1b1c2d2 g2g2g2g2 c2c2d2e2 f2f2f2e2 f2e2d2c2 d2d2d2d2 g2g2r r",
            "s",
            "6",
            "nnff vfff vvvv vfff svff vfff vvvv svnn",
            25,
        )
        pyxel.sounds[4].set(
            "c1g1c1g1 c1g1c1g1 b0g1b0g1 b0g1b0g1 a0e1a0e1 a0e1a0e1 g0d1g0d1 g0d1g0d1",
            "t",
            "7",
            "n",
            25,
        )
        pyxel.sounds[5].set(
            "f0c1f0c1 g0d1g0d1 c1g1c1g1 a0e1a0e1 f0c1f0c1 f0c1f0c1 g0d1g0d1 g0d1g0d1",
            "t",
            "7",
            "n",
            25,
        )
        pyxel.sounds[6].set(
            "f0ra4r f0ra4r f0ra4r f0f0a4r", "n", "6622 6622 6622 6422", "f", 25
        )
        pyxel.musics[0].set([2, 3, 4, 5, 6])

    def play_music(self, ch0, ch1, ch2):
        if ch0:
            pyxel.play(0, [0, 1], loop=True)
        else:
            pyxel.stop(0)
        if ch1:
            pyxel.play(1, [2, 3], loop=True)
        else:
            pyxel.stop(1)
        if ch2:
            pyxel.play(2, 4, loop=True)
        else:
            pyxel.stop(2)

    def reset_game(self):
        self.snake = [(8, 8), (8, 8), (8, 8)]  # La serpiente comienza con una longitud de 3
        self.snake_dir = (1, 0)  # Inicialmente se mueve a la derecha
        self.food = self.spawn_food()
        self.game_over = False
        self.score = 0
        self.obstacles = []

    def spawn_food(self):
        while True:
            food = (random.randint(0, 19) * 8, random.randint(0, 19) * 8)
            if food not in self.snake and food not in self.obstacles:
                return food

    def spawn_obstacles(self):
        for _ in range(5):
            while True:
                obstacle = (random.randint(0, 19) * 8, random.randint(0, 19) * 8)
                if obstacle not in self.snake and obstacle != self.food:
                    self.obstacles.append(obstacle)
                    break

    def update(self):
        if self.state == "START":
            if pyxel.btnp(pyxel.KEY_SPACE):
                self.state = "PLAYING"
                pyxel.stop()  # Detener la música de la pantalla inicial
            else:
                pyxel.playm(0, loop=True)
            return

        if self.state == "GAME_OVER":
            if pyxel.btnp(pyxel.KEY_R):
                self.state = "ENTER_INITIALS"
            return

        if self.state == "ENTER_INITIALS":
            self.update_initials()
            return

        if pyxel.frame_count % self.speed == 0:
            self.update_snake()

        if pyxel.btn(pyxel.KEY_LEFT) and self.snake_dir != (1, 0):
            self.snake_dir = (-1, 0)
        elif pyxel.btn(pyxel.KEY_RIGHT) and self.snake_dir != (-1, 0):
            self.snake_dir = (1, 0)
        elif pyxel.btn(pyxel.KEY_UP) and self.snake_dir != (0, 1):
            self.snake_dir = (0, -1)
        elif pyxel.btn(pyxel.KEY_DOWN) and self.snake_dir != (0, -1):
            self.snake_dir = (0, 1)

    def update_initials(self):
        if pyxel.btnp(pyxel.KEY_LEFT):
            self.initials[self.current_initial] = chr((ord(self.initials[self.current_initial]) - 65 - 1) % 26 + 65)
        elif pyxel.btnp(pyxel.KEY_RIGHT):
            self.initials[self.current_initial] = chr((ord(self.initials[self.current_initial]) - 65 + 1) % 26 + 65)
        elif pyxel.btnp(pyxel.KEY_UP):
            self.current_initial = (self.current_initial - 1) % 3
        elif pyxel.btnp(pyxel.KEY_DOWN):
            self.current_initial = (self.current_initial + 1) % 3
        elif pyxel.btnp(pyxel.KEY_RETURN):
            self.high_scores.append((self.score, "".join(self.initials)))
            self.high_scores = sorted(self.high_scores, reverse=True)[:5]
            self.save_high_scores()
            self.reset_game()
            self.state = "START"

    def update_snake(self):
        new_head = ((self.snake[0][0] + self.snake_dir[0] * 8) % 160,
                    (self.snake[0][1] + self.snake_dir[1] * 8) % 160)
        
        if new_head in self.snake or new_head in self.obstacles:
            self.game_over = True
            self.state = "GAME_OVER"
            pyxel.play(1, 1)  # Reproducir sonido de game over
            return

        self.snake = [new_head] + self.snake

        if new_head == self.food:
            self.food = self.spawn_food()
            self.score += 10
            pyxel.play(0, 0)  # Reproducir sonido de comer comida
            if self.score % 50 == 0:
                self.speed = max(1, self.speed - 1)  # Incrementar dificultad al hacer la serpiente más rápida
            if self.score == 80 or self.score % 50 == 0:
                self.spawn_obstacles()  # Generar obstáculos a partir de los 80 puntos y luego cada 50 puntos
        else:
            self.snake.pop()  # Remover la cola solo si no comió comida

    def draw(self):
        pyxel.cls(0)  # Cambia el color de fondo a negro

        if self.state == "START":
            self.draw_start_screen()
        elif self.state == "PLAYING":
            self.draw_playing_screen()
        elif self.state == "GAME_OVER":
            self.draw_game_over_screen()
        elif self.state == "ENTER_INITIALS":
            self.draw_enter_initials_screen()

    def draw_start_screen(self):
        pyxel.text(40, 60, "SNAKE GAME", pyxel.frame_count % 16)
        pyxel.text(25, 80, "Press SPACE to Start", 7)
        pyxel.rect(72, 88, 8, 8, 5)  # Cabeza de la serpiente (dark gray)
        pyxel.rect(80, 88, 8, 8, 5)  # Cuerpo de la serpiente (dark gray)
        pyxel.rect(88, 88, 8, 8, 5)  # Cuerpo de la serpiente (dark gray)
        pyxel.rect(96, 88, 8, 8, 8)  # Dibuja la comida como un rectángulo (red)
        pyxel.text(20, 150, "Creado por J.Acisclo | 2024", 7)  # Texto en la parte inferior

        pyxel.text(40, 100, "High Scores:", 7)
        for i, (score, initials) in enumerate(self.high_scores):
            pyxel.text(40, 110 + i * 10, f"{initials}: {score}", 7)

    def draw_playing_screen(self):
        for segment in self.snake:
            pyxel.rect(segment[0], segment[1], 8, 8, 11)  # Color de la serpiente verde (11)
        pyxel.rect(self.food[0], self.food[1], 8, 8, 8)  # Dibuja la comida como un rectángulo (red)
        
        for obstacle in self.obstacles:
            pyxel.blt(obstacle[0], obstacle[1], 0, 0, 0, 8, 8)  # Dibuja el sprite del obstáculo

        pyxel.text(5, 4, f"Score: {self.score}", 7)  # Color del texto blanco (white)

    def draw_game_over_screen(self):
        self.draw_playing_screen()
        pyxel.text(50, 70, "GAME OVER", pyxel.frame_count % 16)
        pyxel.text(40, 90, "Press 'R' to Enter Initials", 7)

    def draw_enter_initials_screen(self):
        pyxel.text(40, 60, "Enter Your Initials", 7)
        pyxel.text(40, 80, "Use Arrow Keys", 7)
        pyxel.text(40, 90, "Press Enter to Confirm", 7)

        for i in range(3):
            color = 7 if i == self.current_initial else 5
            pyxel.text(60 + i * 10, 110, self.initials[i], color)

    def __del__(self):
        self.close_database()

SnakeGame()
