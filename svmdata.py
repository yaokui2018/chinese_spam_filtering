from sklearn.model_selection import train_test_split
import os


# 读取单种数据（例normal）
# 参数->  num：读取的文件数  name：文件夹名字  data：存储的数据
# 额外说明：
# num<0：读所有文件
# num=0：不读
# 0<num<=length：正常读取
# num>length：读所有文件
def singleData(num, name, data):
    os.chdir(name)
    i = 0
    length = len(os.listdir())
    if num < 0:
        num = length
    elif num > length:
        num = length
    for file in os.listdir():
        if i < num:
            fi = open(file, 'r', encoding='utf-8')
            lines = fi.readlines()
            for line in lines:
                temp = ""
                for db in line.split():
                    temp = temp + db + " "
                data.append(temp)
            i = i + 1
        else:
            break
    os.chdir('../')


# 不划分数据集，返回->  data  normal评论数  spam评论数
# 参数->  num1：读取的normal文件数  num2：读取的spam文件数
def allData(num1, num2):
    normal_data = []
    singleData(num1, '_normal', normal_data)

    num_normal = len(normal_data)

    spam_data = []
    singleData(num2, '_spam', spam_data)

    num_spam = len(spam_data)

    # num = min(num_normal, num_spam)
    # num_normal, num_spam = num, num
    #
    # data = normal_data[:num] + spam_data[:num]
    data = normal_data + spam_data

    return data, num_normal, num_spam


# 划分数据集，返回->  x_train  x_test  y_train  y_test  normal评论数  spam评论数
# 参数->  normaldoc：读取的normal文件数  spamdoc：读取的spam文件数  ratio:测试集比例
def data(normaldoc, spamdoc, ratio):
    x, num_normal, num_spam = allData(normaldoc, spamdoc)

    y = []

    for i in range(num_normal):
        y.append(1)

    for i in range(num_spam):
        y.append(0)
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=ratio, shuffle=True)

    return x_train, x_test, y_train, y_test, num_normal, num_spam
