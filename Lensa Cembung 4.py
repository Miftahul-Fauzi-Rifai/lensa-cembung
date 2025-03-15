import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageDraw, ImageTk
import random

def create_tree_image():
    """Membuat gambar pohon setinggi 100 satuan."""
    img = Image.new("RGBA", (50, 100), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)
    draw.rectangle([20, 75, 30, 100], fill=(139, 69, 19))
    draw.polygon([5, 75, 25, 40, 45, 75], fill=(34, 139, 34))
    draw.polygon([10, 55, 25, 20, 40, 55], fill=(34, 139, 34))
    draw.polygon([15, 35, 25, 5, 35, 35], fill=(34, 139, 34))
    return np.array(img)

def draw_simulation(ax, obj_size, obj_dist, focal_length, obj_img):
    ax.clear()
    ax.axhline(0, color='black', linewidth=1)
    radius = 2 * focal_length
    ax.scatter([-focal_length, focal_length], [0, 0], color='r', marker='o', label='Titik Fokus')
    ax.scatter([-radius, radius], [0, 0], color='purple', marker='x', label='Titik Jari-jari')
    ax.plot([0, 0], [-200, 200], 'b-', linewidth=3, label='Lensa')
    
    obj_x = -obj_dist
    aspect_ratio = obj_img.shape[1] / obj_img.shape[0]
    obj_height = obj_size
    obj_width = obj_height * aspect_ratio
    ax.imshow(obj_img, extent=[obj_x - obj_width/2, obj_x + obj_width/2, 0, obj_height], aspect='auto')
    
    if obj_dist != focal_length:
        img_dist = 1 / (1/focal_length - 1/obj_dist)
        img_size = (-img_dist / obj_dist) * obj_size
        img_x = img_dist
        img_width_proj = img_size * aspect_ratio
        ax.imshow(obj_img, extent=[img_x - img_width_proj/2, img_x + img_width_proj/2, 0, img_size], aspect='auto', alpha=0.5)
        ax.plot([-obj_dist, 0], [obj_size, obj_size], 'r--', linewidth=1, label='Sinar 1')
        ax.plot([0, img_dist], [obj_size, img_size], 'r--', linewidth=1)
        ax.plot([-obj_dist, 0], [obj_size, img_size], 'm--', linewidth=1, label='Sinar 2')
        ax.plot([0, img_dist], [img_size, img_size], 'm--', linewidth=1)
        ax.plot([-obj_dist, img_dist], [obj_size, img_size], 'g--', linewidth=1, label='Sinar 3')
    
    ax.set_xlim(-500, 500)
    ax.set_ylim(-200, 200)
    ax.legend()
    ax.grid()
    canvas.draw()

def update(*args):
    obj_size = size_slider.get()
    obj_dist = distance_slider.get()
    focal_length = focus_slider.get()
    draw_simulation(ax, obj_size, obj_dist, focal_length, obj_img)

#def upload_image():
 #   global obj_img
  #  file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
   # if file_path:
    #    img = Image.open(file_path)
     #   img = img.convert("RGBA")
      #  obj_img = np.array(img)
       # update()

 # Efek latar belakang berubah warna
    bg_color = (1 - obj_dist / 400, 1, obj_dist / 400)
    ax.set_facecolor(bg_color)
    canvas.draw()


def reset_simulation():
    global obj_img
    obj_img = create_tree_image()
    size_slider.set(100)
    distance_slider.set(100)
    focus_slider.set(50)  # Reset ke titik fokus awal 50
    draw_simulation(ax, 100, 100, 50, obj_img)
    canvas.draw()
 # Pesan pop-up reset
    messages = ["Pohon kembali tumbuh!", "Dunia optik kembali normal!", "Reset berhasil, coba lagi!"]
    messagebox.showinfo("Reset Simulasi", random.choice(messages))

root = tk.Tk()
root.title("Simulasi Lensa Cembung dengan Pohon")
root.geometry("1200x700")
root.columnconfigure(1, weight=1)
root.rowconfigure(1, weight=1)

main_frame = tk.Frame(root)
main_frame.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

size_frame = tk.Frame(root)
size_frame.grid(row=1, column=0, sticky="ns")
size_slider = tk.Scale(size_frame, from_=10, to=200, orient="vertical", label="Ukuran Benda", command=update)
size_slider.pack(fill="y", expand=True)
size_slider.set(100)

distance_frame = tk.Frame(root)
distance_frame.grid(row=0, column=1, sticky="ew")
distance_slider = tk.Scale(distance_frame, from_=0, to=400, orient="horizontal", label="Jarak Benda", command=update)
distance_slider.pack(fill="x", expand=True)
distance_slider.set(100)

focus_frame = tk.Frame(root)
focus_frame.grid(row=2, column=1, sticky="ew")
focus_slider = tk.Scale(focus_frame, from_=50, to=200, orient="horizontal", label="Titik Fokus", command=update)
focus_slider.pack(fill="x", expand=True)

#upload_btn = tk.Button(root, text="Upload Gambar", command=upload_image)
#upload_btn.grid(row=3, column=1, pady=10)

reset_btn = tk.Button(root, text="Reset Simulasi", command=reset_simulation)
reset_btn.grid(row=4, column=1, pady=10)

obj_img = create_tree_image()

fig, ax = plt.subplots(figsize=(7, 5))
canvas = FigureCanvasTkAgg(fig, master=main_frame)
canvas.get_tk_widget().pack(fill="both", expand=True)

update()
root.mainloop()