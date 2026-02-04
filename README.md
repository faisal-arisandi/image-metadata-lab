# Image Metadata Lab

This project is used to extract timestamps and geolocation data (latitude, longitude) from EXIF metadata of multiple images

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
1. Put all photos inside folder `data/input/`
    For example
    ```
    |-- data
        |-- input
            |-- photo1.jpg
            |-- photo2.jpeg
            |-- photo3.heic
            |-- photo4.heif
            |-- ...
    ```
2. Run this command:
    **To extract metadata from multiple images:**

    ```
    python -m image_metadata_lab.cli --input data/input/
    ```
    **To extract metadata from single image:**
    Example:
    ```
    python -m image_metadata_lab.cli --input data/input/photo1.jpg
    ```


**Using Jupyter Lab**
1. Run this command:
    ```
    jupyter lab
    ```
2. Open the notebook `01-notebook.ipynb` and play around with sample code **to extract metadata from single image.**

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