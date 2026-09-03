from PIL import Image, ImageDraw, ImageFont
import os
import math

folder = r"app/static/images/products"
output = r"product-image-audit.jpg"

files = sorted([
    f for f in os.listdir(folder)
    if f.lower().endswith((".jpg", ".jpeg", ".png", ".webp"))
])

thumb_width = 220
thumb_height = 180
columns = 4
rows = math.ceil(len(files) / columns)

sheet = Image.new(
    "RGB",
    (columns * thumb_width, rows * thumb_height),
    "white"
)

draw = ImageDraw.Draw(sheet)

for i, filename in enumerate(files):
    path = os.path.join(folder, filename)

    try:
        image = Image.open(path).convert("RGB")
        image.thumbnail((200, 135))

        x = (i % columns) * thumb_width + 10
        y = (i // columns) * thumb_height + 10

        sheet.paste(image, (x, y))

        draw.text(
            (x, y + 140),
            filename[:32],
            fill="black"
        )

    except Exception as e:
        print("Could not process:", filename, e)

sheet.save(output, quality=95)

print()
print("======================================")
print("IMAGE AUDIT CREATED SUCCESSFULLY")
print("Images:", len(files))
print("File:", output)
print("======================================")