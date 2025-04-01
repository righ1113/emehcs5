from typing import TypeAlias
import re

Expr: TypeAlias = int | bool | str | list['Expr']

def run_before(str0: str) -> list[Expr]:
  def run_before_sub(data: list[str], acc: list[Expr]) -> tuple[list[Expr], list[str]]:
    match data:
      case []: return acc, []
      case [x, *xs]:
        match x:
          case '(':
            acc2, xs2 = run_before_sub(xs, [])
            return run_before_sub(xs2, acc + [acc2])
          case ')':
            return acc, xs
          case _:
            match x:
              case ':q':
                return run_before_sub(xs, acc + [':q'])
              case 'true':
                return run_before_sub(xs, acc + [True])
              case 'false':
                return run_before_sub(xs, acc + [False])
              case _:
                if x.isdecimal():
                  return run_before_sub(xs, acc + [int(x)])
                elif x[0] == '-' and x[1:].isdecimal():
                  return run_before_sub(xs, acc + [-int(x[1:])])
                else:
                  return run_before_sub(xs, acc + [x])
    raise ValueError('not match')
  str1 = re.sub(r';.*', '', str0)                     # コメント削除
  str2 = str1.replace('[]', '(:q)')                   # 空リストを変換
  str3 = str2.replace('[', '(') .replace(']', ' :q)') # 括弧変換
  str4 = str3.replace('(', '( ').replace(')', ' )')   # スペース追加
  str5 = str4.replace('\n', ' ').replace('\r', '')    # 改行削除
  return run_before_sub(str5.split(), [])[0]
