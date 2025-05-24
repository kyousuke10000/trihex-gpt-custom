import os
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML
from modules.trihex_diagnosis_module import trihex_diagnose


# 診断データの仮テスト入力
test_data = {
    "name": "光一",
    "year": 1981,
    "month": 3,
    "day": 24,
    "current": "静",
    "ideal": "響"
}

# 診断実行
diagnosis = trihex_diagnose(
    name=test_data["name"],
    year=test_data["year"],
    month=test_data["month"],
    day=test_data["day"],
    current=test_data["current"],
    ideal=test_data["ideal"]
)

# テンプレート環境設定
env = Environment(loader=FileSystemLoader('.'))
template = env.get_template('trihex_soul_template_variable.html')

# Jinja2に渡す変数構造（テンプレート側に合わせて整形）
html_content = template.render(
    soul_name=diagnosis.get("name", "不明"),
    soul_reading=diagnosis.get("reading", "なし"),
    soul_no=diagnosis.get("魂No", 0),
    eto_expr=f"{diagnosis.get('干支')}（{diagnosis.get('五行')}・{diagnosis.get('陰陽')}）",
    spiral_symbol="🌀",
    spiral=diagnosis.get("先天カテゴリ", "-"),
    spiral_description=diagnosis.get("螺旋語り", "まだ語りが記されていません。"),
    present_kanji=diagnosis.get("今", "-"),
    lineage_symbol="🪞",
    lineage=diagnosis.get("後天カテゴリ", "-"),
    ideal_kanji=diagnosis.get("理想", "-"),
    wisdom_symbol="📘",
    wisdom=diagnosis.get("叡智カテゴリ", "-"),
    soul_story_lines=diagnosis.get("story", "まだ語りが記されていません").split("\n"),
    summary=diagnosis.get("summary", "-"),
)

# PDF出力
target_path = f"魂診断結果_{test_data['name']}.pdf"
HTML(string=html_content).write_pdf(target_path)

print(f"PDF出力完了: {os.path.abspath(target_path)}")
