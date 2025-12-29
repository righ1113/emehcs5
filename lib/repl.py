# -*- coding: utf-8 -*-
import os
import readline
import lib.const
import lib.parse
from typing import TYPE_CHECKING
if TYPE_CHECKING:
  import emehcs

class Repl:
  def __init__(self, emehcs_obj: "emehcs.Emehcs"):
    self.emehcs_obj = emehcs_obj
    hist_file = lib.const.READLINE_HIST_FILE
    if os.path.exists(hist_file):
      with open(hist_file, 'r', encoding='utf-8') as f:
        for line in f:
          readline.add_history(line.rstrip('\n'))

  def prelude(self):
    if not os.path.exists(lib.const.PRELUDE_FILE):
      print('no prelude.')
      return
    with open(lib.const.PRELUDE_FILE, 'r', encoding='utf-8') as f:
      codes = f.read().split('|')
    for c in codes:
      self.emehcs_obj.run(lib.parse.run_before(c))

  def repl(self):
    print(lib.const.EMEHCS_VERSION)
    while True:
      try:
        line = input('emehcs> ')
        if line == '':
          raise EOFError
        prompt = line.rstrip('\n')
        if prompt == 'exit':
          break

        if prompt.startswith('loadFile'):
          path = prompt[9:].lstrip()
          codes = []
          with open(path, 'r', encoding='utf-8') as f:
            codes = f.read().split('|')
          for c in codes:
            print(self.emehcs_obj.run(lib.parse.run_before(c)))
        elif '|' in prompt:
          for c in prompt.split('|'):
            print(self.emehcs_obj.run(lib.parse.run_before(c)))
        else:
          print(self.emehcs_obj.run(lib.parse.run_before(prompt)))

      except (EOFError, KeyboardInterrupt):
        print("\nBye!")
        hist_file = lib.const.READLINE_HIST_FILE
        try:
          length = readline.get_current_history_length()
          with open(hist_file, 'w', encoding='utf-8') as f:
            for i in range(1, length + 1):
              item = readline.get_history_item(i)
              if item != '':
                f.write(item + '\n')
        except Exception:
          pass
        break
      except Exception as e:
        print(f"Error: {e}")
