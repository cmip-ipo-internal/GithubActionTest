import os 
import sys

body = os.environ.keys()
print(body)
try:
  os.mkdir(sys.argv[1])
  os.system(f'touch {sys.argv[1]+"test"}')
  print(sys.argv[1]+'yay')

except Exception as err: 
  print('FAILED',err)


'''
env 
GITHUB_WORKSPACE = directory location
same as 'PWD': '/home/runner/work/GithubActionTest/GithubActionTest'

'GITHUB_TRIGGERING_ACTOR': 'wolfiex',


'GITHUB_REPOSITORY': 'cmip-ipo-internal/GithubActionTest'

'''

