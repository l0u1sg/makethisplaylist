import qrcode
from io import BytesIO
import base64
def generateQRCode(url: str, img_name: str = 'QR_Code.png') -> str:
    """
    This function generates a QR code from a given URL and saves it as an image file
    :param url: URL to generate QR code from
    :param img_name: Name of the image file
    :return: base64 encoded image
    """
    code = qrcode.QRCode(version=1, box_size=10, border=4)
    code.add_data(url)
    code.make(fit=True)
    img = code.make_image(fill_color="black", back_color="white")
    buffered = BytesIO()
    img.save(buffered)
    img_str = base64.b64encode(buffered.getvalue()).decode()
    return img_str