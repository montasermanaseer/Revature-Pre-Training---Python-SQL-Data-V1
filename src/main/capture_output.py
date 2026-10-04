import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

BASE = Path(__file__).resolve().parents[1]
LAB = BASE / "data"
OUT_TXT = BASE / "lab_output.txt"
OUT_IMG = BASE / "lab_output.png"

# Run the lab script and capture stdout
proc = subprocess.run(["python", "src/main/lab.py"], capture_output=True, text=True)
output = proc.stdout + "\n" + proc.stderr
OUT_TXT.write_text(output)

# Create a simple image with the text (wrap lines)
lines = output.splitlines()
font = ImageFont.load_default()
max_width = 1200
# Pillow >= 10 uses getbbox instead of getsize for FreeType fonts
try:
    bbox = font.getbbox("A")
    line_height = bbox[3] - bbox[1] + 2
except Exception:
    line_height = font.getsize("A")[1] + 2
img_height = line_height * (len(lines) + 2)
img = Image.new("RGB", (max_width, img_height), color=(255, 255, 255))
draw = ImageDraw.Draw(img)

y = 0
for line in lines:
    draw.text((5, y), line, font=font, fill=(0, 0, 0))
    y += line_height

img.save(OUT_IMG)
print(f"Wrote {OUT_TXT} and {OUT_IMG}")
