import sys
from typing import TypeAlias

sys.setrecursionlimit(1_000_000)
debug_flg = False

Expr: TypeAlias = int | bool | str | list['Expr']
