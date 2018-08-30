import jieba
from gensim import corpora,models,similarities


class RecommendedHandle:
    def __init__(self,numCount):
        self.count = numCount

    def getArticleList(self,docText,docTextList):
        '''
        进行推荐
        :param docText: 母文章，格式：文章content
        :param docTextList: 子文章列表，格式：（文章id，文章content）
        :return: 文章id的list
        '''

        try:
            # 存放文章id和index的关系,格式为：docTempList[index] = 文章id
            docTempList = []
            # 分词之后的结果
            allDocList = []
            for doc in docTextList:
                docTempList.append(doc[0])
                docList = [word for word in jieba.cut(doc[1])]
                allDocList.append(docList)

            # 对母文章进行处理,分词
            docTestList = [word for word in jieba.cut(docText)]

            # 通过tfidf等算法进行形似度计算
            dictionary = corpora.Dictionary(allDocList)
            corpus = [dictionary.doc2bow(doc) for doc in allDocList]
            doc_test_vec = dictionary.doc2bow(docTestList)
            tfidf = models.TfidfModel(corpus)
            index = similarities.SparseMatrixSimilarity(tfidf[corpus], num_features=len(dictionary.keys()))
            sim = index[tfidf[doc_test_vec]]

            # 对结果进行排序
            resultTempList = sorted(enumerate(sim), key=lambda item: -item[1])

            # 根据排序结果将index转为aid
            resultList = []
            for eveTempIndex in resultTempList:
                resultList.append(docTempList[eveTempIndex[0]])

            # 返回初始化个数
            if len(resultList) > self.count:
                return resultList[0:self.count]
            else:
                return resultList
        except Exception as e:
            print(e)