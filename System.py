from tkinter import *
from tkinter import filedialog
from tkinter.filedialog import askopenfile
from PIL import Image, ImageTk
import os
import shutil

from InfoBtn import InfoButton


class System (Frame):
    existing_images = []
    current_image = 0
    images_number = 0
    description = "The Image Encryptor Demo is a Python program with a Tkinter-based GUI that allows users to encrypt\r " \
                  "and decrypt image files, as well as import and remove existing image files. The program utilizes the\r " \
                  "Pillow library for image processing and maintains a list of existing images and their file paths for\r " \
                  "easy access and manipulation. Encryption is achieved through a reversible algorithm that alters the\r " \
                  "pixel values of the image without any loss of image quality. The program is an effective\r " \
                  "demonstration of image encryption and decryption and can be expanded for more advanced usage.\r" \
                  "Authors: Lior Perlman & Guy Rinsky"
    
    def __init__(self, master):
        Frame.__init__(self, master)
        self.display_window = master
        self.set_window_settings('Image Encryptor Demo')
        self.set_welcome_window()
        self.update_images_number()

    def clean_and_rebuild(self, title):
        self.display_window.update()
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
        self.current_image = 0
        left_arrow_image = Image.open("ExistingImages/Arrows/leftarrow.png")
        resized_left_arrow_image = ImageTk.PhotoImage(left_arrow_image.resize((20, 20), Image.ANTIALIAS))
        right_arrow_image = Image.open("ExistingImages/Arrows/rightarrow.png")
        resizedRightArrowImage = ImageTk.PhotoImage(right_arrow_image.resize((20, 20), Image.ANTIALIAS))

        left_arrow_button = Button(self.display_window, image=resized_left_arrow_image, command=lambda: self.generic_action_handler(left_arrow_button, self.next_image, -1))
        left_arrow_button.image = resized_left_arrow_image
        right_arrow_button = Button(self.display_window, image=resizedRightArrowImage, command=lambda: self.generic_action_handler(right_arrow_button, self.next_image, 1))
        right_arrow_button.image = resizedRightArrowImage
        back_button = Button(self.display_window, text='Back', command=self.set_welcome_window)

        left_arrow_button.pack(side=LEFT, padx=15, pady=20)
        right_arrow_button.pack(side=RIGHT, padx=15, pady=20)
        back_button.pack(side=TOP, pady=10)

        self.photo_frame = Frame(self.display_window)
        self.center_label = Label(self.photo_frame, image=self.existing_images[self.current_image])
        self.photo_frame.pack(anchor='center', pady=30)
        self.center_label.pack()

        encrypt_button = Button(self.display_window, text='Encrypt', command=lambda: self.generic_action_handler(encrypt_button, self.encrypt_image, 0))
        remove_image_button = Button(self.display_window, text='Remove Image', command=lambda: self.generic_action_handler(remove_image_button,self.remove_image, 0))
        decrypt_button = Button(self.display_window, text='Decrypt', command=lambda: self.generic_action_handler(decrypt_button, self.decrypt_image, 0))

        encrypt_button.pack(side='left')
        decrypt_button.pack(side='left')
        remove_image_button.pack(side='right')
        
    def generic_action_handler(self, button, func, flag):
        if self.images_number > 0:
            if flag == 0:
                func()
            else:
                func(flag)
        else:
            button.configure(state="disabled")
        
    def set_welcome_window(self):
        self.clean_and_rebuild('Existing Images')
        info_image_raw = Image.open("ExistingImages/infoBtn/Info.png")
        info_image = ImageTk.PhotoImage(info_image_raw.resize((20, 20), Image.ANTIALIAS))
        info_button = InfoButton(self.display_window, image=info_image, description=self.description)
        info_button.image = info_image
        info_button.configure(state="disable", borderwidth=0, fg="white", font=("Arial", 10, "bold"), compound="left", pady=5)
        existing_images_button = Button(self.display_window, text='Existing Images', command=lambda: self.set_existing_images_window(self.display_window))
        import_images_button = Button(self.display_window, text='Import Images', command=self.open_file)
        exit_button = Button(self.display_window, text='Exit', command=self.display_window.destroy)

        info_button.pack(anchor=NW)
        existing_images_button.pack(side=LEFT, padx=15, pady=20)
        import_images_button.pack(side=RIGHT, padx=15, pady=20)
        exit_button.pack(side=BOTTOM, padx=15, pady=20)

    def next_image(self, direction):
        self.current_image = (self.current_image+direction)%self.images_number
        self.center_label.configure(image=self.existing_images[self.current_image])

    def remove_image(self):        
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
