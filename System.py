from tkinter import *
from Crypto.Cipher import AES
from Crypto.Util import Padding

from PIL import Image, ImageTk, ImageCms
import os
import struct


existing_images = []
current_image = 0

images_number = 0
#key_AES = b'\xba\xfb\xe2\xd72\xcfL\xe9\x1e\x1f\xf4\xe9MS\x1du'


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

        global existing_images
        existing_images = [ImageTk.PhotoImage(Image.open(r'ExistingImages\img' + str(i) + r'.png')
                                              .resize((250, 225))) for i in range(1, 10)]
        global images_number
        images_number = len(existing_images)
        self.photo_frame = Frame(self.display_window)
        self.center_label = Label(self.photo_frame, image=existing_images[current_image])
        self.photo_frame.pack(anchor='center', pady=30)
        self.center_label.pack()

        encrypt_button = Button(self.display_window, text='Encrypt', command=self.encrypt_image)
        decrypt_button = Button(self.display_window, text='Decrypt', command=self.decrypt_image)

        encrypt_button.pack(side='left')
        decrypt_button.pack(side='right')
    def set_welcome_window(self):
        existingImagesBtn = Button(self.display_window, text='Existing Images', command=lambda: self.existingImagesWindow(self.display_window))
        importImagesBtn = Button(self.display_window, text='Import Images')
        exitBtn = Button(self.display_window, text='Exit', command=self.display_window.destroy)

        existingImagesBtn.pack(side=LEFT, padx=15, pady=20)
        importImagesBtn.pack(side=RIGHT, padx=15, pady=20)
        exitBtn.pack(side=BOTTOM, padx=15, pady=20)


    def next_image(self, direction):
        global current_image, images_number
        current_image = (current_image+direction)%images_number
        self.center_label.configure(image=existing_images[current_image])

    def encrypt_image(self):
        global existing_images, current_image

        # Convert the image to a 2D array of pixels
        with Image.open(r'ExistingImages\img' + str(current_image + 1) + ".png") as img:
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
            img.save(r'ExistingImages\encrypted-image' + str(current_image + 1) + ".png")
            existing_images[current_image] = ImageTk.PhotoImage(img.resize((250, 225)))
        self.center_label.configure(image=existing_images[current_image])

    def decrypt_image(self):
        global existing_images, current_image

        # Load the encrypted image
        with Image.open(r'ExistingImages\encrypted-image' + str(current_image + 1) + ".png") as img:
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
            img.save(r'ExistingImages\decrypted-image' + str(current_image + 1) + ".png")
            # Show the decrypted image
            existing_images[current_image] = ImageTk.PhotoImage(img.resize((250, 225)))
            self.center_label.configure(image=existing_images[current_image])


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
