from typing import Any

import qrcode
from datetime import datetime

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
def generator_qrcode(link_id:Any):
    qr = qrcode.QRCode(
        version=5,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=10,
        border=4,
    )
    qr.add_data(link_id)
    qr.make(fit=True)
    img = qr.make_image(fill="black", back_color="white")
    return img.save(f"{timestamp}.png")
generator_qrcode("https://www.youtube.com/watch?v=dQw4w9WgXcQ")