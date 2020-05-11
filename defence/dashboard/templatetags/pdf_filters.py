from django import template
import urllib, base64
from io import StringIO
register = template.Library()

@register.filter
def get64():
    """
    Method returning base64 image data instead of URL
    """

    with open("yourfile.ext", "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    # url=static/img/cemilac_logo_title.png
    # image = StringIO(urllib.urlopen(url).read())
    return encoded_string
