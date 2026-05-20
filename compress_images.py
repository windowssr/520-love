"""压缩回忆照片，便于 GitHub Pages / 手机加载。运行: python compress_images.py"""
import io
from pathlib import Path

from PIL import Image

MAX_EDGE = 1400
QUALITY = 82


def compress(path: Path) -> None:
    before = path.stat().st_size
    im = Image.open(path)
    if im.mode in ("RGBA", "P"):
        im = im.convert("RGB")
    w, h = im.size
    resized = max(w, h) > MAX_EDGE
    if resized:
        r = MAX_EDGE / max(w, h)
        im = im.resize((int(w * r), int(h * r)), Image.Resampling.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=QUALITY, optimize=True, progressive=True)
    data = buf.getvalue()
    if len(data) < before or resized:
        path.write_bytes(data)
        print(f"{path.name}: {before // 1024}KB -> {len(data) // 1024}KB")
    else:
        print(f"{path.name}: 保持原图 {before // 1024}KB（已足够小）")


if __name__ == "__main__":
    for p in sorted(Path(__file__).parent.glob("*.jpg")):
        compress(p)
