import json
import os
import tkinter as tk
from tkinter import simpledialog, messagebox
from PIL import Image, ImageTk
import random
from image import generate_image

class PuzzleGame:
    def __init__(self, root, config):
        self.root = root
        self.config = config
        self.root.title("Puzzle Game")
        self.root.resizable(False, False)
        self.canvas = tk.Canvas(root)
        self.canvas.pack(fill="both", expand=True)
        self.steps = 0
        self.description = None
        self.tiles_count = None
        self.tile_size = None
        self.image = None
        self.start_game()

    def start_game(self):
        if self.config.get("use_saved_image", False):
            if os.path.exists(self.config["saved_image_path"]):
                self.image = Image.open(self.config["saved_image_path"])
            else:
                messagebox.showerror("Error", "Saved image not found!")
                self.root.destroy()
                return
        else:
            self.description = simpledialog.askstring("Input", "Describe the image:")
            if self.description is None:
                self.root.destroy()
                return
        
        # Ensure tiles_count is defined before being used.
        if self.tiles_count is None:
            self.tiles_count = simpledialog.askinteger("Input", "Enter number of tiles (width/height, 2-10):", minvalue=2, maxvalue=10)
            if self.tiles_count is None:
                self.root.destroy()
                return
        
        self.tile_size = 512 // max(self.tiles_count, 2)
        tile_size = self.tile_size
        
        if not self.config.get("use_saved_image", False):
            if self.config.get("high_speed_mode", False):
                tile_size //= 2
            self.image = generate_image(self.description + self.config["prompt_suffix"], self.tiles_count, tile_size, self.config)
            if self.config.get("high_speed_mode", False):
                tile_size *= 2
                self.image = self.image.resize((tile_size * self.tiles_count, tile_size * self.tiles_count), Image.ANTIALIAS)
                
        self.steps = 0
        self.selected_tile = None
        self.shuffle_tiles()
        self.root.geometry(f"{tile_size * self.tiles_count}x{tile_size * self.tiles_count}")
        self.draw_puzzle()

    def shuffle_tiles(self):
        self.tiles = [[None for _ in range(self.tiles_count)] for _ in range(self.tiles_count)]
        self.original_order = [[None for _ in range(self.tiles_count)] for _ in range(self.tiles_count)]

        for i in range(self.tiles_count):
            for j in range(self.tiles_count):
                tile_image = ImageTk.PhotoImage(self.image.crop((j * self.tile_size, i * self.tile_size, (j + 1) * self.tile_size, (i + 1) * self.tile_size)))
                self.tiles[i][j] = tile_image
                self.original_order[i][j] = tile_image

        flat_tiles = [(i, j) for i in range(self.tiles_count) for j in range(self.tiles_count)]
        random.shuffle(flat_tiles)

        for i in range(self.tiles_count):
            for j in range(self.tiles_count):
                x, y = flat_tiles.pop()
                self.tiles[i][j] = self.original_order[x][y]

    def draw_puzzle(self):
        self.canvas.delete("all")
        for i in range(len(self.tiles)):
            for j in range(len(self.tiles[i])):
                tile_image = self.tiles[i][j]
                self.canvas.create_image(j * self.tile_size, i * self.tile_size, anchor="nw", image=tile_image)
                if self.selected_tile == (i, j):
                    self.canvas.create_rectangle(j * self.tile_size, i * self.tile_size, (j + 1) * self.tile_size, (i + 1) * self.tile_size, outline="red", width=5)

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
            self.swap_tiles(self.selected_tile, (i, j))
            self.steps += 1
            if self.check_completion():
                self.draw_puzzle()
                self.root.update()
                play_again = messagebox.askyesno("Congratulations!", f"You've completed the puzzle in {self.steps} steps!\nDo you want to play again?")
                if play_again:
                    generate_new_image = messagebox.askyesno("New Image?", "Do you want to generate a new image?")
                    if generate_new_image:
                        self.description = None
                        self.tiles_count = None
                    self.start_game()
                else:
                    self.root.destroy()
        else:
            self.selected_tile = (i, j)
            self.draw_puzzle()

    def swap_tiles(self, tile1, tile2):
        self.tiles[tile1[0]][tile1[1]], self.tiles[tile2[0]][tile2[1]] = self.tiles[tile2[0]][tile2[1]], self.tiles[tile1[0]][tile1[1]]
        self.selected_tile = None
        self.draw_puzzle()

    def run(self):
        self.canvas.bind("<Button-1>", self.on_tile_click)
        self.root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()

    with open("config.json", "r") as file:
        config = json.load(file)

    game = PuzzleGame(root, config)
    game.run()
