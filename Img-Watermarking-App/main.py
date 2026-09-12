from tkinter import *
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk, ImageDraw, ImageFont
from tkinter.colorchooser import askcolor
import os

FONT_NAME = "Monospace"
uploaded_image = None  # Global variable to store the uploaded PIL image

watermark_added = False

def load_icon(image, size=(30, 30)):
    img = Image.open(f"assets/{image}.png")
    img = img.resize(size)
    return ImageTk.PhotoImage(img)

def upload_img():
    global uploaded_image, original_image, watermark_added

    # Open file dialog to upload an image
    image_path = filedialog.askopenfilename(
        filetypes=[("All Files", "*.*"),("Image Files", "*.png;*.jpg;*.jpeg;*.gif")]
    )

    if image_path:
        try:
            uploaded_image = Image.open(image_path)
            original_image = uploaded_image.copy()  # Save the original image for reset
            watermark_added = False  # Reset watermark status

            # Update image display
            preview_image = uploaded_image.copy()
            preview_image.thumbnail((300, 300))  # Resize preview
            img_display = ImageTk.PhotoImage(preview_image)
            img_label.config(image=img_display)
            img_label.image = img_display

            # Show the reset button
            reset_btn.grid(row=3, column=1, padx=50, pady=10, columnspan=2)  # Only show the reset button when image is uploaded
        except Exception as e:
            messagebox.showerror("Error", f"Failed to upload image: {e}")


def get_text_input():
    if uploaded_image:
        text_input_window = Toplevel(window)
        text_input_window.title("Add Text Watermark")

        label = Label(text_input_window, text="Enter Watermark Text:", font=(FONT_NAME, 12, "bold"))
        label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        text_input = Entry(text_input_window, width=30, font=(FONT_NAME, 15))
        text_input.focus()
        text_input.grid(row=1, column=0, padx=10, pady=10, sticky="w")

        # Default color (white)
        watermark_color = "#FFFFFF"

        def choose_color():
            nonlocal watermark_color
            color_code = askcolor(title="Choose Text Color")[1]
            if color_code:  
                watermark_color = color_code  # Update the selected color
                color_btn.config(bg=watermark_color)  # Change button background

        # Color Picker Button
        color_label = Label(text_input_window, text="Text Color:", font=(FONT_NAME, 12, "bold"))
        color_label.grid(row=2, column=0,padx=10, pady=10, sticky="w")
        
        color_btn = Button(text_input_window, text="Pick Color", command=choose_color, bg=watermark_color, font=(FONT_NAME, 12, "bold"))
        color_btn.grid(row=2, column=0, padx=10, pady=10)

        # Position Selector
        position_label = Label(text_input_window, text="Select Watermark Position:", font=(FONT_NAME, 12, "bold"))
        position_label.grid(row=4, column=0, padx=10, pady=10, sticky="w")

        position_var = StringVar(value="bottom-right")  # Default position

        positions = [
            ("Top Left", "top-left"),
            ("Top Right", "top-right"),
            ("Bottom Left", "bottom-left"),
            ("Bottom Right", "bottom-right"),
            ("Center", "center"),
        ]

        for text, value in positions:
            Radiobutton(
                text_input_window, text=text, variable=position_var, value=value, font=(FONT_NAME, 10)
            ).grid(sticky="w", padx=10)

        def submit_input():
            watermark_text = text_input.get()
            watermark_position = position_var.get()
            text_input_window.destroy()

            if watermark_text:
                text_watermark(watermark_text, watermark_color, watermark_position)

        submit_btn = Button(
            text_input_window, 
            text="Submit", 
            command=submit_input, 
            font=(FONT_NAME, 15, "bold"),
            activebackground="blue",
            activeforeground="white",
            cursor="hand2",
            highlightthickness=0
        )
        submit_btn.grid(row=10, column=0, pady=10)

    else:
        messagebox.showerror("Image not found", "Please select an image first!")

