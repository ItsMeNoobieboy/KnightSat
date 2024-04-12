import tkinter as tk
from PIL import Image, ImageTk
import io

from make_mask import make_mask
from create_outages import edit_image
from image_to_binary import image_to_binary

class DrawingApp:
    def __init__(self, master, background_path):
        self.master = master
        self.master.title("Drawing App")

        self.canvas_width = 500
        self.canvas_height = 500

        # Create a black canvas
        self.canvas = tk.Canvas(self.master, width=self.canvas_width, height=self.canvas_height)
        self.canvas.pack()

        # Load your background image here
        self.background_image = Image.open(background_path)
        self.background_photo = ImageTk.PhotoImage(self.background_image)

        # Place the image under the canvas
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.background_photo)

        self.setup_buttons()
        self.setup_events()

    def setup_buttons(self):
        self.save_button = tk.Button(self.master, text="Continue", command=self.generate_new)
        self.save_button.pack()

    def setup_events(self):
        self.canvas.bind("<B1-Motion>", self.draw)
        self.master.bind("<KeyPress-s>", self.generate_new)

    def draw(self, event):
        x, y = event.x, event.y
        r = 10
        self.canvas.create_oval(x-r, y-r, x+r, y+r, fill="#ff0000", outline="")

    def save_drawing(self, event=None):
        filename = "drawing.png"  # Specify the file path here
        self.canvas.postscript(file=filename + ".eps")
        img = Image.open(filename + ".eps")
        img.save(filename, "png")
        print("Drawing saved as", filename)

    def get_canvas_as_image(self):
        # Get the canvas content in PostScript format
        ps = self.canvas.postscript(colormode='color')

        # Use a BytesIO buffer to convert PS to PNG
        with io.BytesIO() as buffer:
            buffer.write(ps.encode('utf-8'))
            buffer.seek(0)
            with Image.open(buffer) as img:
                return img.convert('RGBA')
            
    def generate_new(self, event=None):
        mask = self.generate_mask()

        with_outages = edit_image(image_to_binary(self.background_image.copy().crop((0, 0, 1024, 1024))), image_to_binary(mask.copy().crop((0, 0, 1024, 1024))))
        with_outages.save("image_analysis/image_test_pairs/london/with_outages2.png")
        print("finished!")


    def generate_mask(self, event=None):
        return make_mask(self.get_canvas_as_image(), self.background_image)

def main():
    print("Which image would you like to use?")
    image_path = input()
    root = tk.Tk()
    app = DrawingApp(root, f"image_analysis/satelite_images/{image_path}")
    root.mainloop()

if __name__ == "__main__":
    main()