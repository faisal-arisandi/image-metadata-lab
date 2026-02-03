from __future__ import annotations

import argparse
from pathlib import Path

from image_metadata_lab.exif_reader import read_exif_summary
from image_metadata_lab.image_ops import to_grayscale_and_resize


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="OpenCV ops + EXIF (GPS/DateTime) reader")
    parser.add_argument("--input", required=True, help="Path to an image file")
    parser.add_argument(
        "--output",
        default="data/output/processed_gray.jpg",
        help="Output path for processed image",
    )
    parser.add_argument(
        "--max-width",
        type=int,
        default=1024,
        help="Max width for resizing (preserves aspect ratio)",
    )
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    input_path = str(Path(args.input))
    output_path = str(Path(args.output))

    exif_summary = read_exif_summary(input_path)
    print("EXIF Summary")
    print("-----------")
    print(f"DateTimeOriginal: {exif_summary.date_time_original}")
    print(f"Latitude:         {exif_summary.latitude}")
    print(f"Longitude:        {exif_summary.longitude}")

    result = to_grayscale_and_resize(
        input_path=input_path,
        output_path=output_path,
        max_width=args.max_width,
    )

    print("\nProcessing Result")
    print("-----------------")
    print(f"Original size: {result.original_size}")
    print(f"Output size:   {result.output_size}")
    print(f"Saved to:      {result.output_path}")


if __name__ == "__main__":
    main()