def text_watermark(watermark_text, watermark_color, position):
    global uploaded_image, watermark_added

    if not watermark_text:
        messagebox.showerror("Error", "Please enter a watermark text!")
        return

    if uploaded_image:
        watermarked_image = uploaded_image.copy()  # Work on a copy
        width, height = watermarked_image.size
        draw = ImageDraw.Draw(watermarked_image)

        try:
            font = ImageFont.truetype("courier", 40)  # Dynamic font size
        except IOError:
            font = ImageFont.load_default(size=60)

        padding = 50
        bbox = draw.textbbox((0, 0), watermark_text, font=font)
        text_width, text_height = bbox[2] - bbox[0], bbox[3] - bbox[1]

        positions = {
            "top-left": (padding, padding),
            "top-right": (width - text_width - padding, padding),
            "bottom-left": (padding, height - text_height - padding),
            "bottom-right": (width - text_width - padding, height - text_height - padding),
            "center": ((width - text_width) // 2, (height - text_height) // 2),
        }
        text_position = positions.get(position, "bottom-right")

        draw.text(text_position, watermark_text, font=font, fill=watermark_color)

        # Update original image but keep preview size the same
        uploaded_image = watermarked_image

        # Display a resized preview (thumbnail only for GUI)
        preview_image = watermarked_image.copy()
        preview_image.thumbnail((300, 300))  # Keep preview small
        img_display = ImageTk.PhotoImage(preview_image)
        img_label.config(image=img_display)
        img_label.image = img_display

        watermark_added = True


def select_logo():
    global uploaded_image

    if not uploaded_image:
        messagebox.showerror("Error", "Please upload an image first!")
        return

    # Open new window
    logo_window = Toplevel(window)
    logo_window.title("Add Logo Watermark")

    # Label for selecting logo
    logo_label = Label(logo_window, text="Select Logo Image:", font=(FONT_NAME, 12, "bold"))
    logo_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

    # Canvas to display logo preview
    canvas_width, canvas_height = 80, 80  # Small square preview
    canvas = Canvas(logo_window, width=canvas_width, height=canvas_height, bg="white", relief="solid", bd=1)
    canvas.grid(row=3, column=0, padx=10, pady=10)

    def browse_logo():
        nonlocal logo_path, logo_image
        logo_path = filedialog.askopenfilename(
            filetypes=[("All Files", "*.*"), ("Image Files", "*.png;*.jpg;*.jpeg;*.gif")]
        )
        if logo_path:
            logo_entry.delete(0, "end")
            logo_entry.insert(0, logo_path)

            # Open the logo image
            logo_img = Image.open(logo_path)
            
            # Resize the logo while keeping aspect ratio within square bounds
            logo_img.thumbnail((canvas_width, canvas_height))

            # Convert image to Tkinter format
            logo_image = ImageTk.PhotoImage(logo_img)

            # Clear previous image and display new one centered
            canvas.delete("all")
            canvas.create_image(canvas_width // 2, canvas_height // 2, image=logo_image, anchor="center")

    logo_path = ""
    logo_image = None

    # Entry field for the selected logo path
    logo_entry = Entry(logo_window, width=20, font=(FONT_NAME, 12))
    logo_entry.grid(row=1, column=0, padx=10, pady=10)

    # Browse button
    browse_btn = Button(logo_window, text="Browse", command=browse_logo, font=(FONT_NAME, 12, "bold"))
    browse_btn.grid(row=1, column=2, padx=10, pady=10, sticky="w")

    # Position Selection
    position_label = Label(logo_window, text="Select Position:", font=(FONT_NAME, 12, "bold"))
    position_label.grid(row=4, column=0, padx=10, pady=10, sticky="w")

    position_var = StringVar()
    position_dropdown = ttk.Combobox(
        logo_window, textvariable=position_var, values=["top-left", "top-right", "bottom-left", "bottom-right", "center"], font=(FONT_NAME, 12)
    )
    position_dropdown.grid(row=5, column=0, padx=10, pady=10, sticky="w", columnspan=2)
    position_dropdown.current(3)  # Default to bottom-right

    # Function to apply the logo watermark
    def apply_logo():
        global uploaded_image, watermark_added

        if not uploaded_image:
            messagebox.showerror("Error", "Please upload an image first!")
            return

        if not logo_path:
            messagebox.showerror("Error", "Please select a logo image!")
            return

        try:
            logo = Image.open(logo_path).convert("RGBA")
            logo_size = max(100, uploaded_image.size[0] // 5)  # Scale logo size based on image width
            logo.thumbnail((logo_size, logo_size))

            width, height = uploaded_image.size
            logo_width, logo_height = logo.size
            padding = 10  # Adjust padding from edges

            # Define positions
            positions = {
                "top-left": (padding, padding),
                "top-right": (width - logo_width - padding, padding),
                "bottom-left": (padding, height - logo_height - padding),
                "bottom-right": (width - logo_width - padding, height - logo_height - padding),
                "center": ((width - logo_width) // 2, (height - logo_height) // 2),
            }
            logo_position = positions.get(position_var.get(), "bottom-right")

            # Paste logo onto the image
            uploaded_image.paste(logo, logo_position, logo)

            # Update displayed preview (thumbnail only)
            preview_image = uploaded_image.copy()
            preview_image.thumbnail((300, 300))
            img_display = ImageTk.PhotoImage(preview_image)
            img_label.config(image=img_display)
            img_label.image = img_display

            watermark_added = True
            logo_window.destroy()  # Close window after applying watermark

        except Exception as e:
            messagebox.showerror("Error", f"Failed to apply logo: {e}")

    # Apply Button
    apply_btn = Button(
        logo_window, 
        text="Apply", 
        command=apply_logo, 
        font=(FONT_NAME, 15, "bold"),
        activebackground="black",
        activeforeground="white",
        cursor="hand2",
        highlightthickness=0
    )
    apply_btn.grid(row=7, column=1, padx=10, pady=10, sticky="ew", columnspan=3)

def save_image():
    global uploaded_image, watermark_added

    if uploaded_image:
        if not watermark_added:
            messagebox.showerror("Error", "No watermark added! Please add a watermark before saving.")
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG Files", "*.png"), ("JPEG Files", "*.jpg"), ("BMP Files", "*.bmp"), ("GIF Files", "*.gif"), ("All Files", "*.*")]
        )

        if file_path:
            file_extension = os.path.splitext(file_path)[1].lower()

            if file_extension in [".jpg", ".jpeg"]:
                uploaded_image.convert("RGB").save(file_path, quality=95)  # Preserve JPEG quality
            elif file_extension == ".png":
                uploaded_image.save(file_path, format="PNG", compress_level=0)  # Lossless PNG
            else:
                uploaded_image.save(file_path)  # Default save

            messagebox.showinfo("Success", "Image saved successfully!")
    else:
        messagebox.showerror("Error", "No image to save! Please upload and watermark an image first.")

def reset_image():
    global uploaded_image, original_image, watermark_added

    if original_image:
        uploaded_image = original_image.copy()  # Restore the original image
        watermark_added = False  # Reset watermark status

        # Update the image preview
        preview_image = uploaded_image.copy()
        preview_image.thumbnail((300, 300))
        img_display = ImageTk.PhotoImage(preview_image)
        img_label.config(image=img_display)
        img_label.image = img_display

        messagebox.showinfo("Reset", "Image has been reset!")


window = Tk()
window.title("Image Watermarking App")
window.config(padx=25, pady=25, bg="white")

# Title Label
title_label = Label(text="Add a Watermark to Image", font=(FONT_NAME, 25, "bold"), bg="white")
title_label.grid(column=1, row=0, columnspan=2)

# Upload Image Button
upload_icon = load_icon("upload_img")

upload_img_btn = Button(
    image=upload_icon,  
    compound="left",
    text="Upload Image",
    command=upload_img,  
    activebackground="blue",
    activeforeground="white",
    anchor="center",
    cursor="hand2",
    overrelief="raised",
    padx=10,
    pady=10,
    font=(FONT_NAME, 15, "bold"),
    highlightthickness=0,
    bg="white"
)
upload_img_btn.grid(column=1, row=1, pady=20, columnspan=2)

# Image Display
img_label = Label(window, bg="white")
img_label.grid(column=1, row=2, pady=20, columnspan=2)

reset_icon = load_icon("reset_img", size=(20, 20))

reset_btn = Button(
    window,
    image=reset_icon,  
    compound="left", 
    text="Reset Image", 
    command=reset_image, 
    font=(FONT_NAME, 12, "bold"),
    activebackground="red",
    activeforeground="white",
    anchor="center",
    cursor="hand2",
    overrelief="raised",
    highlightthickness=0,
    bg="white"
)
reset_btn.grid(row=2, column=1, padx=10, pady=10)
reset_btn.grid_forget()

# Watermark Label
watermark_label = Label(text="Choose the Watermark Type", font=(FONT_NAME, 15, "bold"), bg="white")
watermark_label.grid(column=1, row=5, pady=15, columnspan=2)

# Text Button
text_btn = Button(
    text="Text",
    command=get_text_input,  
    activebackground="black",
    activeforeground="white",
    anchor="center",
    cursor="hand2",
    overrelief="raised",
    padx=10,
    pady=10,
    font=(FONT_NAME, 15, "bold"),
    highlightthickness=0,
    bg="white"
)

# Logo Button
logo_btn = Button(
    text="Logo",
    command=select_logo,  
    activebackground="black",
    activeforeground="white",
    anchor="center",
    cursor="hand2",
    overrelief="raised",
    padx=10,
    pady=10,
    font=(FONT_NAME, 15, "bold"),
    highlightthickness=0,
    bg="white"
)

# Grid layout for "Text" and "Logo" buttons under the watermark label
text_btn.grid(column=1, row=6, padx=5, pady=5, sticky='ew')
logo_btn.grid(column=2, row=6, padx=5, pady=5, sticky='ew')

save_icon = load_icon("save_img")

save_btn = Button(
    image=save_icon,  
    compound="left",
    text="Save Image",
    command=save_image,
    activebackground="green",
    activeforeground="white",
    anchor="center",
    cursor="hand2",
    overrelief="raised",
    padx=10,
    pady=10,
    font=(FONT_NAME, 15, "bold"),
    highlightthickness=0,
    bg="white"
)
save_btn.grid(column=1, row=7, pady=20, columnspan=2)

window.mainloop()
