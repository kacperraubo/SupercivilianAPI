import pathlib
import xml.etree.ElementTree as ET

from django import template
from django.utils.safestring import SafeText, mark_safe

register = template.Library()

ICON_DIR = pathlib.Path("static/images/icons/")


@register.simple_tag
def icon(icon_name: str, class_str: str = "", **kwargs) -> SafeText:
    """Inline an SVG icon from '/static/images/icons/'.

    Args:
        icon_name: The name of the icon to inline.
        class_str: The class to add to the SVG element.
        **kwargs: Additional attributes to add to the SVG element.

    Returns:
        The SVG element as a SafeText object.
    """
    path = ICON_DIR / f"{icon_name}.svg"

    ET.register_namespace("", "http://www.w3.org/2000/svg")
    tree = ET.parse(path)

    root = tree.getroot()
    root.set("class", class_str)

    for key, value in kwargs.items():
        root.set(key, value)

    svg = ET.tostring(root, encoding="unicode", method="html")

    return mark_safe(svg)
