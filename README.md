# Image Steganography using LSB

![Steganography](https://www.wattlecorp.com/wp-content/uploads/2020/10/Top-3-Steganography-Tools.jpg)

This desktop application allows you to hide and extract an image within an image using Image Steganography. It provides a user-friendly interface for selecting cover images, secret images, setting AES keys, and performing the steganography operations.

## Features

- Two tabs: "Hide Data" and "Extract Data"
- Upload cover image and secret image (Cover Image should be larger than secret image for better quality of secret image at the time of extraction)
- Set AES 256-bit password for encryption
- Perform image steganography using the Least Significant Bit (LSB) algorithm
- Save the steganographic result wherever you want
- Extract hidden data from stego images

## Getting Started

Follow these steps to run the Image Steganography App on your local machine:

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/image_steganography_using_lsb.git

2. Change into the project directory:

    ```bash
    cd image_steganography_using_lsb

3. Install the required dependencies:

    ```bash
    pip install -r requirements.txt

4. Run the application:

    ```bash
    python main.py


## Usage
To Hide Data:
    
1. Open the application.
2. Navigate to the "Hide Data" tab.
3. Select a cover image and a secret image (larger cover image and smaller secret image in size and pixels also).
4. Set a 16-character AES key.
5. Click the "Hide Data" button.
6. Image will be saved at the location where your main.py is.

    
To Extract Data:

1. Navigate to the "Extract Data" tab.
2. Select the stego image.
3. Enter the same AES key used for hiding.
4. Click the "Extract Data" button.

        Note: "You can save Extracted image wherever you want on system."

## Licence

This project is licensed under the MIT License - see the [LICENSE](https://choosealicense.com/licenses/mit/) file for details.

## Authors

- Ved Malve [GitHub](https://www.github.com/vedsmalve) | [LinkedIn](https://www.linkedin.com/in/vedsmalve/)

- Aditya Sonar [GitHub](https://www.github.com/AdityaaSonar24) | [LinkedIn](https://www.linkedin.com/in/aditya-sonar-03afd/)

- Shashikant Kandekar [GitHub](https://www.github.com/Shashikantkandekar) | [LinkedIn](https://www.linkedin.com/in/shashikantkandekar/)

- Samadhan Kardile [GitHub](https://www.github.com/samadhankardile17) | [LinkedIn](https://www.linkedin.com/in/samadhan-kardile-5bb28526b?utm_source=share&utm_campaign=share_via&utm_content=profile&utm_medium=android_app)




## Support

For support, email vedsmalve@yahoo.com

## Associated With

    Savitribai Phule Pune University (SPPU)

## Sponsored by

VAnalytics
