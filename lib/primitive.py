import random
from typing import Callable, TypeAlias

Expr: TypeAlias = int | bool | str | list['Expr']

# プリミティブ関数と run() は循環している
def hundle_plus(run: Callable[[list[Expr]], Expr], stack: list[Expr]):
  ret2 = run([stack.pop()])
  ret1 = run([stack.pop()])
  stack.append(ret1 + ret2) # type: ignore
def hundle_minus(run: Callable[[list[Expr]], Expr], stack: list[Expr]):
  ret2 = run([stack.pop()])
  ret1 = run([stack.pop()])
  stack.append(ret1 - ret2) # type: ignore
def hundle_eq(run: Callable[[list[Expr]], Expr], stack: list[Expr]):
  ret2 = run([stack.pop()])
  ret1 = run([stack.pop()])
  stack.append(ret1 == ret2)
def hundle_ne(run: Callable[[list[Expr]], Expr], stack: list[Expr]):
  ret2 = run([stack.pop()])
  ret1 = run([stack.pop()])
  stack.append(ret1 != ret2)
def hundle_lt(run: Callable[[list[Expr]], Expr], stack: list[Expr]):
  ret2 = run([stack.pop()])
  ret1 = run([stack.pop()])
  stack.append(ret1 < ret2) # type: ignore
def hundle_cons(run: Callable[[list[Expr]], Expr], stack: list[Expr]):
  ret2 = run([stack.pop()])
  ret1 = run([stack.pop()])
  stack.append([ret2] + ret1) # type: ignore
def hundle_sample(run: Callable[[list[Expr]], Expr], stack: list[Expr]):
  ret2 = run([stack.pop()])
  stack.append(random.choice(ret2[:-1])) # type: ignore
def hundle_if(run: Callable[[list[Expr]], Expr], stack: list[Expr]):
  ret3 = run([stack.pop()])
  if ret3:
    ret2 = run([stack.pop()])
    stack.append(ret2)
  else:
    stack.pop()
    ret1 = run([stack.pop()])
    stack.append(ret1)
def hundle_index(run: Callable[[list[Expr]], Expr], stack: list[Expr]):
  ret2 = run([stack.pop()])
  ret1 = run([stack.pop()])
  if type(ret1) is list:
    stack.append(ret1[ret2]) # type: ignore
  else:
    stack.append(ret1[ret2] + '@') # type: ignore
def hundle_error(run: Callable[[list[Expr]], Expr], stack: list[Expr]):
  ret = run([stack.pop()])
  raise ValueError(f'error: {ret}')
def hundle_and(run: Callable[[list[Expr]], Expr], stack: list[Expr]):
  ret2 = run([stack.pop()])
  if ret2:
    ret1 = run([stack.pop()])
    stack.append(ret1)
  else:
    stack.pop()
    stack.append(False)
def hundle_up_p(run: Callable[[list[Expr]], Expr], stack: list[Expr]):
  ret3 = run([stack.pop()])
  ret2 = run([stack.pop()])
  ret1 = run([stack.pop()])
  ret1[ret2] += ret3 # type: ignore
  stack.append(ret1)
def hundle_length(run: Callable[[list[Expr]], Expr], stack: list[Expr]):
  ret = run([stack.pop()])
  stack.append(len(ret) - 1) # type: ignore
def hundle_chr(run: Callable[[list[Expr]], Expr], stack: list[Expr]):
  ret = run([stack.pop()])
  stack.append(chr(ret)) # type: ignore

funcs = {
  '+':      hundle_plus,
  '-':      hundle_minus,
  'eq':     hundle_eq,
  '!=':     hundle_ne,
  '<':      hundle_lt,
  'cons':   hundle_cons,
  'sample': hundle_sample,
  '?':      hundle_if,
  '!!':     hundle_index,
  'error':  hundle_error,
  '&&':     hundle_and,
  'up_p':   hundle_up_p,
  'length': hundle_length,
  'chr':    hundle_chr,    }
