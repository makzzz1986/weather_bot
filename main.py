import os


def log(string):
    print(string)

params = {'OWMTOKEN': '', 'TGTOKEN': '', 'TGCHATID': '', 'places': {}}



# get configuration from config.txt
try:
    with open('config.txt', 'r') as config_file:
        counter = 0
        for line in config_file.readlines():
            if not line.startswith('#') and not len(line.strip()) == 0:
                counter += 1
                line_list = line.strip().split('=')
                if len(line_list) == 2:
                    if line_list[0] in params:
                        params[line_list[0]] = line_list[1]
                    else:
                        params['places'][line_list[0]] = line_list[1]
                else:
                    log('Error in line %s' % str(counter))

except FileNotFoundError:
    log('Base config file not found!')
except Exception as e:
    log(e)


env = os.environ
if 'OWMTOKEN' in env:
    params['OWMTOKEN'] = env['OWMTOKEN']
else:
    pass

print(params)
#print(env)
