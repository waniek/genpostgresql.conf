"""
Postgresql configuration genome
Includes only performance related options - to keep it simple

(c) Greg Jaskiewicz 2013

Licenced under PostgreSQL BSD Licence

"""

import random
import pickle

class PostgresConfig:
  """foo bar """
  _options = {'shared_buffers':'memory', 'effective_cache_size':'memory', 'checkpoint_segments':'uint',
              'checkpoint_completion_target':'0.0to1.0', 'default_statistics_target':'uint',
              'maintenance_work_mem':'memory', 'work_mem':'memory', 'wal_buffers':'memory',
              'random_page_cost':'0.0to1.0'
  }


  def __init__(self):
    """ constructor """
    self.config = self._options.copy()
    for option in self.config:
      self.config[option] = 0


  def _random_for_type(self, thetype):
    if thetype == 'memory':
      """ integer between 1kb and 1024MB """
      val = random.randint(1, 1024*1024*1024)
      return val
    elif thetype == '0.0to1.0':
      return round(random.random(), 3)
    elif thetype == 'uint':
      return random.randint(1, 1024)
    else:
      return '0'


  def set_random(self):
    self.config = self._options.copy()
    for option in self.config:
      value = self._random_for_type(self.config[option])
      self.config[option] = value


  """ pick randomly half of params from the 'mate' """
  def cross_over(self, mate):
    newconfig_keys = self.config.keys()
    random.shuffle(newconfig_keys)

    """
        now that we have randomised newconfig dictionary
        go through it, and every second option shall be replaced with mate values
    """
    i = 0
    newconfig = dict()
    for k in newconfig_keys:
      if (i%2):
        newconfig[k] =  mate.config[k]
      else:
        newconfig[k] = self.config[k]
      i = i+1

    """ and save it """
    self.config = newconfig.copy()

  def mutate_random(self, percent, number_of_mutations):
    randomkeys = self.config.keys()
    random.shuffle(randomkeys)
    randomkeys = randomkeys[0:number_of_mutations]

    for key in randomkeys:
     self.mutate_one_config(key, percent)

  def mutate_one_config(self, configkey, percent):
    value = self.config[configkey]
    key = self._options[configkey]
    variant = 0
    if key == 'memory':
      """ integer between 1kb and 1024MB """
      variant = random.randint(1, 1024*1024*1024)
      variant = variant * (percent/100.0)
      variant = variant - (1024*1024*1024*percent/100.0)/2.0
      variant = int(variant)
    elif key == '0.0to1.0':
      variant = round(random.random(), 3)
      variant = variant * (percent/100.0)
      variant = variant - (0.5*(percent/100.0))
    elif key == 'uint':
      variant = random.randint(1, 1024)
      variant = variant * (percent/100.0)
      variant = variant - (1024.0 * percent/100.0)/2.0
      variant = int(variant)
    else:
      """ nuffin """

    value = value+variant
    if (value < 0):
      value = 0

    self.config[configkey] = value



  def _memory_value_from_int(self, val):
    if (val <= 2*1024*1024):
      return '%dkb' % val
    else:
      return '%dMB' % (val/(1024*1024))


  def print_out(self):
    for option in self.config:
      if self._options[option] == 'memory':
        print option, '\t= ', self._memory_value_from_int(self.config[option])
      else:
        print option, '\t= ', self.config[option]




