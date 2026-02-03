import argparse
from pathlib import Path

from image_metadata_lab.exif_reader import read_exif_summary


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="OpenCV ops + EXIF (GPS/DateTime) reader")
    parser.add_argument("--input", required=True, help="Path to an image file")

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    input_path = str(Path(args.input))

    exif_summary = read_exif_summary(input_path)
    print("EXIF Summary")
    print("-----------")
    print(f"DateTimeOriginal: {exif_summary.date_time_original}")
    print(f"Latitude:         {exif_summary.latitude}")
    print(f"Longitude:        {exif_summary.longitude}")


if __name__ == "__main__":
    main()
