# from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Optional, Tuple

import cv2


@dataclass(frozen=True)
class ProcessResult:
    input_path: str
    output_path: str
    original_size: Tuple[int, int]
    output_size: Tuple[int, int]


def to_grayscale_and_resize(
    input_path: str,
    output_path: str,
    max_width: Optional[int] = 1024,
) -> ProcessResult:
    image_bgr = cv2.imread(input_path, cv2.IMREAD_COLOR)
    if image_bgr is None:
        raise ValueError(f"Could not read image: {input_path}")

    height, width = image_bgr.shape[:2]
    original_size = (width, height)

    scale = 1.0
    if max_width is not None and width > max_width:
        scale = max_width / float(width)

    new_width = int(round(width * scale))
    new_height = int(round(height * scale))

    resized_bgr = cv2.resize(image_bgr, (new_width, new_height), interpolation=cv2.INTER_AREA)
    gray = cv2.cvtColor(resized_bgr, cv2.COLOR_BGR2GRAY)

    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    ok = cv2.imwrite(output_path, gray)
    if not ok:
        raise ValueError(f"Could not write output image: {output_path}")

    return ProcessResult(
        input_path=input_path,
        output_path=output_path,
        original_size=original_size,
        output_size=(new_width, new_height),
    )
