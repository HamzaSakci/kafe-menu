import qrcode
from PIL import Image, ImageDraw, ImageFont
import os

url = 'https://hamzasakci.github.io/kafe-menu/'
out_dir = r'C:\Users\hamza\.gemini\antigravity\scratch\kafe-qr-menu'

# 1. Standard High-Res QR Code (800x800)
qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_H,
    box_size=16,
    border=3,
)
qr.add_data(url)
qr.make(fit=True)

img_std = qr.make_image(fill_color='#12100e', back_color='#ffffff')
img_std.save(os.path.join(out_dir, 'qr_code.png'))

# 2. Premium Cafe Styled Printable Stand Card (A5 ratio: 800 x 1160 px)
card_w, card_h = 800, 1160
card = Image.new('RGB', (card_w, card_h), '#12100e')
draw = ImageDraw.Draw(card)

# Inner gold/cream decorative border
draw.rectangle([25, 25, card_w - 25, card_h - 25], outline='#d4a373', width=2)
draw.rectangle([32, 32, card_w - 32, card_h - 32], outline='#5c4735', width=1)

# Fonts
try:
    font_badge = ImageFont.truetype('arialbd.ttf', 16)
    font_title = ImageFont.truetype('georgiab.ttf', 44)
    font_sub = ImageFont.truetype('arial.ttf', 18)
    font_instruct = ImageFont.truetype('arialbd.ttf', 24)
    font_instruct_sub = ImageFont.truetype('arial.ttf', 18)
    font_wifi_label = ImageFont.truetype('arialbd.ttf', 15)
    font_wifi_val = ImageFont.truetype('arial.ttf', 19)
    font_url = ImageFont.truetype('arial.ttf', 15)
except:
    try:
        font_badge = font_title = font_sub = font_instruct = font_instruct_sub = font_wifi_label = font_wifi_val = font_url = ImageFont.truetype('arial.ttf', 20)
    except:
        font_badge = font_title = font_sub = font_instruct = font_instruct_sub = font_wifi_label = font_wifi_val = font_url = ImageFont.load_default()

# Header badge
draw.rounded_rectangle([(card_w - 240) // 2, 60, (card_w + 240) // 2, 92], radius=16, fill='#231e1a', outline='#d4a373', width=1)
draw.text((card_w // 2, 76), 'ARTISAN CAFE & LOUNGE', fill='#d4a373', font=font_badge, anchor='mm')

# Cafe Title
draw.text((card_w // 2, 140), 'AURA COFFEE', fill='#faedcd', font=font_title, anchor='mm')
draw.text((card_w // 2, 185), 'D I J I T A L   M E N U', fill='#d4a373', font=font_sub, anchor='mm')

# QR Code Background Box
qr_box_size = 480
qr_x1 = (card_w - qr_box_size) // 2
qr_y1 = 230
qr_x2 = qr_x1 + qr_box_size
qr_y2 = qr_y1 + qr_box_size

# Crisp white rounded card for QR
draw.rounded_rectangle([qr_x1, qr_y1, qr_x2, qr_y2], radius=24, fill='#ffffff', outline='#d4a373', width=4)

# Resize & paste QR
qr_resized = img_std.resize((qr_box_size - 40, qr_box_size - 40), Image.Resampling.LANCZOS)
card.paste(qr_resized, (qr_x1 + 20, qr_y1 + 20))

# Instructions below QR
draw.text((card_w // 2, 755), 'KAMERANIZ ILE OKUTUNUZ', fill='#faedcd', font=font_instruct, anchor='mm')
draw.text((card_w // 2, 795), 'Meyve Sulari  •  Sicak & Soguk Icecekler', fill='#a99985', font=font_instruct_sub, anchor='mm')

# Divider line
draw.line([(80, 840), (card_w - 80, 840)], fill='#2a231d', width=2)

# WiFi Info Box
wifi_box_y = 875
draw.rounded_rectangle([(card_w - 540) // 2, wifi_box_y, (card_w + 540) // 2, wifi_box_y + 115], radius=18, fill='#1a1614', outline='#3a3028', width=1)
draw.text((card_w // 2, wifi_box_y + 35), 'Ucretsiz Wi-Fi:  AuraCoffee_Guest', fill='#d4a373', font=font_wifi_label, anchor='mm')
draw.text((card_w // 2, wifi_box_y + 75), 'Sifre:  aura2026coffee', fill='#ffffff', font=font_wifi_val, anchor='mm')

# Direct URL & Footer
draw.text((card_w // 2, 1040), 'Menuye dogrudan ulasmak icin:', fill='#8c7e70', font=font_url, anchor='mm')
draw.text((card_w // 2, 1070), url, fill='#d4a373', font=font_url, anchor='mm')

card.save(os.path.join(out_dir, 'kafe_masa_karti_stand.png'), quality=95)
print('SUCCESS')
