import lib.const
import random
from typing import Callable

class EmehcsBase:
  def __init__(self):
    self.stack:           list[lib.const.Expr] = []
    self.env:        dict[str, lib.const.Expr] = {}
    self.prim_funcs: dict[str, Callable[[], None]] = {
      '+':      self.hundle_plus,
      '-':      self.hundle_minus,
      'mod':    self.hundle_mod,
      'eq':     self.hundle_eq,
      '!=':     self.hundle_ne,
      '<':      self.hundle_lt,
      'car':    self.hundle_car,
      'cdr':    self.hundle_cdr,
      'cons':   self.hundle_cons,
      'sample': self.hundle_sample,
      '?':      self.hundle_if,
      '!!':     self.hundle_index,
      'error':  self.hundle_error,
      '&&':     self.hundle_and,
      'up_p':   self.hundle_up_p,
      'length': self.hundle_length,
      'chr':    self.hundle_chr,
      's.++':   self.hundle_plus,
      'eval':   self.hundle_eval,    }
  def run(self, code: list[lib.const.Expr]) -> lib.const.Expr:
    return 1 if not code else code[0]
  # プリミティブ関数と run() は相互に呼び合っている
  def hundle_plus(self):
    ret2 = self.run([self.stack.pop()])
    ret1 = self.run([self.stack.pop()])
    self.stack.append(ret1 + ret2) # type: ignore
  def hundle_minus(self):
    ret2 = self.run([self.stack.pop()])
    ret1 = self.run([self.stack.pop()])
    self.stack.append(ret1 - ret2) # type: ignore
  def hundle_mod(self):
    ret2 = self.run([self.stack.pop()])
    ret1 = self.run([self.stack.pop()])
    self.stack.append(ret1 % ret2) # type: ignore
  def hundle_eq(self):
    ret2 = self.run([self.stack.pop()])
    ret1 = self.run([self.stack.pop()])
    self.stack.append(ret1 == ret2)
  def hundle_ne(self):
    ret2 = self.run([self.stack.pop()])
    ret1 = self.run([self.stack.pop()])
    self.stack.append(ret1 != ret2)
  def hundle_lt(self):
    ret2 = self.run([self.stack.pop()])
    ret1 = self.run([self.stack.pop()])
    self.stack.append(ret1 < ret2) # type: ignore
  def hundle_car(self):
    ret1 = self.run([self.stack.pop()])
    self.stack.append(ret1[0]) # type: ignore
  def hundle_cdr(self):
    ret1 = self.run([self.stack.pop()])
    self.stack.append(ret1[1:]) # type: ignore
  def hundle_cons(self):
    ret2 = self.run([self.stack.pop()])
    ret1 = self.run([self.stack.pop()])
    self.stack.append([ret2] + ret1) # type: ignore
  def hundle_sample(self):
    ret2 = self.run([self.stack.pop()])
    self.stack.append(random.choice(ret2[:-1])) # type: ignore
  def hundle_if(self):
    ret3 = self.run([self.stack.pop()])
    if ret3:
      ret2 = self.run([self.stack.pop()])
      self.stack.append(ret2)
    else:
      self.stack.pop()
      ret1 = self.run([self.stack.pop()])
      self.stack.append(ret1)
  def hundle_index(self):
    ret2 = self.run([self.stack.pop()])
    ret1 = self.run([self.stack.pop()])
    if type(ret1) is list:
      self.stack.append(ret1[ret2]) # type: ignore
    else:
      self.stack.append(ret1[ret2] + '@') # type: ignore
  def hundle_error(self):
    ret = self.run([self.stack.pop()])
    raise ValueError(f'error: {ret}')
  def hundle_and(self):
    ret2 = self.run([self.stack.pop()])
    if ret2:
      ret1 = self.run([self.stack.pop()])
      self.stack.append(ret1)
    else:
      self.stack.pop()
      self.stack.append(False)
  def hundle_up_p(self):
    ret3 = self.run([self.stack.pop()])
    ret2 = self.run([self.stack.pop()])
    ret1 = self.run([self.stack.pop()])
    ret1[ret2] += ret3 # type: ignore
    self.stack.append(ret1)
  def hundle_length(self):
    ret = self.run([self.stack.pop()])
    self.stack.append(len(ret) - 1) # type: ignore
  def hundle_chr(self):
    ret = self.run([self.stack.pop()])
    self.stack.append(chr(ret)) # type: ignore
  def hundle_eval(self):
    _   = self.stack.pop()
    ret = self.stack.pop()
    ret = self.run(ret) # type: ignore
    self.stack.append(ret)
