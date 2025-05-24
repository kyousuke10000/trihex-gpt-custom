def calculate_life_path(year: int, month: int, day: int) -> int:
    """
    TriHexφ専用：ライフパスナンバー（構造振動数）を算出します。
    
    対応方式：
    - 年月日を連結（例：19810324）→ 各桁合算（1+9+8+1+0+3+2+4 = 28）
    - 繰り返し縮約 → マスター数（11, 22, 33）を除き1桁化
    
    Parameters:
        year (int): 西暦（例：1981）
        month (int): 月（1〜12）
        day (int): 日（1〜31）

    Returns:
        int: ライフパスナンバー（1〜9、または11・22・33）
    """

    def reduce_to_one_digit(n: int) -> int:
        while n > 9 and n not in (11, 22, 33):
            n = sum(int(d) for d in str(n))
        return n

    # 年月日を連結して構造振動数に変換
    date_string = f"{year}{month:02d}{day:02d}"  # 例: "19810324"
    total = sum(int(digit) for digit in date_string)
    return reduce_to_one_digit(total)
