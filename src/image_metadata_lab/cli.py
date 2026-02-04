import argparse
from pathlib import Path
from typing import Dict, List

from image_metadata_lab.exif_reader import read_exif_summary
from image_metadata_lab.report_generator import write_csv, write_json

IMAGE_EXTS = {".jpg", ".jpeg", ".tif", ".tiff", ".heic", ".heif"}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Extract EXIF (DateTime + GPS) from file or folder")
    parser.add_argument("--input", required=True, help="Path to an image file or a folder containing images")
    parser.add_argument(
        "--format",
        choices=["csv", "json"],
        default="csv",
        help="Output format",
    )
    parser.add_argument(
        "--output",
        default=None,
        help="Output path. Defaults to data/output/metadata_report.(csv|json)"
    )

    return parser

def iterate_images(input_path: Path) -> List[Path]:
    if input_path.is_file():
        return [input_path]
    
    if input_path.is_dir():
        files: List[Path] = []
        for p in sorted(input_path.iterdir()):
            if p.is_file() and p.suffix.lower() in IMAGE_EXTS:
                files.append(p)
        
        return files

def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    input_path = Path(args.input)
    output_path = args.output
    if output_path is None:
        output_path = f"data/output/metadata_report.{args.format}"

    images = iterate_images(input_path)
    if not images:
        print("No images found. Supported extensions:", ", ".join(sorted(IMAGE_EXTS)))
        return

    rows: List[Dict[str, object]] = []
    for img_path in images:
        summary = read_exif_summary(str(img_path))
        rows.append(
            {
                "filename": img_path.name,
                "date_time_original": summary.date_time_original,
                "latitude": summary.latitude,
                "longitude": summary.longitude,
            }
        )
    
    if args.format == "csv":
        write_csv(output_path, rows)
    else:
        write_json(output_path, rows)

    print(f"Processed {len(images)} image(s).")
    print(f"Saved report to: {output_path}")


if __name__ == "__main__":
    main()
