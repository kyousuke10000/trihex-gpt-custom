# astro_resolver.py  ★必ずこのファイル名
# -------------------------------------------
# 太陽・月・ASC の 4エレメント(火/地/風/水)を返す簡易版
from datetime import datetime as _dt
from typing import Tuple

_ZODIAC = [
    ("牡羊座","火"),("牡牛座","地"),("双子座","風"),("蟹座","水"),
    ("獅子座","火"),("乙女座","地"),("天秤座","風"),("蠍座","水"),
    ("射手座","火"),("山羊座","地"),("水瓶座","風"),("魚座","水")
]

def _deg_to_elem(deg: float) -> str:
    idx = int(deg // 30) % 12
    return _ZODIAC[idx][1]

def _fake_longitude(dt_utc: _dt) -> float:
    seed = int(dt_utc.strftime("%Y%m%d%H%M%S"))
    return (seed % 36000) / 100.0          # 0-359.99°

def resolve_elements(
    birth_datetime: _dt,
    birth_time_str: str,
    lat: float,
    lon: float
) -> Tuple[str, str, str]:
    """(sun_elem, moon_elem, asc_elem) を返す"""
    sun_long  = _fake_longitude(birth_datetime)
    moon_long = (sun_long + 35) % 360      # ダミー
    asc_long  = (sun_long + 90) % 360      # ダミー
    return (
        _deg_to_elem(sun_long),
        _deg_to_elem(moon_long),
        _deg_to_elem(asc_long)
    )

# 旧コード互換
def resolve_astro_elements(*args, **kw):
    return resolve_elements(*args, **kw)
