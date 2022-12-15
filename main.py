# ###########################################################
# F22 - COM S 513 - Project 3: Building an automatic debugger
# Author: Marios Tsekitsidis
# ###########################################################

from os import path
from helpers.etc import *
from diff_match_patch import diff_match_patch

class DeltaDebugger:
    def __init__(self, changes, harness):
        self.changes_incl_fault = changes
        self.harness = harness
    
    def dd2(self, c, r):
        c1 = dict(list(c.items())[len(c)//2:])
        c2 = dict(list(c.items())[:len(c)//2])  # https://stackoverflow.com/a/12988416
        #c1 = c[:len(c)//2]
        #c2 = c[len(c)//2:]  # https://stackoverflow.com/a/752330
        
        print('Step: c={} and r={}'.format(list(c.keys()), list(r.keys())))

        # Case 1 of 4:
        if len(c) == 1:
            return c
        # Case 2 of 4:
        elif self.harness({**c1,**r}):  # self.harness(c1+r):  # note: "+" here means union!
            return self.dd2(c1, r)
        # Case 3 of 4:
        elif self.harness({**c2,**r}):  # self.harness(c2+r):
            return self.dd2(c2, r)
        # Case 4 of 4:
        else:
            return {**self.dd2(c1, {**c2,**r}), **self.dd2(c2, {**c1,**r})}  # self.dd2(c1, c2+r) + self.dd2(c2, c1+r)
    
    def dd(self):
        return self.dd2(self.changes_incl_fault, {})


def is_fault_in_config(change_dict):
    change_list = list(change_dict.values())
    # Apply changes to V1 and save to temp.c:
    patch_to_new_file(change_list, path.join('test', 'get_sign_v1.c'))
    # Compile:
    compile_temp()
    # If resulting program returns seg fault, return True; else return False:
    return is_faulty(path.join('test', 'temp'))


if __name__ == '__main__':
    path_to_progV1 = path.join('test', 'get_sign_v1.c')
    path_to_progV2 = path.join('test', 'get_sign_v2.c')

    changes = extract_changes_between_files(path_to_progV1, path_to_progV2)
    dict_of_changes = {}

    print('\n' + '='*48 + '\nThere are {} changes between V1 and V2:'.format(len(changes)) + '\n' + '-'*48)

    for i, change in enumerate(changes):
        dict_of_changes[i+1] = change

        print('Change #{}:'.format(i+1))
        print(change)
    
    print('-'*48 + '\n\nDelta debugger started...\n')

    dd = DeltaDebugger(dict_of_changes, is_fault_in_config)
    dd.dd()
