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

        leftArrowImage = Image.open("ExistingImages/leftarrow.png")
        resizedLeftArrowImage = ImageTk.PhotoImage(leftArrowImage.resize((20, 20), Image.ANTIALIAS))
        rightArrowImage = Image.open("ExistingImages/rightarrow.png")
        resizedRightArrowImage = ImageTk.PhotoImage(rightArrowImage.resize((20, 20), Image.ANTIALIAS))

        leftArrowBtn = Button(self.display_window, image=resizedLeftArrowImage)
        leftArrowBtn.image = resizedLeftArrowImage
        rightArrowBtn = Button(self.display_window, image=resizedRightArrowImage)
        rightArrowBtn.image = resizedRightArrowImage

        leftArrowBtn.pack(side=LEFT, padx=15, pady=20)
        rightArrowBtn.pack(side=RIGHT, padx=15, pady=20)


    def set_welcome_window(self):
        existingImagesBtn = Button(self.display_window, text='Existing Images', command=lambda: self.existingImagesWindow(self.display_window))
        importImagesBtn = Button(self.display_window, text='Import Images')
        exitBtn = Button(self.display_window, text='Exit', command=self.display_window.destroy)

        existingImagesBtn.pack(side=LEFT, padx=15, pady=20)
        importImagesBtn.pack(side=RIGHT, padx=15, pady=20)
        exitBtn.pack(side=BOTTOM, padx=15, pady=20)