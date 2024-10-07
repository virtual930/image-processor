import os
import sys
import logging
from PIL import Image, ImageFilter
from concurrent.futures import ThreadPoolExecutor, as_completed

class Defaults:
    """
    A class to hold default constants for image processing settings.

    :Attributes:
        SIZE (int): The default size to which images will be resized. Default is 300 pixels.
        SMALLEST_SIZE (int): The minimum allowed size for resizing images. Default is 25 pixels.
        LARGEST_SIZE (int): The maximum allowed size for resizing images. Default is 10,000 pixels.
        BLUR (int): The radius of the Gaussian blur to apply to images. Default is 10.
        SQUARE_PERCENT (float): The percentage tolerance to determine if an image is approximately square. Default is 0.05 (5%).
        WHITE_TRANSPARENCY (float): The transparency level for the white overlay applied to images. Default is 0.33 (33%).
        OUTPUT_FOLDER (str): The name of the folder where processed images will be saved. Default is "revised images".
        KEEP_EXTENSION (str): The string used to indicate that the original file extension should be retained. Default is "org".
        VALID_EXTENSIONS (list): A list of valid image file extensions that the program can process. Defaults include 'jpg', 'jpeg', 'bmp', 'png', 'webp'.
    """
    SIZE = 300
    SMALLEST_SIZE = 25
    LARGEST_SIZE = 10000
    BLUR = 10
    SQUARE_PERCENT = 0.05
    WHITE_TRANSPARENCY = 0.33
    OUTPUT_FOLDER = "revised images"
    KEEP_EXTENSION = "org"
    VALID_EXTENSIONS = ['jpg', 'jpeg', 'bmp', 'png', 'webp']


def main():
    """Main function to initiate image processing.

    This function gets the input folder, desired image size, and file extension from the user,
    creates an output folder, and processes all images in the input folder.

    :returns: None
    """
    input_folder = os.getcwd()

    size = get_size_input()
    extension = get_extension_input()

    output_folder = os.path.join(input_folder, Defaults.OUTPUT_FOLDER)
    make_output_folder(output_folder)

    folder_to_process(input_folder, size, extension, output_folder)




