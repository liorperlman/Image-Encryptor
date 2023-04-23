# Readme file for Image Encryptor Demo

## Description

The Image Encryptor Demo is a Python program with a Tkinter-based GUI that allows users to encrypt and decrypt image files, as well as import and remove existing image files. The program utilizes the Pillow library for image processing and maintains a list of existing images and their file paths for easy access and manipulation. Encryption is achieved through a reversible algorithm that alters the pixel values of the image without any loss of image quality. The program is an effective demonstration of image encryption and decryption and can be expanded for more advanced usage.

## Requirements

- Python 3.x
- tkinter module (usually pre-installed with Python)
- Pillow library (can be installed using `pip install Pillow`)

## How to use

1. Open a terminal window and navigate to the directory where the program files are located.
2. Run the following command: `python main.py`
3. The main window of the program will appear, with three buttons: "Existing Images", "Import Images", and "Exit".
4. Click on "Import Images" to select image files to import. Supported file formats are `.png`, `.jpg`, and `.jpeg`. Imported images will be stored in the "ExistingImages" directory in the same directory as the program files.
5. Click on "Existing Images" to view a list of existing images. You can navigate between images using the left and right arrow buttons. You can also remove an image by clicking the "Remove Image" button, and encrypt or decrypt an image using the "Encrypt" and "Decrypt" buttons, respectively.
6. To exit the program, click on the "Exit" button.

## Authors

- Lior Perlman
- Guy Rinsky
