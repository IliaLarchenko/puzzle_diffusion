import tkinter as tk
from tkinter import simpledialog, messagebox
from PIL import Image, ImageTk
import random
from image import generate_image

class PuzzleGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Puzzle Game")
        self.canvas = tk.Canvas(root)
        self.canvas.pack(fill="both", expand=True)
        self.steps = 0
        self.start_game()

    def start_game(self):
        description = simpledialog.askstring("Input", "Describe the image:")
        tiles = simpledialog.askinteger("Input", "Enter number of tiles (width/height, 2-10):", minvalue=2, maxvalue=10)
        tile_size = 512 // max(tiles, 2)
        image = generate_image(description, tiles, tile_size)
        self.tiles = [[None for _ in range(tiles)] for _ in range(tiles)]
        self.original_order = [[None for _ in range(tiles)] for _ in range(tiles)]
        self.tile_size = tile_size
        self.selected_tile = None
        self.steps = 0

        for i in range(tiles):
            for j in range(tiles):
                tile_image = ImageTk.PhotoImage(image.crop((j * tile_size, i * tile_size, (j + 1) * tile_size, (i + 1) * tile_size)))
                self.tiles[i][j] = tile_image
                self.original_order[i][j] = tile_image

        flat_tiles = [(i, j) for i in range(tiles) for j in range(tiles)]
        random.shuffle(flat_tiles)

        for i in range(tiles):
            for j in range(tiles):
                x, y = flat_tiles.pop()
                self.tiles[i][j] = self.original_order[x][y]

        self.root.geometry(f"{tile_size * tiles}x{tile_size * tiles}")
        self.draw_puzzle()

    def draw_puzzle(self):
        self.canvas.delete("all")
        for i in range(len(self.tiles)):
            for j in range(len(self.tiles[i])):
                tile_image = self.tiles[i][j]
                self.canvas.create_image(j * self.tile_size, i * self.tile_size, anchor="nw", image=tile_image)
                if self.selected_tile == (i, j):
                    self.canvas.create_rectangle(j * self.tile_size, i * self.tile_size, (j + 1) * self.tile_size, (i + 1) * self.tile_size, outline="red", width=5)

    def swap_tiles(self, tile1, tile2):
        self.tiles[tile1[0]][tile1[1]], self.tiles[tile2[0]][tile2[1]] = self.tiles[tile2[0]][tile2[1]], self.tiles[tile1[0]][tile1[1]]
        self.selected_tile = None
        self.draw_puzzle()

    def check_completion(self):
        for i in range(len(self.tiles)):
            for j in range(len(self.tiles[i])):
                if self.tiles[i][j] != self.original_order[i][j]:
                    return False
        return True

    def on_tile_click(self, event):
        i = event.y // self.tile_size
        j = event.x // self.tile_size
        if self.selected_tile:
            if abs(self.selected_tile[0] - i) + abs(self.selected_tile[1] - j) == 1:
                self.swap_tiles(self.selected_tile, (i, j))
                self.steps += 1
                if self.check_completion():
                    self.draw_puzzle()
                    self.root.update()
                    messagebox.showinfo("Congratulations!", f"You've completed the puzzle in {self.steps} steps!\nDo you want to play again?")
                    self.start_game()
        else:
            self.selected_tile = (i, j)
            self.draw_puzzle()

    def run(self):
        self.canvas.bind("<Button-1>", self.on_tile_click)
        self.root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    game = PuzzleGame(root)
    game.run()
