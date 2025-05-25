import os
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML
from trihex_diagnosis_module import trihex_diagnose

# 対話式でユーザーから入力を取得
name = input("お名前を入力してください：")
year = int(input("生まれた西暦年を入力してください（例：1981）："))
month = int(input("月を入力してください（例：3）："))
day = int(input("日を入力してください（例：24）："))
current = input("今のあなたを表す漢字一文字：")
ideal = input("理想の魂状態を表す漢字一文字：")

# 7つの質問を聞く
questions = [
    "周囲からどんな印象・評価をよく受けますか？",
    "自然体でいられるときはどんなときですか？",
    "夢中で没頭したことがあるのは？",
    "意外だと言われたこと／驚かれた能力は？",
    "「自分らしさ」を実感した瞬間って？",
    "最も充実感を感じた経験はどんなとき？",
    "自分が本当にやりたい／やるべきだと感じることは？"
]
answers = []
for i, q in enumerate(questions, start=1):
    print(f"第{i}問: {q}")
    a = input("→ ")
    answers.append((q, a))

# 診断実行
diagnosis = trihex_diagnose(
    name=name,
    year=year,
    month=month,
    day=day,
    current=current,
    ideal=ideal
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
    spiral=diagnosis.get("先天カテゴリ", "不明"),
    present_kanji=diagnosis.get("今", "-"),
    lineage_symbol="🪞",
    lineage=diagnosis.get("後天カテゴリ", "-"),
    ideal_kanji=diagnosis.get("理想", "-"),
    wisdom_symbol="📘",
    wisdom=diagnosis.get("叡智カテゴリ", "-"),
    soul_story_lines=diagnosis.get("story", "まだ語りが記されていません").split("\n"),
    summary=diagnosis.get("summary", "-"),
    spiral_description=diagnosis.get("spiral_description", "-"),
    answer_pairs=answers
)

# PDF出力
filename = f"魂診断結果_{name}.pdf"
HTML(string=html_content).write_pdf(filename)
print(f"PDF出力完了: {os.path.abspath(filename)}")
pdf.add_font('NotoSansJP', '', './fonts/NotoSansJP-Regular.ttf', uni=True)

