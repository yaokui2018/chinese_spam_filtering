
# 中文垃圾评论分类
![GitHub last commit](https://img.shields.io/github/last-commit/yaokui2018/spam_filtering)
![](https://img.shields.io/badge/python-3.7-blue)

数据集来源：[JansonKong/spam_filtering](https://github.com/JansonKong/spam_filtering)，由于原本数据集质量不是很高（标签混乱），故使用 ChatGPT 对数据进行了重新标注。

原始数据：`/normal0` 、`/spam0`

重新标注数据：`/data/normal.txt` 、`/data/spam.txt`
（正样本：731378，负样本：299854）

标注代码：`/data/data_annotate.py` (特别感谢 AIchatOS 提供的 ChatGPT api 接口!!![狗头保命])

###  依赖环境

```  
pip install -r requirements.txt
```
###  使用
  1. 分词
    ```
    >>> python run_cutdata.py
    ```
  2. 训练
    ```
    >>> python svm_filter.py
    ```
   3. 预测
    ```
    >>> python predict.py
    ```

###  演示
Demo：[http://www.bhshare.cn/AI/spam/demo.html](http://www.bhshare.cn/AI/spam/demo.html)

---

目前主要就是做了下数据集的重新标注工作，代码还是和 JansonKong 的一样的，用的SVM，后面有时间会换下模型。

 - 利用大模型（ChatGLM）进行微调示例：[LLM/chatglm-6b/fine_tune](https://github.com/yaokui2018/LLM/tree/master/chatglm-6b/fine_tune)


现存问题：在垃圾评论后面接一段很长的正常评论，会被识别成正常评论...