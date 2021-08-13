from traits.api import HasStrictTraits
import pandas as pd
import re
import datetime

unixtime = datetime.datetime(year=1970, month=1, day=1)


class Report(HasStrictTraits):

    def __new__(self, filename):

        with open(filename, 'r') as fid:
            content = fid.readlines()
            block = dict()
            key = 'start'
            block[key] = list()
            for linenumber, line in enumerate(content[:-1]):
                if len(line.strip()) == 0:
                    key = content[linenumber + 1]
                    key = re.sub(r'\s+', ' ', key.replace('\n', '').strip())
                    block[key] = list()
                else:
                    line = re.sub(r'\s+', ' ', line.replace('\n', '').strip())
                    if line in key:
                        pass
                    elif line.startswith('---------'):
                        pass
                    else:
                        block[key].append(line.split(' '))

        pieces = []
        for key in list(block.keys()):
            if key.startswith('Node') or key.startswith('Link'):
                lst = block[key]
                lst[2:] = [x[0:len(lst[0])+1] for x in lst[2:]]
                frame = pd.DataFrame.from_dict(lst[2:])
                frame.columns = ['id'] + lst[0]
                frame[lst[0]] = frame[lst[0]].applymap(float)
                vals = key.split(' ')
                if ' at ' in key:
                    h, m, s = list(map(int, vals[3].split(':')))
                    frame['Time'] = unixtime + datetime.timedelta(hours=h, minutes=m, seconds=s)
                frame['Type'] = vals[0]
                frame.set_index(frame.id, inplace=True)
                pieces.append(frame)
        df = pd.concat(pieces)
        return df
