from PyQt5.QtGui import QFontDatabase


def load_custom_font(font_path):
    """Load a custom font from a file and return its family name."""
    font_id = QFontDatabase.addApplicationFont(font_path)
    if font_id != -1:
        font_family = QFontDatabase.applicationFontFamilies(font_id)
        if font_family:
            return font_family[0]
    return None