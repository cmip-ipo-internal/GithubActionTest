import os 
import sys

body = os.environ['ISSUE_BODY']
print(body)
try:
  os.mkdir(sys.argv[1])
  os.system(f'touch {sys.argv[1]+"test"}')
  print('yay dsjfdskljklj dklsjf ldks fdjslkj fdskljfd slkjf dslkj fdsklj fdsj l')

except Exception as err: 
  print('FAILED',err)
