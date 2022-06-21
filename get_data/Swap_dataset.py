import os
import random

def rename(path_old, path_new, lst):
    if not os.path.exists(path_new):
        os.makedirs(path_new, exist_ok = True)

    for i, j in zip(lst, range(len(lst))):
        os.rename(path_old + i, path_new + str(j) + '.jpg')

def change_name(path_old, path_new, folder, n_train, n_valid, n_test):
    for f1, f2, f3 in os.walk(path_old):
        l = set(f3)
        
    l_train = random.sample(l, n_train)
    l = l.difference(l_train)
    l_valid = random.sample(l, n_valid)
    l = l.difference(l_valid)
    l_test = random.sample(l, n_test)

    rename(path_old, path_new + 'train/' + folder + '/', l_train)
    rename(path_old, path_new + 'valid/' + folder + '/', l_valid)
    rename(path_old, path_new + 'test/' + folder + '/', l_test)

path_old = 'D:/Move_mouse/'
path_new = 'D:/Hand_Gestures_750/'
os.chdir(path_old)
for i in os.listdir():
    change_name(path_old + i + '/', path_new, i, n_train=600, n_valid=100, n_test=50)