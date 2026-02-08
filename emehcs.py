# $ python3 emehcs.py

import lib.const
from   lib.emehcs_base import EmehcsBase
from   lib.repl        import Repl

# やっぱ継承だよね
class Emehcs(EmehcsBase):
  def run(self, code: list[lib.const.Expr]) -> lib.const.Expr:
    if code == [[]]: return []
    for idx, x in enumerate(code):
      em = idx == (len(code) - 1)
      if lib.const.debug_flg and (x == '+@' or x == '-@'): print(f'{idx=}, {x=}')
      match x:
        case bool() | int(): self.stack.append(x)
        case list():         self.stack.append(self._islist_run(x, em))
        case str():
          if   x in self.prim_funcs.keys():   self.prim_funcs[x]()
          elif x[0]  == '=' or x[0] == '>':   self._prefix_run(x, x[0])
          elif x[-1] == '@':                  self.stack.append(x)                                 # 純粋文字列
          elif isinstance(self.env[x], list): self.stack.append(self._islist_run(self.env[x], em)) # 関数を参照している場合
          else:                               self.stack.append(self.env[x])                       # 変数
        case _:
          raise ValueError(f'Unsupported type: {type(x)}')
    return self.stack.pop()

  def _islist_run(self, y: lib.const.Expr, em: bool) -> lib.const.Expr:
    return self.run(y) if em and type(y) == list and (y[-1] != ':q') else y

  def _prefix_run(self, x: str, sep: str):
    if x[1] == sep: self.env[x[2:]] = self._islist_run(self.stack[-1],   {'=': True, '>': False}[sep]) # ==, >>
    else:           self.env[x[1:]] = self._islist_run(self.stack.pop(), {'=': True, '>': False}[sep]) # =, >

if __name__ == '__main__':
  repl = Repl(Emehcs())
  repl.prelude()
  repl.repl()
