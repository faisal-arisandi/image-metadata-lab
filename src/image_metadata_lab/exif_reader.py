from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, Optional, Tuple

from PIL import Image
from PIL.ExifTags import GPSTAGS, TAGS

@dataclass(frozen=True)
class ExifSummary:
  date_time_original: Optional[datetime]
  latitude: Optional[float]
  longitude: Optional[float]
  raw: Dict[str, Any]

def _to_float_rational(value: Any) -> Optional[float]:
  """
  Pillow may return rationals as tuples, IFDRational, or plain numbers.
  Convert best-effort.
  """

  if value is None:
    return None
  
  try:
    return float(value)
  except Exception:
    pass

  if isinstance(value, tuple) and len(value) == 2:
    numerator, denominator = value

    try:
      return float(numerator) / float(denominator)
    except Exception:
      return None

  return None

def _dms_to_decimal(
  degrees_value: Any,
  minutes_value: Any,
  seconds_value: Any,
  hemisphere: str,
) -> Optional[float]:
  degrees = _to_float_rational(degrees_value)
  minutes = _to_float_rational(minutes_value)
  seconds = _to_float_rational(seconds_value)

  if degrees is None or minutes is None or seconds is None:
    return None
  
  decimal_value = degrees + (minutes / 60.0) + (seconds / 3600.0)
  if hemisphere in ("S", "W"):
    decimal_value = -decimal_value
  
  return decimal_value

def _extract_gps_decimal(gps_info: Dict[str, Any]) -> Tuple[Optional[float], Optional[float]]:
  lat = lon = None

  lat_ref = gps_info.get("GPSLatitudeRef")
  lat_value = gps_info.get("GPSLatitude")
  lon_ref = gps_info.get("GPSLongitudeRef")
  lon_value = gps_info.get("GPSLongitude")

  if lat_ref and lat_value and isinstance(lat_value, (list, tuple)) and len(lat_value) == 3:
    lat = _dms_to_decimal(lat_value[0], lat_value[1], lat_value[2], str(lat_ref))

  if lon_ref and lon_value and isinstance(lon_value, (list, tuple)) and len(lon_value) == 3:
    lon = _dms_to_decimal(lon_value[0], lon_value[1], lon_value[2], str(lon_ref))
  
  return lat, lon

def _read_gps_ifd(exif: Image.Exif) -> Dict[str, Any]:
    """
    EXIF GPS lives in a separate IFD (subdirectory). The GPSInfo tag in the main
    EXIF is often just an offset/pointer. Pillow exposes the GPS IFD via get_ifd.
    """
    GPSINFO_TAG_ID = 0x8825  # 34853
    gps_ifd = exif.get_ifd(GPSINFO_TAG_ID)

    gps_parsed: Dict[str, Any] = {}
    for gps_key, gps_value in gps_ifd.items():
        gps_name = GPSTAGS.get(gps_key, gps_key)
        gps_parsed[str(gps_name)] = gps_value

    return gps_parsed

def read_exif_summary(image_path: str) -> ExifSummary:
  """
  Reads EXIF metadata and extracts:
    - DateTimeOriginal (if present) or falls back to DateTime
    - GPS latitude/longitude (if present)
  """

  with Image.open(image_path) as image:
    exif = image.getexif()

  raw_tags: Dict[str, Any] = {}
  # gps_parsed: Dict[str, Any] = {}

  date_time_original: Optional[datetime] = None
  latitude: Optional[float] = None
  longitude: Optional[float] = None

  if exif is not None:
    for tag_id, value in exif.items():
      tag_name = TAGS.get(tag_id, tag_id)
      raw_tags[str(tag_name)] = value

      if tag_name == "DateTimeOriginal" and isinstance(value, str):
        # Common format: "YYYY:MM:DD HH:MM:SS"
        try:
          date_time_original = datetime.strptime(value, "%Y:%m:%d %H:%M:%S")
        except ValueError:
          date_time_original = None

    # Fallback: DateTime (IFD0) if DateTimeOriginal not present
    if date_time_original is None:
      dt_value = raw_tags.get("DateTime")
      if isinstance(dt_value, str):
        try:
          date_time_original = datetime.strptime(dt_value, "%Y:%m:%d %H:%M:%S")
        except ValueError:
          date_time_original = None

    try:
      gps_parsed = _read_gps_ifd(exif)
    except Exception:
      gps_parsed = {}

  
    if gps_parsed:
      latitude, longitude = _extract_gps_decimal(gps_parsed)
      raw_tags["GPSInfoParsed"] = gps_parsed

  return ExifSummary(
    date_time_original=date_time_original,
    latitude=latitude,
    longitude=longitude,
    raw=raw_tags,
  )