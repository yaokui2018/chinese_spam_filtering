from cut_func import cut_sentence
from cut_func import cut_file
from cut_func import cut_save
import os

# os.chdir('normal')
# for file in os.listdir():
#     cut_save(file, '_normal')
#
# os.chdir('../spam')
# for file in os.listdir():
#     cut_save(file, '_spam')

os.chdir('data')
cut_save('normal.txt', '_normal')

cut_save('spam.txt', '_spam')
