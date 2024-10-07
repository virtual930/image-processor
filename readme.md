# Image to Square Processing Tool

## Overview

The Image to Square Processing Tool is a user-friendly application designed to convert a folder of images with varying aspect ratios into perfectly square images. This is particularly useful for applications where uniform image dimensions are required, such as social media profiles, e-commerce platforms, and portfolio displays.

This tool efficiently processes multiple images in a single operation, allowing users to save time and effort by converting an entire batch of images at once. When processing, the tool intelligently adjusts each image's dimensions based on specific criteria. If an image's width is within 5% of its height, the application stretches the image to fit the specified square dimensions.

For images with significant aspect ratio deviations, the tool proportionally scales them to fit within the defined dimensions while maintaining their original proportions, ensuring that images do not become distorted. Additionally, for enhanced visual appeal, a duplicate of each original image is manipulated to fill the background. This duplicate is stretched to match the square dimensions, blurred to create a soft focus effect, and whitewashed to provide a subtle, aesthetically pleasing backdrop. The final result is a visually striking composition that maintains the integrity of the original images while providing a polished and professional appearance.

The tool has been compiled into an executable (.exe) format for seamless usage—simply place it in your images folder and run it! This makes it accessible for users who may not have programming skills or the Python environment installed.

## Features

- **Batch Resize Images**: Easily convert multiple images into square dimensions based on user-defined specifications, saving time and effort.
- **Soft Background Effect**: If the original image is not within 5% of being square, a Gaussian blur is applied, and a transparent white layer is placed on top for a softening effect. The original image is then proportionally scaled and layered on top, enhancing the overall visual aesthetics.
- **Output Format**:  Users can save processed images in various formats, including PNG, JPG, JPEG, and WEBP. Importantly, users can also choose to keep the original file type by selecting "org" as the output extension. This flexibility ensures that the images can be used across different platforms and applications without compatibility issues.
- **Image Quality Preservation**: The tool uses high-quality resizing algorithms (Lanczos) to ensure that images retain their visual fidelity during the resizing process.
- **Logging**: The tool automatically logs all actions and errors encountered during processing. This feature is invaluable for tracking progress and identifying issues, allowing users to troubleshoot effectively.

## Requirements

- **Python Version**: Python Version: Python 3.x is required if you are using the script version.
- **Libraries**:
  - `Pillow`: For image processing tasks. 
    - Install using pip: `pip install -r requirements.txt`

## Getting Started

### Prerequisites

- Windows Operating System (Executable designed for Windows)
- A folder containing the images you wish to process. Supported formats include .jpg, .jpeg, .png, and .webp.

### Installation

1. **Download the Executable**: Obtain the `ImageProcessingTool.exe` file from the [releases page](link-to-releases).

2. **Prepare Your Images**: Create a dedicated folder and place all the images you want to process in this location. Ensure that they are in a supported format to avoid processing errors.

3. **Run the Tool**:
   - Move the `ImageProcessingTool.exe` file into the folder with your images.
   - Double-click the executable to run it.

### Usage Instructions

1. Upon launching the tool, you will be prompted to enter the desired size for the images.
   - Press Enter to use the default size (300 pixels).

2. Next, you will be prompted to choose the output file extension:
   - Options include: `jpg`, `jpeg`, `png`, `webp`, or type `org` to keep the original file extension.
   - Press Enter to use the original format.

3. The tool will process all compatible images in the folder:
   - Processed images will be saved in a subfolder named `revised images`.

4. Check the `image_processing.txt` log file in the `revised images` folder for a summary of processed images and any errors that occurred.

### Notes

- Ensure the images in the folder are in supported formats: `.jpg`, `.jpeg`, `.png`, `.webp`.
- If no images are processed, a warning will be logged.

### Troubleshooting

- **Error Opening Images**: If the tool encounters an error while opening an image, check if the image file is corrupted or in an unsupported format.
- **No Images Processed**: Verify that the folder contains images with valid extensions.

## Contributing

Contributions are welcome! If you'd like to contribute to this project, feel free to submit issues or pull requests. Your feedback and contributions help improve the functionality and usability of the tool, making it better for everyone in the community.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Special thanks to the [Pillow](https://python-pillow.org/)  library for providing powerful image processing capabilities that make this tool possible.
- We also extend our gratitude to the open-source community for their invaluable contributions and support, which inspire and drive innovation in projects like this.