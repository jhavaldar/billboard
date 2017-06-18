import time

def time_map(function, set):
  # First, run the function on the first 3 indices
  index = 0
  total = len(set)
  for item in set:
    diff1=0.0
    diff2=0.0
    diff3=0.0
    start = time.time()
    function(set)
    end = time.time()
    diff = end-start
    index = index + 1

    if diff3==0.0:
      diff3=diff
      diff2=diff
      diff1=diff
    else:
      diff1=diff2
      diff2=diff3
      diff3=diff

    avg = (diff1+diff2+diff3)/3.0
    print (total-index)*avg

def func(x):
  return x*2

tons = list(xrange(10000))

time_map(func, tons)




