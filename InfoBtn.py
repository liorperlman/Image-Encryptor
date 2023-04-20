import tkinter as tk


class InfoButton(tk.Button):
    def __init__(self, master, description, **kwargs):
        super().__init__(master, **kwargs)
        self.description = description
        self.bind("<Enter>", self.show_description)
        self.bind("<Leave>", self.hide_description)

    def show_description(self, event):
        self.description_window = tk.Toplevel()
        self.description_window.geometry("+{}+{}".format(event.x_root, event.y_root))
        self.description_window.overrideredirect(True)
        self.description_window.configure(bg="#F0F0F0", bd=1, relief="solid")

        description_label = tk.Label(self.description_window, text=self.description, bg="#F0F0F0", fg="black",
                                     font=("Arial", 9), padx=5, pady=2, justify="left")
        description_label.pack()

    def hide_description(self, event):
        self.description_window.destroy()