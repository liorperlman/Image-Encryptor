from tkinter import *
from PIL import Image, ImageTk

existing_images = []


class System (Frame):
    # Constructor without parameters
    def __init__(self, master):
        Frame.__init__(self, master)
        self.display_window = master
        self.set_window_settings('Image Encryptor Demo')
        self.set_welcome_window()

    def clean_and_rebuild(self, title):
        self.display_window.destroy()
        self.display_window = Tk()
        self.set_window_settings(title)

    def set_window_settings(self, title):
        self.display_window.resizable(False, False)
        self.display_window.geometry("350x350")
        self.display_window.title(title)

    def existingImagesWindow(self, master):
        self.clean_and_rebuild('Existing Images')

        leftImage = Image.open("ExistingImages/leftarrow.png")
        leftArrowImage = ImageTk.PhotoImage(leftImage.resize((50, 50), Image.ANTIALIAS))
        rightImage = Image.open("ExistingImages/rightarrow.png")
        rightArrowImage = ImageTk.PhotoImage(rightImage.resize((50, 50), Image.ANTIALIAS))

        leftBtn = Button(self.display_window, image=leftArrowImage)
        rightBtn = Button(self.display_window, image=rightArrowImage)

        leftBtn.pack(side=LEFT, padx=15, pady=20)
        rightBtn.pack(side=RIGHT, padx=15, pady=20)
        # master = Tk()
        # self.set_window_settings()
        # self.display_window.destroy()

    def set_welcome_window(self):
        existingImagesBtn = Button(self.display_window, text='Existing Images', command=lambda: self.existingImagesWindow(self.display_window))
        importImagesBtn = Button(self.display_window, text='Import Images')
        exitBtn = Button(self.display_window, text='Exit', command=self.display_window.destroy)

        existingImagesBtn.pack(side=LEFT, padx=15, pady=20)
        importImagesBtn.pack(side=RIGHT, padx=15, pady=20)
        exitBtn.pack(side=BOTTOM, padx=15, pady=20)