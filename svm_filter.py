# -*- coding: utf-8 -*-

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2
from sklearn.svm import SVC
from sklearn.metrics import classification_report
import numpy as np
from tqdm import tqdm

import svmdata
import pickle


"""
train test
"""
x_train, x_test, y_train, y_test, num_normal, num_spam = svmdata.data(3, 3, 0.2)

"""
停用词,词频
"""
stop_words_file = open("stopwords.txt", 'r')
stop_words_content = stop_words_file.read()
stop_words_list = stop_words_content.splitlines()
stop_words_file.close()

count_vect = CountVectorizer(stop_words=stop_words_list, token_pattern=r"(?u)\b\w+\b")
train_count = count_vect.fit_transform(x_train)
print(train_count.shape)
test_count = count_vect.transform(x_test)
print(test_count.shape)

"""
tf-idf chi特征选择
"""
tfidf_trainformer = TfidfTransformer()
train_tfidf = tfidf_trainformer.fit_transform(train_count)
test_tfidf = tfidf_trainformer.transform(test_count)
select = SelectKBest(chi2, k=10000)
# print(X_train_tf.shape)
train_tfidf_chi = select.fit_transform(train_tfidf, y_train)
test_tfidf_chi = select.transform(test_tfidf)
# print(X_train_tf_chi.shape)
# print(X_train_tf_chi)
# print(train_tfidf_chi, test_tfidf_chi)

"""
SVM
"""
print('*************************\nSVM\n*************************')

batch_size = 51200000
epochs = 1

svclf = SVC(kernel='linear')
for epoch in range(epochs):
    # 批次训练 SVM 分类器
    for i in tqdm(range(0, len(y_train), batch_size)):
        X_batch, y_batch = train_tfidf[i:i + batch_size], y_train[i:i + batch_size]
        svclf.fit(X_batch, y_batch)
        print(f"epoch: {epoch + 1}/{epochs}, train accurancy:", svclf.score(X_batch, y_batch))
train_pre = svclf.predict(train_tfidf)
print(classification_report(train_pre, y_train))
pred_svm = svclf.predict(test_tfidf)
accuracy_svm = np.mean(pred_svm == y_test)
print("test accuracy:", accuracy_svm)
print(classification_report(pred_svm, y_test))

"""
保存模型
"""
with open('svm.pickle', 'wb') as fw:
    pickle.dump(svclf, fw)

with open('count_vect.pickle', 'wb') as fw:
    pickle.dump(count_vect, fw)

with open('tfidf_trainformer.pickle', 'wb') as fw:
    pickle.dump(tfidf_trainformer, fw)

"""
E:\win10_software\anaconda3\envs\spam_filtering\python.exe E:/NLP_study/workspace/spam_filtering-master/svm_filter.py
E:\win10_software\anaconda3\envs\spam_filtering\lib\site-packages\sklearn\feature_extraction\text.py:391: UserWarning: Your stop_words may be inconsistent with your preprocessing. Tokenizing the stop words generated tokens ['a', 'lex', 'β', 'δ', 'λ', 'ξ', 'ψ', 'в', 'ⅲ', '①①', '①②', '①③', '①④', '①⑤', '①⑥', '①⑦', '①⑧', '①⑨', '①ａ', '①ｂ', '①ｃ', '①ｄ', '①ｅ', '①ｆ', '①ｇ', '①ｈ', '①ｉ', '①ｏ', '②①', '②②', '②③', '②④', '②⑤', '②⑥', '②⑦', '②⑧', '②⑩', '②ａ', '②ｂ', '②ｄ', '②ｅ', '②ｆ', '②ｇ', '②ｈ', '②ｉ', '②ｊ', '③①', '③⑩', '③ａ', '③ｂ', '③ｃ', '③ｄ', '③ｅ', '③ｆ', '③ｇ', '③ｈ', '④ａ', '④ｂ', '④ｃ', '④ｄ', '④ｅ', '⑤ａ', '⑤ｂ', '⑤ｄ', '⑤ｅ', '⑤ｆ', '元', '吨', '数', '日', '末', '１２', 'ａ', 'ｂ', 'ｃ', 'ｅ', 'ｆ', 'ｌ', 'ｌｉ', 'ｒ', 'ｚｘｆｉｔｌ'] not in stop_words.
  'stop_words.' % sorted(inconsistent))
(96000, 55273)
(24000, 55273)
*************************
SVM
*************************
train accurancy: 0.9138645833333333
              precision    recall  f1-score   support

           0       0.93      0.90      0.92     49925
           1       0.89      0.93      0.91     46075

    accuracy                           0.91     96000
   macro avg       0.91      0.91      0.91     96000
weighted avg       0.91      0.91      0.91     96000

test accuracy: 0.8149166666666666
              precision    recall  f1-score   support

           0       0.81      0.82      0.81     11816
           1       0.82      0.81      0.82     12184

    accuracy                           0.81     24000
   macro avg       0.81      0.81      0.81     24000
weighted avg       0.82      0.81      0.81     24000


进程已结束,退出代码0

"""


"""
F:\anaconda3\python.exe E:\yaokui\spam_filtering\svm_filter.py 
F:\anaconda3\lib\site-packages\sklearn\feature_extraction\text.py:401: UserWarning: Your stop_words may be inconsistent with your preprocessing. Tokenizing the stop words generated tokens ['a', 'lex', 'β', 'δ', 'λ', 'ξ', 'ψ', 'в', 'ⅲ', '①①', '①②', '①③', '①④', '①⑤', '①⑥', '①⑦', '①⑧', '①⑨', '①ａ', '①ｂ', '①ｃ', '①ｄ', '①ｅ', '①ｆ', '①ｇ', '①ｈ', '①ｉ', '①ｏ', '②①', '②②', '②③', '②④', '②⑤', '②⑥', '②⑦', '②⑧', '②⑩', '②ａ', '②ｂ', '②ｄ', '②ｅ', '②ｆ', '②ｇ', '②ｈ', '②ｉ', '②ｊ', '③①', '③⑩', '③ａ', '③ｂ', '③ｃ', '③ｄ', '③ｅ', '③ｆ', '③ｇ', '③ｈ', '④ａ', '④ｂ', '④ｃ', '④ｄ', '④ｅ', '⑤ａ', '⑤ｂ', '⑤ｄ', '⑤ｅ', '⑤ｆ', '元', '吨', '数', '日', '末', '１２', 'ａ', 'ｂ', 'ｃ', 'ｅ', 'ｆ', 'ｌ', 'ｌｉ', 'ｒ', 'ｚｘｆｉｔｌ'] not in stop_words.
  % sorted(inconsistent)
(479766, 117981)
(119942, 117981)
*************************
SVM
*************************
  0%|          | 0/1 [00:00<?, ?it/s]
epoch: 1/1, train accurancy: 0.8612865438567968
100%|██████████| 1/1 [4:32:15<00:00, 16335.62s/it]
              precision    recall  f1-score   support

           0       0.83      0.88      0.86    225758
           1       0.89      0.84      0.87    254008

    accuracy                           0.86    479766
   macro avg       0.86      0.86      0.86    479766
weighted avg       0.86      0.86      0.86    479766

test accuracy: 0.8256157142618933
              precision    recall  f1-score   support

           0       0.79      0.85      0.82     55576
           1       0.86      0.80      0.83     64366

    accuracy                           0.83    119942
   macro avg       0.83      0.83      0.83    119942
weighted avg       0.83      0.83      0.83    119942


Process finished with exit code 0
"""