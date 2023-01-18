from tkinter import *

import rsa
from PIL import Image, ImageTk
import glob
import cv2
existing_images = []
current_image = 0
images_number = 0
public_key, private_key = rsa.newkeys(512)


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
        # existing_images = [cv2.imread(file) for file in glob.glob("ExistingImages/*.jpg")]
        existing_images = [ImageTk.PhotoImage(Image.open(r'ExistingImages\img' + str(i) + r'.jpg')
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
        global existing_images, current_image, public_key
        #img = existing_images[current_image]

        # Convert the image to a 2D array of pixels
        with Image.open(r'ExistingImages\img' + str(current_image + 1) + ".jpg") as img:
            pixels = img.load()
            width, height = img.size

            # The key to use for encryption
            key = 123

            # Encrypt the pixels
            for x in range(width):
                for y in range(height):
                    pixel = pixels[x, y]
                    new_pixel = []
                    for value in pixel:
                        new_value = value ^ key
                        new_pixel.append(new_value)
                    pixels[x, y] = tuple(new_pixel)

                # Save the encrypted image
            img.save(r'ExistingImages\encrypted-image' + str(current_image + 1) + ".jpg")
            existing_images[current_image] = ImageTk.PhotoImage(img.resize((250, 225)))
        self.center_label.configure(image=existing_images[current_image])

    def decrypt_image(self):
        global existing_images, current_image
        #existing_images[current_image] = rsa.decrypt(existing_images[current_image])

        with Image.open(r'ExistingImages\encrypted-image' + str(current_image + 1) + ".jpg") as img:
            pixels = img.load()
            width, height = img.size

            # The key to use for encryption
            key = 123

            # Encrypt the pixels
            for x in range(width):
                for y in range(height):
                    pixel = pixels[x, y]
                    new_pixel = []
                    for value in pixel:
                        new_value = value ^ key
                        new_pixel.append(new_value)
                    pixels[x, y] = tuple(new_pixel)

                # Save the encrypted image
            img.save(r'ExistingImages\decrypted-image' + str(current_image + 1) + ".jpg")
            existing_images[current_image] = ImageTk.PhotoImage(img.resize((250, 225)))
        self.center_label.configure(image=existing_images[current_image])


        # from PIL import Image
        #
        # # Open the image
        # with Image.open("image.jpg") as img:
        #     # Convert the image to a 2D array of pixels
        #     pixels = img.load()
        #     width, height = img.size
        #
        #     # The key to use for encryption
        #     key = 123
        #
        #     # Encrypt the pixels
        #     for x in range(width):
        #         for y in range(height):
        #             pixel = pixels[x, y]
        #             new_pixel = []
        #             for value in pixel:
        #                 new_value = value ^ key
        #                 new_pixel.append(new_value)
        #             pixels[x, y] = tuple(new_pixel)
        #
        #     # Save the encrypted image
        #     img.save("encrypted_image.jpg")
