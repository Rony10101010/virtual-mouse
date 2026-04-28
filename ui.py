import tkinter as tk
from threading import Thread
import main


class VirtualMouseUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Virtual Mouse")
        self.master.geometry("450x350")
        self.master.resizable(False, False)

        self.thread_running = False

        tk.Label(master, text="Gesture Mouse", font=("Arial", 16)).pack(pady=10)

        self.status_label = tk.Label(master, text="Status: Idle", fg="blue", font=("Arial", 10))
        self.status_label.pack()

        tk.Button(master, text="Start", width=25, command=self.start_mouse).pack(pady=5)
        tk.Button(master, text="Exit", width=25, command=self.master.quit).pack(pady=5)

        tk.Label(master, text="🖱️ Gesture Controls", font=("Arial", 12, "underline")).pack(pady=10)

        gestures = [
            "Move      : Index finger only",
            "Click     : Index + Pinky",
            "Double    : Pinky",
            "Drag      : All fingers up",
            "RightClick: Thumb + Pinky"
        ]
        for gesture in gestures:
            tk.Label(master, text=gesture, font=("Arial", 9)).pack(anchor="w", padx=20)

    def start_mouse(self):
        if not self.thread_running:
            self.thread_running = True
            self.status_label.config(text="Status: Running", fg="green")
            Thread(target=main.start_mouse_control, daemon=True).start()


if __name__ == "__main__":
    root = tk.Tk()
    app = VirtualMouseUI(root)
    root.mainloop()
