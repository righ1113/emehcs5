import random
from typing import Callable, TypeAlias
from emehcs import Emehcs

Expr: TypeAlias = int | bool | str | list['Expr']

class Primitive:
  def __init__(self, emehcs: Emehcs):
    self.emehcs = emehcs
  # プリミティブ関数と run() は循環している
  def hundle_plus(self):
    ret2 = self.emehcs.run([self.emehcs.stack.pop()])
    ret1 = self.emehcs.run([self.emehcs.stack.pop()])
    self.emehcs.stack.append(ret1 + ret2) # type: ignore
  def hundle_minus(self):
    ret2 = self.emehcs.run([self.emehcs.stack.pop()])
    ret1 = self.emehcs.run([self.emehcs.stack.pop()])
    self.emehcs.stack.append(ret1 - ret2) # type: ignore
  def hundle_eq(self):
    ret2 = self.emehcs.run([self.emehcs.stack.pop()])
    ret1 = self.emehcs.run([self.emehcs.stack.pop()])
    self.emehcs.stack.append(ret1 == ret2)
  def hundle_ne(self):
    ret2 = self.emehcs.run([self.emehcs.stack.pop()])
    ret1 = self.emehcs.run([self.emehcs.stack.pop()])
    self.emehcs.stack.append(ret1 != ret2)
  def hundle_lt(self):
    ret2 = self.emehcs.run([self.emehcs.stack.pop()])
    ret1 = self.emehcs.run([self.emehcs.stack.pop()])
    self.emehcs.stack.append(ret1 < ret2) # type: ignore
  def hundle_cons(self):
    ret2 = self.emehcs.run([self.emehcs.stack.pop()])
    ret1 = self.emehcs.run([self.emehcs.stack.pop()])
    self.emehcs.stack.append([ret2] + ret1) # type: ignore
  def hundle_sample(self):
    ret2 = self.emehcs.run([self.emehcs.stack.pop()])
    self.emehcs.stack.append(random.choice(ret2[:-1])) # type: ignore
  def hundle_if(self):
    ret3 = self.emehcs.run([self.emehcs.stack.pop()])
    if ret3:
      ret2 = self.emehcs.run([self.emehcs.stack.pop()])
      self.emehcs.stack.append(ret2)
    else:
      self.emehcs.stack.pop()
      ret1 = self.emehcs.run([self.emehcs.stack.pop()])
      self.emehcs.stack.append(ret1)
  def hundle_index(self):
    ret2 = self.emehcs.run([self.emehcs.stack.pop()])
    ret1 = self.emehcs.run([self.emehcs.stack.pop()])
    if type(ret1) is list:
      self.emehcs.stack.append(ret1[ret2]) # type: ignore
    else:
      self.emehcs.stack.append(ret1[ret2] + '@') # type: ignore
  def hundle_error(self):
    ret = self.emehcs.run([self.emehcs.stack.pop()])
    raise ValueError(f'error: {ret}')
  def hundle_and(self):
    ret2 = self.emehcs.run([self.emehcs.stack.pop()])
    if ret2:
      ret1 = self.emehcs.run([self.emehcs.stack.pop()])
      self.emehcs.stack.append(ret1)
    else:
      self.emehcs.stack.pop()
      self.emehcs.stack.append(False)
  def hundle_up_p(self):
    ret3 = self.emehcs.run([self.emehcs.stack.pop()])
    ret2 = self.emehcs.run([self.emehcs.stack.pop()])
    ret1 = self.emehcs.run([self.emehcs.stack.pop()])
    ret1[ret2] += ret3 # type: ignore
    self.emehcs.stack.append(ret1)
  def hundle_length(self):
    ret = self.emehcs.run([self.emehcs.stack.pop()])
    self.emehcs.stack.append(len(ret) - 1) # type: ignore
  def hundle_chr(self):
    ret = self.emehcs.run([self.emehcs.stack.pop()])
    self.emehcs.stack.append(chr(ret)) # type: ignore
  funcs: dict[str, Callable[['Primitive'], None]] = {
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
