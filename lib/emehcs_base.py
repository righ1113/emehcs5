import lib.const
import random
from typing import Callable

class EmehcsBase:
  def __init__(self, keep: list[lib.const.Expr] = [], keep_d: dict[str, lib.const.Expr] = {}):
    self.stack:               list[lib.const.Expr] = keep
    self.env:            dict[str, lib.const.Expr] = keep_d
    self.stack2:              list[lib.const.Expr] = []
    self.env2:           dict[str, lib.const.Expr] = {}
    self.prim_funcs: dict[str, Callable[[], None]] = {
      '+':       self.hundle_plus,
      '-':       self.hundle_minus,
      'eq':      self.hundle_eq,
      '!=':      self.hundle_ne,
      '<':       self.hundle_lt,
      'cons':    self.hundle_cons,
      'sample':  self.hundle_sample,
      '?':       self.hundle_if,
      '!!':      self.hundle_index,
      'error':   self.hundle_error,
      '&&':      self.hundle_and,
      'up_p':    self.hundle_up_p,
      'length':  self.hundle_length,
      'chr':     self.hundle_chr,
      'push':    self.my_push,
      'pop':     self.my_pop,
      'pop_l':   self.my_pop_l,
      'get_env': self.my_get_env,
      'set_env': self.my_set_env,
      'int?':    self.is_int,
      'bool?':   self.is_bool,
      'list?':   self.is_list,
      'car':     self.hundle_car,
      'cdr':     self.hundle_cdr,     }
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
  def my_push(self):
    ret = self.run([self.stack.pop()])
    self.stack2.append(ret)
  def my_pop(self):
    ret = self.run([self.stack2.pop()])
    self.stack.append(ret)
  def my_pop_l(self):
    ret = self.run([self.stack2.pop()])
    if type(ret) is list:
      self.stack.append(ret)
    else:
      self.stack.append([ret, ':q'])
  def my_get_env(self):
    ret = self.run([self.stack2.pop()])
    self.stack2.append(self.env2[ret]) # type: ignore
  def my_set_env(self):
    ret2 = self.run([self.stack2.pop()])
    ret1 = self.run([self.stack2.pop()])
    self.env2[ret2] = ret1 # type: ignore
  def is_int(self):
    ret = self.run([self.stack2.pop()])
    self.stack2.append(isinstance(ret, int))
  def is_bool(self):
    ret = self.run([self.stack2.pop()])
    self.stack2.append(isinstance(ret, bool))
  def is_list(self):
    ret = self.run([self.stack2.pop()])
    self.stack2.append(isinstance(ret, list))
  def hundle_car(self):
    # print(f'{self.stack=}\n{self.stack2=}\n{self.env2=}')
    ret = self.run([self.stack.pop()])
    if not ret:
      pass
    else:
      self.stack.append(ret[0]) # type: ignore
  def hundle_cdr(self):
    ret = self.run([self.stack.pop()])
    self.stack.append(ret[1:]) # type: ignore
