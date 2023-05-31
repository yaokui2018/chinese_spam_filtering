import pickle
import cut_func
import sys


def predict(word):
    """
    :param word: list
    :return:
    """
    with open('count_vect.pickle', 'rb') as fw:
        count_vect = pickle.load(fw)

    with open('tfidf_trainformer.pickle', 'rb') as fw:
        tfidf_trainformer = pickle.load(fw)

    with open('svm.pickle', 'rb') as fw:
        svclf = pickle.load(fw)

    word = cut_func.cut_sentence(word)
    word = word.split("\n")
    # print(word)
    train_count = count_vect.transform(word)
    train_tfidf = tfidf_trainformer.fit_transform(train_count)

    pre = svclf.predict(train_tfidf)
    # print(pre)
    return pre


if __name__ == '__main__':
    code = 200
    # word = sys.argv[1]
    while True:
        word = input(">> ")
        try:
            pre = str(predict(word)[0])
            print('{"code":' + str(code) + ',"msg":"ok","data":' + pre + '}')
        except Exception as e:
            print('{"code":0,"msg":"系统异常: ' + str(e) + '","data":""}')
        # predict("访问http://www.bhshare.cn评论啊")
