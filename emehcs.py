# $ python3 emehcs.py

import lib.const
import lib.parse
from lib.emehcs_base import EmehcsBase

# やっぱ継承だよね
class Emehcs(EmehcsBase):
  def run(self, code: list[lib.const.Expr]) -> lib.const.Expr:
    def islist_run(y: lib.const.Expr, em: bool) -> lib.const.Expr:
      return self.run(y) if em and type(y) == list and (y[-1] != ':q') else y
    for idx, x in enumerate(code):
      em = idx == (len(code) - 1)
      if lib.const.debug_flg and (x == '+@' or x == '-@'): print(f'{idx=}, {x=}')
      match x:
        case bool() | int(): self.stack.append(x)
        case list():         self.stack.append(islist_run(x, em))
        case str():
          if   x in self.prim_funcs.keys():   self.prim_funcs[x]()
          elif x[0]  == '=':                  self.env[x[1:]] = islist_run(self.stack.pop(), True)
          elif x[0]  == '>':                  self.env[x[1:]] = islist_run(self.stack.pop(), False)
          elif x[-1] == '@':                  self.stack.append(x)                           # 純粋文字列
          elif isinstance(self.env[x], list): self.stack.append(islist_run(self.env[x], em)) # 関数を参照している場合
          else:                               self.stack.append(self.env[x])                 # 変数
        case _:
          raise ValueError(f'Unsupported type: {type(x)}')
    return self.stack.pop()

if __name__ == '__main__':
  emehcs = Emehcs()
  print(emehcs.run(lib.parse.run_before(
    '(=x ((x 1 +) rec) x (x 100 eq) ?) >rec 0 rec')))

  with open('./sample/bf.eme', encoding='UTF-8') as f:
    text = f.read()
  print(emehcs.run(lib.parse.run_before(text)))

  print(emehcs.run(lib.parse.run_before(
    '"((=n =a0 =a1 (a0 a1 +) =b (b a1 (n 1 -) fib) a1 (n 1 eq) ?) >fib 1 0 12 fib)" eval')))
