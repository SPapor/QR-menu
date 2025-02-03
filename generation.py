from typing import Any

import qrcode


def generator_qrcode(link_id: Any):
    qr = qrcode.QRCode(
        version=5,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=10,
        border=4,
    )
    qr.add_data(link_id)
    qr.make(fit=True)
    img = qr.make_image(fill="black", back_color="white")
    return img
