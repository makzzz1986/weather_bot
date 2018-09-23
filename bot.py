import os

try:
    print(os.environ['OWMTOKEN'])
    print(os.environ['TGTOKEN'])
    print(os.environ['TGCHATID'])
except Exception as e:
    print(e)
