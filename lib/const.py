import sys
from typing import TypeAlias

sys.setrecursionlimit(1_000_000)
debug_flg = False

Expr: TypeAlias = int | bool | str | list['Expr']

READLINE_HIST_FILE = './data/.readline_history'
PRELUDE_FILE       = './data/prelude.eme'
EMEHCS_VERSION     = 'emehcs(p) version 0.2.0'
