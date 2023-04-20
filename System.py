from tkinter import *
from tkinter import filedialog
from tkinter.filedialog import askopenfile
from PIL import Image, ImageTk
import os
import shutil

class System (Frame):
    existing_images = []
    current_image = 0
    images_number = 0
    
    def __init__(self, master):
        Frame.__init__(self, master)
        self.display_window = master
        self.set_window_settings('Image Encryptor Demo')
        self.set_welcome_window()
        self.update_images_number()

    def clean_and_rebuild(self, title):
        self.display_window.destroy()
        self.display_window = Tk()
        self.load_initial_images()
        self.set_window_settings(title)

    def set_window_settings(self, title):
        self.display_window.resizable(False, False)
        self.display_window.geometry("350x370")
        self.display_window.title(title)
    
    def update_images_number(self):
        self.images_number = 0
        for file in os.listdir('ExistingImages'):
            if file.endswith(".png"):
                self.images_number += 1
    
    def load_initial_images(self):
        self.existing_images = [ImageTk.PhotoImage(Image.open(r'ExistingImages\img' + str(i) + r'.png')
                                              .resize((250, 225))) for i in range(1, self.images_number+1)]
        
    def set_existing_images_window(self, master):
        self.clean_and_rebuild('Existing Images')
        leftArrowImage = Image.open("ExistingImages/Arrows/leftarrow.png")
        resizedLeftArrowImage = ImageTk.PhotoImage(leftArrowImage.resize((20, 20), Image.ANTIALIAS))
        rightArrowImage = Image.open("ExistingImages/Arrows/rightarrow.png")
        resizedRightArrowImage = ImageTk.PhotoImage(rightArrowImage.resize((20, 20), Image.ANTIALIAS))

        leftArrowBtn = Button(self.display_window, image=resizedLeftArrowImage, command=lambda: self.next_image(-1))
        leftArrowBtn.image = resizedLeftArrowImage
        rightArrowBtn = Button(self.display_window, image=resizedRightArrowImage, command=lambda: self.next_image(1))
        rightArrowBtn.image = resizedRightArrowImage
        back_button = Button(self.display_window, text='Back', command=self.set_welcome_window)


        leftArrowBtn.pack(side=LEFT, padx=15, pady=20)
        rightArrowBtn.pack(side=RIGHT, padx=15, pady=20)
        back_button.pack(side=TOP, pady=10)

        self.photo_frame = Frame(self.display_window)
        self.center_label = Label(self.photo_frame, image=self.existing_images[self.current_image])
        self.photo_frame.pack(anchor='center', pady=30)
        self.center_label.pack()

        encrypt_button = Button(self.display_window, text='Encrypt', command=lambda: self.generic_action_handler(encrypt_button, self.encrypt_image))
        remove_image_button = Button(self.display_window, text='Remove Image', command=lambda: self.generic_action_handler(remove_image_button,self.remove_image))
        decrypt_button = Button(self.display_window, text='Decrypt', command=lambda: self.generic_action_handler(decrypt_button, self.decrypt_image))

        encrypt_button.pack(side='left')
        decrypt_button.pack(side='left')
        remove_image_button.pack(side='right')
        
    def generic_action_handler(self, button, func):
        if self.images_number > 0:
            func()
        else:
            button.configure(state="disabled")
        
    def set_welcome_window(self):
        self.clean_and_rebuild('Existing Images')
        existingImagesBtn = Button(self.display_window, text='Existing Images', command=lambda: self.set_existing_images_window(self.display_window))
        importImagesBtn = Button(self.display_window, text='Import Images', command=self.open_file)
        exitBtn = Button(self.display_window, text='Exit', command=self.display_window.destroy)

        existingImagesBtn.pack(side=LEFT, padx=15, pady=20)
        importImagesBtn.pack(side=RIGHT, padx=15, pady=20)
        exitBtn.pack(side=BOTTOM, padx=15, pady=20)

    def next_image(self, direction):
        self.current_image = (self.current_image+direction)%self.images_number
        self.center_label.configure(image=self.existing_images[self.current_image])

    def remove_image(self):
        print("Images number before decrypt is: " +str(self.images_number))
        
        self.existing_images.remove(self.existing_images[self.current_image])
        os.remove(r'ExistingImages\img' + str(self.current_image + 1) + ".png")
                
        #shifting saved images names
        for i in range(self.current_image + 1, self.images_number):
            src_path = os.path.join(r'ExistingImages', f"img{i+1}.png")
            dst_path = os.path.join(r'ExistingImages', f"img{i}.png")
            shutil.move(src_path, dst_path)    
        self.images_number -= 1
        #check upper bound
        if self.current_image >= self.images_number:
            self.current_image = self.images_number - 1
        if self.images_number > 0:
            self.center_label.configure(image=self.existing_images[self.current_image])

    def encrypt_image(self):
        # Convert the image to a 2D array of pixels
        with Image.open(r'ExistingImages\img' + str(self.current_image + 1) + ".png") as img:
            pixels = img.load()
            width, height = img.size
            # The key to use for encryption
            key = 20
            salt = 0
            # Encrypt the pixels
            for x in range(width):
                key =(key+10)%256
                for y in range(height):
                    salt += 17
                    pixel = pixels[x, y]
                    new_pixel = []
                    for value in pixel:
                        new_value = (value + salt)%256
                        new_value ^= key
                        new_pixel.append(new_value)
                    pixels[x, y] = tuple(new_pixel)

            # Save the encrypted image
            img.save(r'ExistingImages\img' + str(self.current_image + 1) + ".png")
            self.existing_images[self.current_image] = ImageTk.PhotoImage(img.resize((250, 225)))
        self.center_label.configure(image=self.existing_images[self.current_image])

    def decrypt_image(self):
        # Load the encrypted image
        with Image.open(r'ExistingImages\img' + str(self.current_image + 1) + ".png") as img:
            pixels = img.load()
            width, height = img.size

            # The key to use for decryption
            key = 20
            salt = 0
            # Decrypt the pixels
            for x in range(width):
                key =(key+10)%256
                for y in range(height):
                    salt +=17
                    pixel = pixels[x, y]
                    new_pixel = []
                    for value in pixel:
                        value ^= key
                        new_value = (value - salt)%256
                        new_pixel.append(new_value)
                    pixels[x, y] = tuple(new_pixel)
            img.save(r'ExistingImages\img' + str(self.current_image + 1) + ".png")
            # Show the decrypted image
            self.existing_images[self.current_image] = ImageTk.PhotoImage(img.resize((250, 225)))
            self.center_label.configure(image=self.existing_images[self.current_image])

    def open_file(self):
        # Open a file dialog box and allow the user to select multiple image files
        file_paths = filedialog.askopenfilenames(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
        # Convert each file into a PhotoImage object and store them in a list
        for file_path in file_paths:
            image = Image.open(file_path)
            image.save(r'ExistingImages\img' + str(self.images_number + 1) + ".png")
            self.images_number += 1
