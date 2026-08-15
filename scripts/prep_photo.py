import sys
import numpy as np
import cv2
from PIL import Image
from rembg import remove

def prep_photo(input_path, output_path="source-prepped.png"):
    print("Fotoğraf okunuyor...")
    with open(input_path, "rb") as f:
        input_bytes = f.read()

    print("Arka plan siliniyor (bu biraz sürebilir, ilk seferde model indiriliyor)...")
    output_bytes = remove(input_bytes)

    with open("temp_nobg.png", "wb") as f:
        f.write(output_bytes)

    img = Image.open("temp_nobg.png").convert("RGBA")

    # Beyaz zemine yerleştir
    background = Image.new("RGBA", img.size, (255, 255, 255, 255))
    composited = Image.alpha_composite(background, img).convert("RGB")

    # Griye çevir
    gray = np.array(composited.convert("L"))

    # CLAHE ile kontrastı artır
    clahe = cv2.createCLAHE(clipLimit=2.5, tileGridSize=(8, 8))
    enhanced = clahe.apply(gray)

    result = Image.fromarray(enhanced)
    result.save(output_path)
    print(f"{output_path} yazıldı.")

if __name__ == "__main__":
    input_path = sys.argv[1] if len(sys.argv) > 1 else "source-photo.jpg"
    prep_photo(input_path)
