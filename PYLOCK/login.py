import tkinter as tk

root = tk.Tk()
root.title("PyLock")

frame_container = tk.Frame(root, bg="black")  # Use your preferred background
frame_container.pack(pady=50)

tk.Label(frame_container, text="Enter username:", fg="green", bg="black").pack()
tk.Entry(frame_container).pack()

tk.Label(frame_container, text="Enter password:", fg="green", bg="black").pack()
tk.Entry(frame_container, show="*").pack()

tk.Button(frame_container, text="Sign in", bg="green", fg="black").pack()

root.mainloop()
