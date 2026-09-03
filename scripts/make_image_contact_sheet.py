from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import math

PROJECT_ROOT = Path(__file__).resolve().parent.parent

IMAGE_DIR = (
    PROJECT_ROOT
    / "app"
    / "static"
    / "images"
    / "products"
)

OUTPUT = PROJECT_ROOT / "product_image_contact_sheet.jpg"

EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".webp",
    ".gif",
}

images = sorted(
    [
        p for p in IMAGE_DIR.iterdir()
        if p.is_file()
        and p.suffix.lower() in EXTENSIONS
    ],
    key=lambda p: p.name.lower()
)

if not images:
    print("No product images found.")
    raise SystemExit(1)

COLUMNS = 3
IMAGE_WIDTH = 300
IMAGE_HEIGHT = 230
LABEL_HEIGHT = 55

rows = math.ceil(len(images) / COLUMNS)

sheet = Image.new(
    "RGB",
    (
        COLUMNS * IMAGE_WIDTH,
        rows * (IMAGE_HEIGHT + LABEL_HEIGHT)
    ),
    "white",
)

draw = ImageDraw.Draw(sheet)

try:
    font = ImageFont.truetype("arial.ttf", 18)
except:
    font = ImageFont.load_default()

for index, image_path in enumerate(images):

    row = index // COLUMNS
    column = index % COLUMNS

    x = column * IMAGE_WIDTH
    y = row * (IMAGE_HEIGHT + LABEL_HEIGHT)

    try:
        image = Image.open(image_path).convert("RGB")

        image.thumbnail(
            (
                IMAGE_WIDTH - 20,
                IMAGE_HEIGHT - 20
            )
        )

        image_x = (
            x
            + (IMAGE_WIDTH - image.width) // 2
        )

        image_y = (
            y
            + (IMAGE_HEIGHT - image.height) // 2
        )

        sheet.paste(
            image,
            (image_x, image_y)
        )

    except Exception as error:

        draw.text(
            (x + 10, y + 10),
            f"ERROR: {error}",
            fill="red",
            font=font,
        )

    label = image_path.name

    draw.text(
        (x + 10, y + IMAGE_HEIGHT + 10),
        label,
        fill="black",
        font=font,
    )

    # Image number
    draw.text(
        (x + 10, y + 5),
        f"#{index + 1}",
        fill="black",
        font=font,
    )

sheet.save(
    OUTPUT,
    "JPEG",
    quality=95,
)

print()
print("=" * 70)
print("EAGLE FURNITURE NGARA")
print("PRODUCT IMAGE CONTACT SHEET")
print("=" * 70)
print()
print(f"Images found: {len(images)}")
print(f"Output: {OUTPUT}")
print()
print("Images:")
for index, image_path in enumerate(images, 1):
    print(f"{index:02d}. {image_path.name}")

print()
print("CONTACT SHEET CREATED SUCCESSFULLY")