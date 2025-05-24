from datetime import date
import ephem
from modules.life_path_utils import calculate_life_path
import json

# 干支分類辞書の読み込み
def load_eto_dict():
    with open("data/eto_classification_dict.json", encoding="utf-8") as f:
        return json.load(f)

# 魂データの読み込み
def load_soulbook():
    with open("data/soulbook_master_v1.json", encoding="utf-8") as f:
        return json.load(f)

# 干支マッピング（暦補正）
eto_year_dict = {
    year: eto for year, eto in zip(range(1900, 2041), [
        "庚子", "辛丑", "壬寅", "癸卯", "甲辰", "乙巳", "丙午", "丁未", "戊申", "己酉",
        "庚戌", "辛亥", "壬子", "癸丑", "甲寅", "乙卯", "丙辰", "丁巳", "戊午", "己未",
        "庚申", "辛酉", "壬戌", "癸亥", "甲子", "乙丑", "丙寅", "丁卯", "戊辰", "己巳",
        "庚午", "辛未", "壬申", "癸酉", "甲戌", "乙亥", "丙子", "丁丑", "戊寅", "己卯",
        "庚辰", "辛巳", "壬午", "癸未", "甲申", "乙酉", "丙戌", "丁亥", "戊子", "己丑",
        "庚寅", "辛卯", "壬辰", "癸巳", "甲午", "乙未", "丙申", "丁酉", "戊戌", "己亥",
        "庚子", "辛丑", "壬寅", "癸卯", "甲辰", "乙巳", "丙午", "丁未", "戊申", "己酉",
        "庚戌", "辛亥", "壬子", "癸丑", "甲寅", "乙卯", "丙辰", "丁巳", "戊午", "己未",
        "庚申", "辛酉", "壬戌", "癸亥", "甲子", "乙丑", "丙寅", "丁卯", "戊辰", "己巳",
        "庚午", "辛未", "壬申", "癸酉", "甲戌", "乙亥", "丙子", "丁丑", "戊寅", "己卯",
        "庚辰"
    ])
}

def get_eto_from_date(year: int, month: int, day: int) -> str:
    target_date = date(year, month, day)
    spring_start = date(year, 2, 4)
    eto_year = year if target_date >= spring_start else year - 1
    return eto_year_dict.get(eto_year, "不明")

# 螺旋語りを取得
def load_spiral_definitions():
    with open("data/spiral_definitions.md", encoding="utf-8") as f:
        text = f.read()
    blocks = text.split("## ")
    spiral_map = {}
    for block in blocks[1:]:
        title, *body = block.splitlines()
        spiral_map[title.strip()] = "\n".join(body).strip()
    return spiral_map

def trihex_diagnose(name: str, year: int, month: int, day: int, current: str, ideal: str) -> dict:
    eto = get_eto_from_date(year, month, day)
    eto_dict = load_eto_dict()
    soulbook = load_soulbook()
    spiral_defs = load_spiral_definitions()

    eto_info = eto_dict.get(eto, {})
    five_element = eto_info.get("五行", "未知")
    yin_yang = eto_info.get("陰陽", "未知")
    senten = eto_info.get("先天カテゴリ", "仮カテゴリ")

    life_path = calculate_life_path(year, month, day)

    # 仮ロジック（後天・叡智カテゴリ）
    kouten = "智略系" if current in ["義", "知", "理"] else "仮カテゴリ"
    wisdom = "螺律" if ideal in ["解", "律", "理"] else "仮カテゴリ"

    soul_no = str(((life_path * len(senten)) + len(kouten) + len(wisdom)) % 216 + 1)
    soul_data = soulbook.get(soul_no, {})

    spiral_text = spiral_defs.get(senten, "（螺旋語りが未設定です）")

    return {
        "干支": eto,
        "五行": five_element,
        "陰陽": yin_yang,
        "ライフパスナンバー": life_path,
        "先天カテゴリ": senten,
        "後天カテゴリ": kouten,
        "叡智カテゴリ": wisdom,
        "魂No": int(soul_no),
        **soul_data,
        "名前": name,
        "今": current,
        "理想": ideal,
        "spiral_description": spiral_text
    }
