from typing import TypeAlias
Expr: TypeAlias = int | bool | str | list['Expr']
class Emehcs:
  def __init__(self) -> None:
    self.stack:    list[Expr] = [] # type: ignore
    self.env: dict[str, Expr] = {} # type: ignore
  def run(self, code: list[Expr]) -> Expr: ...
