# -*- coding: utf-8 -*-
"""
TriHex φ ― 自己完結型 診断モジュール
--------------------------------------
■ 先天スパイラル決定ロジック
A. 干支 → 五行・陰陽 → 基本螺旋       : +100pt
B. 太陽 / 月 / ASC の 4エレメント換算
      └  Sun +5  /  Moon +3  /  ASC +3
C. 数秘マスターナンバー (11/22/33)      : 識 +30pt
D. Sun‒Moon‒ASC すべて同一エレメント    : 識 +15pt
E. 最終得点の最大螺旋を採用 (同点時は A を優先)

＊占星計算は ephem が使えない環境でも動く
  “ダミー黄経” 方式（UTCタイムスタンプのハッシュ値）で
  エレメントを一貫して決定する。
"""

from datetime import datetime as _dt
from typing import Dict, Tuple

# ─────────────────────────────────────
# 1) 干支テーブル（十干＋十二支 60 通り）
# 　 element : 木 / 火 / 土 / 金 / 水
# 　 yin_yang: 陽 / 陰
# 　 spiral  : 地 / 水 / 火 / 風 / 空 / 識
# サイズ削減のため十干・十二支から動的生成
_STEMS = "甲乙丙丁戊己庚辛壬癸"
_BRANCH = "子丑寅卯辰巳午未申酉戌亥"
ELEMENT_MAP = {
    "木":"風",
    "火":"火",
    "土":"地",
    "金":"空",
    "水":"水",
}
_YIN_YANG_STEM = ["陽","陽","陽","陽","陽","陰","陰","陰","陰","陰"]
_ELEMENT_STEM   = ["木","木","火","火","土","土","金","金","水","水"]

def _eto_table()->Dict[str,Tuple[str,str,str]]:
    tbl={}
    for i in range(60):
        stem=_STEMS[i%10]
        branch=_BRANCH[i%12]
        elem = _ELEMENT_STEM[i%10]
        yin  = _YIN_YANG_STEM[i%10]
        spiral = ELEMENT_MAP[elem]
        tbl[f"{stem}{branch}"]=(elem,yin,spiral)
    return tbl

_ETO_INFO = _eto_table()

def _eto_from_date(date)->Tuple[str,str,str,str]:
    """与えられた date → (干支, 五行, 陰陽, 螺旋)"""
    base_year=1984  # 甲子
    idx=(date.year-base_year)%60
    key=list(_ETO_INFO.keys())[idx]
    elem,yin,spiral=_ETO_INFO[key]
    return key,elem,yin,spiral

# ─────────────────────────────────────
# 2) 数秘ライフパス
def _life_path_number(date:_dt)->int:
    total=sum(int(d) for d in date.strftime("%Y%m%d"))
    while total>9 and total not in (11,22,33):
        total=sum(int(d) for d in str(total))
    return total

# ─────────────────────────────────────
# 3) 占星エレメント (ダミー算法：ライブラリ不要)
_ZODIAC_ELEM=("火","地","風","水")*3  # 12 星座 → 30° 区切り
def _deg_to_elem(deg:float)->str:
    return _ZODIAC_ELEM[int(deg//30)%12]

def _fake_longitude(dt_utc:_dt,seed:int)->float:
    """UTC タイムスタンプで 0-359.99° を擬似生成"""
    ts=int(dt_utc.timestamp())+seed
    return (ts%36000)/100.0

def _resolve_elements(birth_dt_local:_dt)->Tuple[str,str,str]:
    utc=_dt.utcfromtimestamp(birth_dt_local.timestamp())
    sun_long  = _fake_longitude(utc,0)
    moon_long = _fake_longitude(utc,111)
    asc_long  = _fake_longitude(utc,222)
    return (_deg_to_elem(sun_long),
            _deg_to_elem(moon_long),
            _deg_to_elem(asc_long))

# API 用互換名
resolve_astro_elements=_resolve_elements
resolve_elements      =_resolve_elements

# ─────────────────────────────────────
# 4) スコアリング
_BASE_PT      = 100          # 干支
_SUN_PT       = 5
_MOON_PT      = 3
_ASC_PT       = 3
_MASTER_PT    = 30
_TRIPLE_PT    = 15

def diagnose(
    birth_date:str,      # "YYYY-MM-DD"
    birth_time:str,      # "HH:MM"
    present_kanji:str="",
    ideal_kanji:str=""
)->Dict:
    dt=_dt.strptime(f"{birth_date} {birth_time}","%Y-%m-%d %H:%M")
    # A 干支
    eto_key,elem,yin,spiral=_eto_from_date(dt.date())
    scores={s:0 for s in ["地","水","火","風","空","識"]}
    scores[spiral]+=_BASE_PT

    # B 占星
    sun,moon,asc=_resolve_elements(dt)
    for e,pt in [(sun,_SUN_PT),(moon,_MOON_PT),(asc,_ASC_PT)]:
        scores[ELEMENT_MAP[e]]+=pt
    if sun==moon==asc:
        scores["識"]+=_TRIPLE_PT

    # C 数秘
    lp=_life_path_number(dt)
    if lp in (11,22,33):
        scores["識"]+=_MASTER_PT

    # D 最終決定
    max_pt=max(scores.values())
    final=[k for k,v in scores.items() if v==max_pt]
    final_spiral=spiral if spiral in final else final[0]

    return {
        "eto": eto_key,
        "element": elem,
        "yin_yang": yin,
        "life_path": lp,
        "sun_elem": sun,
        "moon_elem": moon,
        "asc_elem": asc,
        "scores": scores,
        "spiral": final_spiral,
        # ↓ 後天系統・顕現叡智は質問終了後に決定
        "lineage": None,
        "wisdom": None,
        "present_kanji": present_kanji,
        "ideal_kanji": ideal_kanji,
    }

# 旧関数名互換
trihex_diagnose = diagnose
