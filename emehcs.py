# $ python3 emehcs.py

import sys
from typing import TypeAlias
import lib.primitive
import lib.parse

sys.setrecursionlimit(1_000_000)

Expr: TypeAlias = int | bool | str | list['Expr']

class Emehcs:
  def __init__(self):
    self.stack:    list[Expr] = [] # type: ignore
    self.env: dict[str, Expr] = {} # type: ignore
  def run(self, code: list[Expr]) -> Expr:
    def islist_run(y: Expr, em: bool) -> Expr:
      return self.run(y) if em and type(y) == list and (y[-1] != ':q') else y
    for idx, x in enumerate(code):
      em = idx == (len(code) - 1)
      # if x == '+@' or x == '-@': print(f'{idx=}, {x=}')
      match x:
        case int() | bool(): self.stack.append(x) # type: ignore
        case list():         self.stack.append(islist_run(x, em))
        case str():
          if   x in lib.primitive.funcs.keys(): lib.primitive.funcs[x](self.run, self.stack)
          elif x[0]  == '=':                    self.env[x[1:]] = islist_run(self.stack.pop(), True)
          elif x[0]  == '>':                    self.env[x[1:]] = islist_run(self.stack.pop(), False)
          elif x[-1] == '@':                    self.stack.append(x)                           # 純粋文字列
          elif isinstance(self.env[x], list):   self.stack.append(islist_run(self.env[x], em)) # 関数を参照している場合
          else:                                 self.stack.append(self.env[x])                 # 変数
        case _:
          raise ValueError(f'Unsupported type: {type(x)}')
    return self.stack.pop()

if __name__ == '__main__':
  emehcs = Emehcs()
  print(emehcs.run(lib.parse.run_before(
    '(=x ((x 1 +) rec) x (x 100 eq) ?) >rec 0 rec')))

  # with open('./sample/bf.eme', encoding='UTF-8') as f:
  #   text = f.read()
  # print(run(lib.parse.run_before(text)))
