import sys
from typing import TypeAlias

sys.setrecursionlimit(1_000_000)
debug_flg = False

Expr: TypeAlias = int | bool | str | list['Expr']

def to_l(x: Expr) -> list[Expr]:
  if isinstance(x, list):
    return x[:-1] if x[-1] == ':q' else x
  else:
    return [x]
