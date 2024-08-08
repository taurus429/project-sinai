def get_contrast_color(hex_color):
    # RGB 값을 0-1 범위로 변환
    hex_color = hex_color.lstrip('#')  # Remove the leading '#'
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)
    r /= 255.0
    g /= 255.0
    b /= 255.0

    # 정규화된 RGB 값을 기반으로 명도를 계산
    def calc_luminance(c):
        if c <= 0.03928:
            return c / 12.92
        else:
            return ((c + 0.055) / 1.055) ** 2.4

    luminance = 0.2126 * calc_luminance(r) + 0.7152 * calc_luminance(g) + 0.0722 * calc_luminance(b)

    # 흰색 및 검은색 대비 비율을 계산
    contrast_white = (1.05) / (luminance + 0.05)
    contrast_black = (luminance + 0.05) / 0.05

    # 대비 비율에 따라 적절한 텍스트 색상을 선택
    if contrast_white > contrast_black:
        return "#FFFFFF"  # 흰색
    else:
        return "#000000"  # 검은색