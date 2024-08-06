import tkinter as tk
from tkinter import messagebox
import pygame
from pynput.keyboard import Controller, Key

pygame.init()

pygame.joystick.init()
if pygame.joystick.get_count() > 0:
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
else:
    messagebox.showerror("Error", "No joystick connected")
    pygame.quit()
    exit()

keyboard = Controller()

# Mapping joystick buttons to keyboard keys
button_key_map = {
    0: Key.space,  # Example: Button 0 maps to the spacebar
    1: 'a',        # Example: Button 1 maps to the 'a' key
    2: 'd',        # Example: Button 2 maps to the 'd' key
}

# Mapping joystick axis to keyboard keys
axis_key_map = {
    0: ('left', 'right'),  # Example: Axis 0 maps to left and right arrow keys
    1: ('up', 'down'),     # Example: Axis 1 maps to up and down arrow keys
}

# Function Events
def press_key(key):
    keyboard.press(key)
    keyboard.release(key)

def handle_button_event(button, pressed):
    if button in button_key_map:
        key = button_key_map[button]
        if pressed:
            keyboard.press(key)
        else:
            keyboard.release(key)

def handle_axis_event(axis, value):
    if axis in axis_key_map:
        negative_key, positive_key = axis_key_map[axis]
        if value < -0.5:
            press_key(negative_key)
        elif value > 0.5:
            press_key(positive_key)

def joystick_loop():
    for event in pygame.event.get():
        if event.type == pygame.JOYBUTTONDOWN:
            handle_button_event(event.button, True)
        elif event.type == pygame.JOYBUTTONUP:
            handle_button_event(event.button, False)
        elif event.type == pygame.JOYAXISMOTION:
            handle_axis_event(event.axis, event.value)
    root.after(10, joystick_loop)

# update mappings
def update_mappings():
    try:
        button_key_map[int(entry_button.get())] = entry_key.get()
        axis_key_map[int(entry_axis.get())] = (entry_axis_negative.get(), entry_axis_positive.get())
        messagebox.showinfo("Success", "Mappings updated successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to update mappings: {e}")

# UI
root = tk.Tk()
root.title("J2K")

frame_buttons = tk.Frame(root)
frame_buttons.pack(pady=10)

tk.Label(frame_buttons, text="Button:").grid(row=0, column=0)
entry_button = tk.Entry(frame_buttons)
entry_button.grid(row=0, column=1)

tk.Label(frame_buttons, text="Key:").grid(row=0, column=2)
entry_key = tk.Entry(frame_buttons)
entry_key.grid(row=0, column=3)

# axis mapping
frame_axis = tk.Frame(root)
frame_axis.pack(pady=10)

tk.Label(frame_axis, text="Axis:").grid(row=1, column=0)
entry_axis = tk.Entry(frame_axis)
entry_axis.grid(row=1, column=1)

tk.Label(frame_axis, text="Negative Key:").grid(row=1, column=2)
entry_axis_negative = tk.Entry(frame_axis)
entry_axis_negative.grid(row=1, column=3)

tk.Label(frame_axis, text="Positive Key:").grid(row=1, column=4)
entry_axis_positive = tk.Entry(frame_axis)
entry_axis_positive.grid(row=1, column=5)

button_update = tk.Button(root, text="Update Mappings", command=update_mappings)
button_update.pack(pady=20)

root.after(10, joystick_loop)
root.protocol("WM_DELETE_WINDOW", root.quit)
root.mainloop()

pygame.quit()
