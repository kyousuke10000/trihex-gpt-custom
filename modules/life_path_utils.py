"""
life_path_utils.py
ライフパスナンバー計算（マスターナンバー保持）
"""

def calculate_life_path_number(date_obj):
    # 例: 1990-01-23 → 1+9+9+0+0+1+2+3 = 25 → 2+5 = 7
    total = sum(int(d) for d in date_obj.strftime("%Y%m%d"))
    while total > 9 and total not in (11, 22, 33):
        total = sum(int(d) for d in str(total))
    return total
