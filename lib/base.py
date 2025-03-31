import random

# プリミティブ関数と run() は循環している
def hundle_plus(run, stack):
  ret2 = run([stack.pop()])
  ret1 = run([stack.pop()])
  stack.append(ret1 + ret2)
def hundle_minus(run, stack):
  ret2 = run([stack.pop()])
  ret1 = run([stack.pop()])
  stack.append(ret1 - ret2)
def hundle_eq(run, stack):
  ret2 = run([stack.pop()])
  ret1 = run([stack.pop()])
  stack.append(ret1 == ret2)
def hundle_ne(run, stack):
  ret2 = run([stack.pop()])
  ret1 = run([stack.pop()])
  stack.append(ret1 != ret2)
def hundle_lt(run, stack):
  ret2 = run([stack.pop()])
  ret1 = run([stack.pop()])
  stack.append(ret1 < ret2)
def hundle_cons(run, stack):
  ret2 = run([stack.pop()])
  ret1 = run([stack.pop()])
  stack.append([ret2] + ret1)
def hundle_sample(run, stack):
  ret2 = run([stack.pop()])
  stack.append(random.choice(ret2[:-1]))
def hundle_if(run, stack):
  ret3 = run([stack.pop()])
  if ret3:
    ret2 = run([stack.pop()])
    stack.append(ret2)
  else:
    stack.pop()
    ret1 = run([stack.pop()])
    stack.append(ret1)
def hundle_index(run, stack):
  ret2 = run([stack.pop()])
  ret1 = run([stack.pop()])
  if type(ret1) is list:
    stack.append(ret1[ret2])
  else:
    stack.append(ret1[ret2] + '@')
def hundle_error(run, stack):
  ret = run([stack.pop()])
  raise ValueError(f'error: {ret}')
def hundle_and(run, stack):
  ret2 = run([stack.pop()])
  if ret2:
    ret1 = run([stack.pop()])
    stack.append(ret1)
  else:
    stack.pop()
    stack.append(False)
def hundle_up_p(run, stack):
  ret3 = run([stack.pop()])
  ret2 = run([stack.pop()])
  ret1 = run([stack.pop()])
  ret1[ret2] += ret3
  stack.append(ret1)
def hundle_length(run, stack):
  ret = run([stack.pop()])
  stack.append(len(ret) - 1)
def hundle_chr(run, stack):
  ret = run([stack.pop()])
  stack.append(chr(ret))

prim_funcs = {
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
