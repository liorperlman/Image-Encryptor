from tkinter import *
from tkinter import filedialog
from tkinter.filedialog import askopenfile

from Crypto.Cipher import AES
from Crypto.Util import Padding

from PIL import Image, ImageTk, ImageCms
import os
import struct






#key_AES = b'\xba\xfb\xe2\xd72\xcfL\xe9\x1e\x1f\xf4\xe9MS\x1du'


class System (Frame):
    # Constructor without parameters
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
        self.display_window.geometry("350x350")
        self.display_window.title(title)
    
    def update_images_number(self):
        self.images_number = 0
        for file in os.listdir('ExistingImages'):
            if file.endswith(".png"):
                self.images_number += 1
    
    def load_initial_images(self):
        self.existing_images = [ImageTk.PhotoImage(Image.open(r'ExistingImages\img' + str(i) + r'.png')
                                              .resize((250, 225))) for i in range(1, self.images_number+1)]
        
    

    def existingImagesWindow(self, master):
        self.clean_and_rebuild('Existing Images')
        leftArrowImage = Image.open("ExistingImages/Arrows/leftarrow.png")
        resizedLeftArrowImage = ImageTk.PhotoImage(leftArrowImage.resize((20, 20), Image.ANTIALIAS))
        rightArrowImage = Image.open("ExistingImages/Arrows/rightarrow.png")
        resizedRightArrowImage = ImageTk.PhotoImage(rightArrowImage.resize((20, 20), Image.ANTIALIAS))

        leftArrowBtn = Button(self.display_window, image=resizedLeftArrowImage, command=lambda: self.next_image(-1))
        leftArrowBtn.image = resizedLeftArrowImage
        rightArrowBtn = Button(self.display_window, image=resizedRightArrowImage, command=lambda: self.next_image(1))
        rightArrowBtn.image = resizedRightArrowImage

        leftArrowBtn.pack(side=LEFT, padx=15, pady=20)
        rightArrowBtn.pack(side=RIGHT, padx=15, pady=20)

        self.photo_frame = Frame(self.display_window)
        self.center_label = Label(self.photo_frame, image=self.existing_images[self.current_image])
        self.photo_frame.pack(anchor='center', pady=30)
        self.center_label.pack()

        encrypt_button = Button(self.display_window, text='Encrypt', command=self.encrypt_image)
        remove_image_button = Button(self.display_window, text='remove Image', command=self.remove_image)
        decrypt_button = Button(self.display_window, text='Decrypt', command=self.decrypt_image)

        encrypt_button.pack(side='left')
        decrypt_button.pack(side='left')
        remove_image_button.pack(side='right')
        
    def set_welcome_window(self):
        existingImagesBtn = Button(self.display_window, text='Existing Images', command=lambda: self.existingImagesWindow(self.display_window))
        importImagesBtn = Button(self.display_window, text='Import Images', command=self.open_file)
        exitBtn = Button(self.display_window, text='Exit', command=self.display_window.destroy)

        existingImagesBtn.pack(side=LEFT, padx=15, pady=20)
        importImagesBtn.pack(side=RIGHT, padx=15, pady=20)
        exitBtn.pack(side=BOTTOM, padx=15, pady=20)


    def next_image(self, direction):
        self.current_image = (self.current_image+direction)%self.images_number
        
        self.center_label.configure(image=self.existing_images[self.current_image])

    def remove_image(self):
        self.existing_images.remove(self.existing_images[self.current_image])
        os.remove(r'ExistingImages\img' + str(self.current_image + 1) + ".png")
        for i in range(self.current_image+1, self.images_number):
            temp_image = Image.open(r'ExistingImages\img' + str(i + 1) + ".png")
            temp_image.save(r'ExistingImages\img' + str(i) + ".png")
        os.remove(r'ExistingImages\img' + str(self.images_number) + ".png")
        self.images_number -= 1
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


    #def decrypt_image_AES(self):
        #     global key, cipher_global, cipher_nonce
        #     # Open the encrypted image file
        #     with Image.open(r'ExistingImages\encrypted_image' + str(current_image + 1) + ".png") as img:
        #         # Convert the image to bytes
        #         img_bytes = img.tobytes()
        #         # Create a new AES cipher
        #         #cipher = AES.new(key, AES.MODE_EAX, cipher_global)
        #         cipher_global = AES.new(key, AES.MODE_EAX, nonce=cipher_global.nonce)
        #         # Decrypt the image bytes
        #         decrypted_data = cipher_global.decrypt(img_bytes)
        #         # Unpad the decrypted data
        #         #unpadded_data = decrypted_data
        #         #unpadded_data = Padding.unpad(decrypted_data, AES.block_size)
        #         # Create a new image from the decrypted data
        #         decrypted_img = Image.frombytes(img.mode, img.size, decrypted_data)
        #         # Save the decrypted image
        #         decrypted_img.save(r'ExistingImages\decrypted_image' + str(current_image + 1) + ".png")
        #         existing_images[current_image] = ImageTk.PhotoImage(img.resize((250, 225)))
        #     self.center_label.configure(image=existing_images[current_image])

    #def encrypt_image_AES(self):
        #     global public_keys, current_image, existing_images, key, cipher_global,cipher_nonce, cipher_tag
        #     # Open the image file
        #     with Image.open(r'ExistingImages\img' + str(current_image + 1) + ".png") as img:
        #         # Convert the image to bytes
        #         img_bytes = img.tobytes()
        #         # Create a new AES cipher
        #         #key = os.urandom(16)
        #         #public_keys.insert(current_image, key)
        #         cipher_global = AES.new(key, AES.MODE_EAX)
        #         #cipher_nonce = cipher_global.nonce
        #         #cipher_global = cipher
        #         # Pad the data to a multiple of the block size
        #         #padded_data = img_bytes
        #         #padded_data = Padding.pad(img_bytes, AES.block_size)
        #         # Encrypt the padded data
        #         #encrypted_data, cipher_tag= cipher_global.encrypt_and_digest(padded_data)
        #         encrypted_data = cipher_global.encrypt(img_bytes)
        #         # Create a new image from the encrypted data
        #         encrypted_img = Image.frombytes(img.mode, img.size, encrypted_data)
        #         # Save the encrypted image
        #         encrypted_img.save(r'ExistingImages\encrypted_image' + str(current_image + 1) + ".png")
        #         existing_images[current_image] = ImageTk.PhotoImage(encrypted_img.resize((250, 225)))
        #     self.center_label.configure(image=existing_images[current_image])
