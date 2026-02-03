# Image Metadata Lab
This project is used to read EXIF metadata from an image, extract date time, latitude, and longitude, also to perform simple image processing (convert image into grayscale)

### How to run
**Using CLI**
1. Put the photo inside folder `data/input/`
    For example, if the filename is `photo.jpg`, then the file location will be `data/input/photo.jpg`
2. Run this command:
    ```
    python -m image_metadata_lab.cli --input data/input/photo.jpg --output data/output/sample_gray.jpg
    ```

**Using Jupyter Lab**
1. Run this command:
    ```
    jupyter lab
    ```
2. Open the notebook `01-notebook.ipynb`