# $ python3 emehcs.py

import sys
from typing import TypeAlias
import lib.base
import lib.parse

sys.setrecursionlimit(1_000_000)

Expr:      TypeAlias = int | bool | str | list['Expr']
stack:    list[Expr] = []
env: dict[str, Expr] = {}

def run(code: list[Expr]) -> Expr:
  def islist_run(y: Expr, em: bool) -> Expr:
    return run(y) if em and type(y) == list and (y[-1] != ':q') else y
  global stack, env
  for idx, x in enumerate(code):
    em = idx == (len(code) - 1)
    # if x == '+@' or x == '-@': print(f'{idx=}, {x=}')
    match x:
      case int() | bool(): stack.append(x) # type: ignore
      case list():         stack.append(islist_run(x, em))
      case str():
        if   x in lib.base.prim_funcs.keys(): lib.base.prim_funcs[x](run, stack)
        elif x[0]  == '=':                    env[x[1:]] = islist_run(stack.pop(), True)
        elif x[0]  == '>':                    env[x[1:]] = islist_run(stack.pop(), False)
        elif x[-1] == '@':                    stack.append(x)                      # 純粋文字列
        elif isinstance(env[x], list):        stack.append(islist_run(env[x], em)) # 関数を参照している場合
        else:                                 stack.append(env[x])                 # 変数
      case _:
        raise ValueError(f'Unsupported type: {type(x)}')
  return stack.pop()

print(run(lib.parse.run_before(
  '(=x ((x 1 +) rec) x (x 100 eq) ?) >rec 0 rec')))

with open('./sample/bf.eme', encoding='UTF-8') as f:
  text = f.read()
print(run(lib.parse.run_before(text)))
