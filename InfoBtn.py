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


# # Example usage
# root = tk.Tk()
# root.geometry("300x200")
#
# info_image = tk.PhotoImage(file="info.png").subsample(4, 4)
# info_btn = InfoButton(root, image=info_image, text="Info", description="This is the description of the info button.")
# info_btn.configure(bg="#2196F3", fg="white", font=("Arial", 10, "bold"), compound="left", padx=10, pady=5)
# info_btn.pack(pady=20)
#
# root.mainloop()
