import tkinter as tk

# Define colors
colors = {
    'primary': '#39FF14',    # Neon green
    'secondary': '#1F1F1F',  # Dark gray
    'bg_dark': '#000000',    # Pure black
    'bg_light': '#0A0A0A',   # Slightly lighter black
    'text': '#FFFFFF',       # White text
    'input_bg': '#121212',   # Dark input background
    'border': '#32CD32',     # Neon green border
    'error': '#FF0033',      # Bright red
    'hover': '#39FF14'       # Lighter green for hover
}

# Create main window
root = tk.Tk()
root.title("Color Theme Preview")
root.configure(bg=colors['bg_dark'])
root.geometry("400x400")

# Add Labels for Colors
for idx, (key, value) in enumerate(colors.items()):
    frame = tk.Frame(root, bg=value, width=380, height=40)
    frame.place(x=10, y=10 + (idx * 45))
    label = tk.Label(frame, text=f"{key}: {value}", fg=colors['text'], bg=value, font=("Arial", 12, "bold"))
    label.pack(pady=10)

# Run the app
root.mainloop()
