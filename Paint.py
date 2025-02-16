import tkinter as tk
from tkinter import colorchooser
from tkinter import filedialog
from PIL import Image, ImageDraw, ImageTk

def paint(event):
    x1, y1 = (event.x - 2), (event.y - 2)
    x2, y2 = (event.x + 2), (event.y + 2)
    # Zeichnen auf dem Canvas
    canvas.create_oval(x1, y1, x2, y2, fill=color, outline=color, width=5)
    # Zeichnen auf dem ImageDraw-Objekt (für Speicherung und Lade-Funktion)
    draw.ellipse([x1, y1, x2, y2], fill=color, outline=color)

def choose_color():
    global color
    color = colorchooser.askcolor(color=color)[1]

def choose_bg_color():
    global bg_color
    bg_color = colorchooser.askcolor(color=bg_color)[1]
    canvas.config(bg=bg_color)
    # Leeres Bild mit neuer Hintergrundfarbe erstellen
    global image, draw
    image = Image.new("RGB", (1920, 1080), bg_color)
    draw = ImageDraw.Draw(image)
    # Bild mit neuer Hintergrundfarbe auf dem Canvas anzeigen
    img_tk = ImageTk.PhotoImage(image)
    canvas.create_image(0, 0, anchor=tk.NW, image=img_tk)
    canvas.image = img_tk  # Referenz halten

def clear_canvas():
    global draw, image
    # Canvas löschen
    canvas.delete("all")
    # Neues leeres Bild mit der Hintergrundfarbe erstellen
    image = Image.new("RGB", (1920, 1080), bg_color)
    draw = ImageDraw.Draw(image)
    # Das leere Bild auf dem Canvas anzeigen
    img_tk = ImageTk.PhotoImage(image)
    canvas.create_image(0, 0, anchor=tk.NW, image=img_tk)
    canvas.image = img_tk  # Referenz halten

def save_canvas():
    filename = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("All Files", "*.*")])
    if filename:
        image.save(filename)

def load_canvas():
    global image, draw, img_tk
    filename = filedialog.askopenfilename(filetypes=[("PNG files", "*.png"), ("All Files", "*.*")])
    if filename:
        # Bild laden und auf Canvas anzeigen
        image = Image.open(filename).resize((1920, 1080))
        draw = ImageDraw.Draw(image)
        img_tk = ImageTk.PhotoImage(image)
        canvas.create_image(0, 0, anchor=tk.NW, image=img_tk)
        canvas.image = img_tk  # Referenz halten

def set_color(new_color):
    global color
    color = new_color

root = tk.Tk()
root.title("Paint")

# Fenstergröße auf 2000x1150 setzen
window_width = 2000
window_height = 1150

# Zentrieren des Fensters auf dem Bildschirm
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
position_top = int(screen_height / 2 - window_height / 2)
position_left = int(screen_width / 2 - window_width / 2)
root.geometry(f'{window_width}x{window_height}+{position_left}+{position_top}')

color = "black"
bg_color = "white"  # Standard Hintergrundfarbe

# Die Canvas wird 1920x1080 Pixel groß und beginnt oben im Fenster
canvas = tk.Canvas(root, bg=bg_color, width=1920, height=1080)
canvas.pack()  # Kein Padding mehr, damit es ganz oben ist
canvas.bind("<B1-Motion>", paint)

toolbar = tk.Frame(root)
toolbar.pack()

color_btn = tk.Button(toolbar, text="Farbe wählen", command=choose_color)
color_btn.pack(side=tk.LEFT)

bg_color_btn = tk.Button(toolbar, text="Hintergrundfarbe wählen", command=choose_bg_color)
bg_color_btn.pack(side=tk.LEFT)

clear_btn = tk.Button(toolbar, text="Löschen", command=clear_canvas)
clear_btn.pack(side=tk.LEFT)

save_btn = tk.Button(toolbar, text="Speichern", command=save_canvas)
save_btn.pack(side=tk.LEFT)

load_btn = tk.Button(toolbar, text="Laden", command=load_canvas)
load_btn.pack(side=tk.LEFT)

# Initiales leeres Bild erstellen und ImageDraw-Objekt initialisieren
image = Image.new("RGB", (1920, 1080), bg_color)
draw = ImageDraw.Draw(image)

# Initiale Farbe für den Pinsel
color = "black"

root.mainloop()
