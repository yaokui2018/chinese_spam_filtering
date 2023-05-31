# matrixdata测试
"""
import matrixdata
from gensim.models import Word2Vec

model=Word2Vec.load('save.model')

data=[]

matrixdata.singleData(1,'_normal',data,model)

"""
# svmdata测试
import svmdata

data = []

x_train, x_test, y_train, y_test, num_normal, num_spam = svmdata.data(25, 25, 0.2)

print(len(x_train), len(x_test))
print(x_train[0])


# import time
#
# import requests
#
# response = requests.post("http://www.bhshare.cn/", stream=True)
# # 遍历所有的数据块并打印出来
# if (response.status_code == 200):
#     pre = b''
#     for chunk in response.iter_content(chunk_size=2):
#         if chunk:
#             pre += chunk
#             try:
#                 print(pre.decode('utf-8').replace("\n", "\\n"), end='', flush=True)
#                 pre = b''
#                 time.sleep(0.1)  # 仅仅是为了更加直观的展示“打字机”效果，实际使用时应删除
#             except UnicodeDecodeError:
#                 # 当前chunk数据不完整无法被正确解码时会报UnicodeDecodeError异常，临时存储起来与下一个chunk合并解码
#                 pass