def make_output_folder(output_folder):
    """Create the output folder if it does not exist.

    :param output_folder: The path to the output folder.
    :returns: None

    If the folder cannot be created, an error message is logged.
    """
    try:
        os.makedirs(output_folder, exist_ok=True)
        setup_logging(output_folder)
    except Exception as e:
        print(f"Could not create the output folder: {e}")
        logging.basicConfig(
            filename='image_processing_error.txt',
            level=logging.ERROR,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        logging.error(f"Error creating output folder: {e}")
        return


def setup_logging(output_folder):
    """Set up logging to a file in the specified output folder.

    :param output_folder: The path to the output folder where the log file will be saved.
    :returns: None
    """
    log_file_path = os.path.join(output_folder, 'image_processing.txt')
    logging.basicConfig(
        filename=log_file_path,
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )


def get_size_input():
    """Prompt the user for the desired size.

    :returns: An integer representing the desired size within the valid range.

    If the input is invalid, the user is prompted again until a valid size is entered.
    """
    while True:
        size_input = input(f"Enter the desired size (default is {Defaults.SIZE}): ")
        if size_input.strip() == '':
            return Defaults.SIZE
        try:
            size = int(size_input)
            if Defaults.LARGEST_SIZE >= size >= Defaults.SMALLEST_SIZE:
                return size
            print(f"Please enter a positive integer between {Defaults.SMALLEST_SIZE}-{Defaults.LARGEST_SIZE}")
        except ValueError:
            print("Invalid input. Please enter a number.")


def get_extension_input():
    """Prompt the user to select the output file extension for processed images.

    This function presents a list of valid output file formats, allowing the user to
    specify their preferred format or to keep the original file type. If the user
    does not provide input, the default option is set to keep the original extension.

    :returns: A string representing the desired output file extension.
              Valid options include 'jpg', 'jpeg', 'png', 'webp',
              or 'org' to retain the original file type.

    If the input is invalid, the user is prompted again until a valid extension is entered.
    """
    while True:
        extension = input(
            f"Enter the desired output file extension ({', '.join(Defaults.VALID_EXTENSIONS)}), or '{Defaults.KEEP_EXTENSION}' \nto use the original extension,  default is '{Defaults.KEEP_EXTENSION}': ").strip().lower()
        if extension == "":
            return Defaults.KEEP_EXTENSION
        elif extension == Defaults.KEEP_EXTENSION:
            return Defaults.KEEP_EXTENSION
        elif extension in Defaults.VALID_EXTENSIONS:
            return extension
        else:
            print("Invalid extension. Please choose from: " + ', '.join(Defaults.VALID_EXTENSIONS))


def process_image(input_path, output_path, size, extension):
    """Process a single image: resize, blur, and overlay.

    :param input_path: The path to the input image.
    :param output_path: The path where the processed image will be saved.
    :param size: The size to which the image will be resized.
    :param extension: The file extension for the output image.
    :returns: None

    If there is an error while processing the image, it is logged.
    """

    try:
        original_image = Image.open(input_path)
    except Exception as e:
        logging.error(f"Error opening {input_path}: {e}")
        print(f"Error opening {input_path}: {e}")
        return

    original_width, original_height = original_image.size

    if is_square(original_width, original_height):
        final_image = resize_image(original_image, size)
    else:
        final_image = create_blurred_overlay(original_image, size)

    extension = "JPEG" if extension == "JPG" else extension

    save_image(final_image, output_path, extension)


def is_square(width, height):
    """Check if the image dimensions are approximately square.

    :param width: The width of the image.
    :param height: The height of the image.
    :returns: True if the dimensions are approximately square, otherwise False.
    """
    return (width >= height * (1 - Defaults.SQUARE_PERCENT)) and (width <= height * (1 + Defaults.SQUARE_PERCENT))


def resize_image(image, size):
    """Resize the image to a square.

    :param image: The image to resize.
    :param size: The size to which the image will be resized.
    :returns: The resized image.
    """
    resized_image = image.resize((size, size), Image.LANCZOS)
    return resized_image.convert('RGBA')


def create_blurred_overlay(image, size):
    """Create a blurred background for a non-square image.

    :param image: The image to process.
    :param size: The size for the resized image.
    :returns: The image with a blurred for use in the background.
    """
    resized_image = image.resize((size, size), Image.LANCZOS)

    # Convert to a suitable mode before applying Gaussian blur
    resized_image = resized_image.convert("RGB") if resized_image.mode not in ("RGB", "L") else resized_image

    blurred_image = resized_image.filter(ImageFilter.GaussianBlur(radius=Defaults.BLUR))

    white_overlay = create_white_overlay(blurred_image.size)
    blurred_with_white = Image.alpha_composite(blurred_image.convert('RGBA'), white_overlay)

    resized_original = resize_original(image, size)

    return compose_final_image(blurred_with_white, resized_original)

def create_white_overlay(size):
    """Create a white overlay with transparency.

    :param size: The size of the overlay.
    :returns: An image that is a white overlay with the specified size.
    """
    return Image.new('RGBA', size, (255, 255, 255, int(255 * Defaults.WHITE_TRANSPARENCY)))


def resize_original(image, max_size):
    """Resize the original image while maintaining aspect ratio.

    :param image: The original image to resize.
    :param max_size: The maximum size for the resized image.
    :returns: The resized image with maintained aspect ratio.
    """
    original_width, original_height = image.size
    scale = max_size / max(original_width, original_height)
    new_size = (int(original_width * scale), int(original_height * scale))
    return image.resize(new_size, Image.LANCZOS)


def compose_final_image(blurred_with_white, resized_original):
    """Compose the final image with the blurred overlay and the resized original.

    :param blurred_with_white: The image with the blurred overlay.
    :param resized_original: The resized original image.
    :returns: The final composed image.
    """
    final_image = Image.new('RGBA', blurred_with_white.size)
    final_image.paste(blurred_with_white, (0, 0))

    x_offset = (final_image.width - resized_original.width) // 2
    y_offset = (final_image.height - resized_original.height) // 2
    final_image.paste(resized_original.convert('RGBA'), (x_offset,
                      y_offset), resized_original.convert('RGBA'))

    return final_image


def save_image(image, output_path, extension):
    """Save the processed image to the specified path.

    :param image: The processed image to save.
    :param output_path: The path where the image will be saved.
    :param extension: The file extension for saving the image.
    :returns: None

    The function counts and logs how many images were processed.
    """
    try:
        image = image.convert('RGB') if extension == "JPEG" else image

        # Ensure the output path is unique
        output_path = get_unique_output_path(output_path)


        image.save(output_path, format=extension)  # Use the passed extension (already uppercase)
        logging.info(f"Saved: {output_path}")
        print(f"Saved: {output_path}")
    except Exception as e:
        logging.error(f"Error saving {output_path}: {e}")
        print(f"Error saving {output_path}: {e}")


def get_unique_output_path(output_path):
    """Generate a unique output path by appending (1), (2), ... if a file already exists.

    :param output_path: The base output path for the image.
    :returns: A unique output path.
    """
    base, extension = os.path.splitext(output_path)
    counter = 1

    while os.path.exists(output_path):
        output_path = f"{base} ({counter}){extension}"
        counter += 1

    return output_path


def folder_to_process(input_folder, size, extension, output_folder):
    """Process all images in the specified folder in parallel to handle multiple
    images at once, improving performance when processing large batches.

    :param input_folder: The folder containing the images to process.
    :param size: The size to which the images will be resized.
    :param extension: The desired output file extension.
    :param output_folder: The folder where processed images will be saved.
    :returns: None

    Errors during processing are logged, and a summary of processed images is displayed.
    """
    processed_count = 0



    with ThreadPoolExecutor() as executor:
        futures = []
        for filename in os.listdir(input_folder):
            if filename.lower().endswith(tuple(Defaults.VALID_EXTENSIONS)):
                input_path = os.path.join(input_folder, filename)
                output_extension = filename.split('.')[-1].lower() if extension == Defaults.KEEP_EXTENSION else extension
                output_filename = f"{os.path.splitext(filename)[0]}.{output_extension}"
                output_path = os.path.join(output_folder, output_filename)
                futures.append(executor.submit(process_image, input_path, output_path, size, output_extension.upper()))

        for _ in as_completed(futures):
            processed_count += 1

    if processed_count == 0:
        logging.warning("No images processed. Please check the input folder for valid image files.")
        print("No images processed. Please check the input folder for valid image files.")
    else:
        logging.info(f"Processed {processed_count} images.")
        print(f"Processed {processed_count} images.")

if __name__ == "__main__":
    main()
    # Check if the script is running in a console or as an executable
    if sys.stdout.isatty() and hasattr(sys, 'frozen'):  # Running as an EXE
        input("Press Enter to exit...")
