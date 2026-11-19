import os
import qrcode
from PIL import Image, ImageDraw, ImageFont

url = "https://hamzasakci.github.io/kafe-menu/"
out_dir = r"C:\Users\hamza\.gemini\antigravity\scratch\kafe-qr-menu"

# 1. Crisp High-Contrast QR Code (ERROR_CORRECT_H)
qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_H,
    box_size=16,
    border=3,
)
qr.add_data(url)
qr.make(fit=True)

img_std = qr.make_image(fill_color="#1F162B", back_color="#FFFFFF").convert("RGB")
img_std.save(os.path.join(out_dir, "qr_code.png"))

# 2. Colorful Sunlit Cream Printable Stand Card (800 x 1160 px, A5 ratio)
card_w, card_h = 800, 1160
card = Image.new("RGB", (card_w, card_h), "#FFF8F0")
draw = ImageDraw.Draw(card)

# Subtle colorful corner circles (soft pastel wash)
overlay = Image.new("RGBA", (card_w, card_h), (0, 0, 0, 0))
odraw = ImageDraw.Draw(overlay)
odraw.ellipse([-120, 760, 320, 1200], fill=(249, 115, 22, 28))
odraw.ellipse([480, 720, 940, 1180], fill=(2, 132, 199, 28))
card = Image.alpha_composite(card.convert("RGBA"), overlay).convert("RGB")
draw = ImageDraw.Draw(card)

# Sunset Coral-to-Orange Header Gradient Band
header_h = 225
for y in range(header_h):
    t = y / max(1, header_h - 1)
    r = int(225 + (249 - 225) * t)
    g = int(29 + (115 - 29) * t)
    b = int(98 + (22 - 98) * t)
    draw.line([(0, y), (card_w, y)], fill=(r, g, b))

# Golden accent stripe under header
draw.rectangle([0, header_h, card_w, header_h + 10], fill="#FBBF24")

# Outer decorative frame
draw.rectangle([16, 16, card_w - 16, card_h - 16], outline="#EA580C", width=4)

# Windows fonts supporting Turkish characters (İ, ğ, ş, ü, ö, ç)
def load_font(names, size):
    for name in names:
        for base in [r"C:\Windows\Fonts", ""]:
            p = os.path.join(base, name) if base else name
            try:
                return ImageFont.truetype(p, size)
            except OSError:
                continue
    return ImageFont.load_default()

font_badge = load_font(["arialbd.ttf"], 17)
font_title = load_font(["georgiab.ttf", "arialbd.ttf"], 48)
font_sub = load_font(["arialbd.ttf"], 19)
font_instruct = load_font(["arialbd.ttf"], 25)
font_chip = load_font(["arialbd.ttf"], 17)
font_wifi_lbl = load_font(["arialbd.ttf"], 16)
font_wifi_val = load_font(["arialbd.ttf"], 21)
font_url = load_font(["arialbd.ttf"], 17)

# Header content
draw.rounded_rectangle([(card_w - 290) // 2, 38, (card_w + 290) // 2, 74], radius=18, fill="#B91C50", outline="#FFE4D6", width=2)
draw.text((card_w // 2, 56), "ARTISAN CAFE & LOUNGE", fill="#FFFFFF", font=font_badge, anchor="mm")
draw.text((card_w // 2, 126), "AURA COFFEE", fill="#FFFFFF", font=font_title, anchor="mm")
draw.text((card_w // 2, 180), "R E N K L İ   D İ J İ T A L   M E N Ü", fill="#FFF3D6", font=font_sub, anchor="mm")

# Pure White QR Box with Vibrant Coral Border
qr_box_size = 450
qr_x1 = (card_w - qr_box_size) // 2
qr_y1 = 270
qr_x2 = qr_x1 + qr_box_size
qr_y2 = qr_y1 + qr_box_size
draw.rounded_rectangle([qr_x1, qr_y1, qr_x2, qr_y2], radius=26, fill="#FFFFFF", outline="#EA580C", width=6)

qr_resized = img_std.resize((qr_box_size - 44, qr_box_size - 44), Image.Resampling.LANCZOS)
card.paste(qr_resized, (qr_x1 + 22, qr_y1 + 22))

# Scan Instruction
draw.text((card_w // 2, 768), "KAMERANIZ İLE OKUTUNUZ", fill="#1F162B", font=font_instruct, anchor="mm")

# Colorful Category Chips
chips = [
    ("Meyve Suları", "#FFF0E4", "#BD3E08", "#FDBA74"),
    ("Sıcak İçecekler", "#FCE7F3", "#9D174D", "#F9A8D4"),
    ("Soğuk İçecekler", "#E0F2FE", "#0369A1", "#7DD3FC"),
]
chip_w, chip_h, gap = 205, 42, 18
start_x = (card_w - (len(chips) * chip_w + (len(chips) - 1) * gap)) // 2
chip_y = 805
for idx, (label, bg, fg, bd) in enumerate(chips):
    x1 = start_x + idx * (chip_w + gap)
    draw.rounded_rectangle([x1, chip_y, x1 + chip_w, chip_y + chip_h], radius=21, fill=bg, outline=bd, width=2)
    draw.text((x1 + chip_w // 2, chip_y + chip_h // 2), label, fill=fg, font=font_chip, anchor="mm")

# Wi-Fi Card
wifi_y = 885
draw.rounded_rectangle([(card_w - 600) // 2, wifi_y, (card_w + 600) // 2, wifi_y + 115], radius=20, fill="#FFFFFF", outline="#0284C7", width=3)
draw.text((card_w // 2, wifi_y + 35), "Ücretsiz Wi-Fi Ağı:  AuraCoffee_Guest", fill="#0369A1", font=font_wifi_lbl, anchor="mm")
draw.text((card_w // 2, wifi_y + 76), "Şifre:  aura2026coffee", fill="#1F162B", font=font_wifi_val, anchor="mm")

# Footer URL
draw.text((card_w // 2, 1045), "Menüye doğrudan ulaşmak için:", fill="#554A66", font=font_wifi_lbl, anchor="mm")
draw.text((card_w // 2, 1082), url, fill="#C81E56", font=font_url, anchor="mm")

card.save(os.path.join(out_dir, "kafe_masa_karti_stand.png"), quality=95)
print("SUCCESS")
