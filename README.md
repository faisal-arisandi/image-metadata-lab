# Image Metadata Lab
This project is used to read EXIF metadata from an image, extract date time, latitude, and longitude, also to perform simple image processing (convert image into grayscale)

### Preparation
1. Activate the virtual environment by running this command:
    ```
    source .venv/bin/activate
    ```
2. Install dependencies by running these commands:
    ```
    python -m pip install -U pip
    python -m pip install -e ".[dev]"
    ```

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

### How to stop
#### Stop Jupyter Lab
**Using terminal**
1. In terminal, press `CTRL+C`
2. Confirm by type `y` and hit `Enter` 

**Using Web Interface**
1. Click `File` menu
2. Select `Shutdown` 

### Deactivate Virtual Environment
1. In terminal, type `deactivate`