#-*- coding: UTF-8 -*-
import pandas as pd
from sklearn.ensemble import GradientBoostingClassifier
from  sklearn.tree import  DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn import metrics

#读取数据
def readCsv(file_path,header=True):
    if header == True:
        return pd.read_csv(file_path)
    elif header ==False:
        return pd.read_csv(file_path,header=None)

#保存数据
def saveCsv(data,filePath,flag=True):
    if flag == True:
        data.to_csv(filePath,index=False)
    elif flag ==False:
        data.to_csv(filePath, index=False,header=None)

def evaluation(true_ui,pre_ui):
    pos_ui = pd.merge(true_ui, pre_ui, on=('user_id', 'item_id'), how='inner')
    pos_ui_len = len(pos_ui)
    print pos_ui_len
    precision = pos_ui_len / (len(pre_ui) * 1.0)
    recall = pos_ui_len / (len(true_ui) * 1.0)
    f1 = (2 * precision * recall) / (precision + recall)
    print 'precison：%f' % precision
    print 'recall：%f' % recall
    print 'f1：%f' % f1

if __name__ == '__main__':
    train_data_path = "E:\\PYProject\\fresh_game\\output_data\\0216_2\\train_data_fea_0216_2.csv"
    verify_data_path = "E:\\PYProject\\fresh_game\\output_data\\0216_2\\verify_data_fea_0216_2.csv"
    test_data_path = "E:\\PYProject\\fresh_game\\output_data\\0216_2\\test_data_fea_0216_2.csv"

    # train_data_path = "E:\\PYProject\\fresh_game\\output_data\\train_data_fea_0216_1.csv"
    # verify_data_path = "E:\\PYProject\\fresh_game\\output_data\\verify_data_fea_0216_1.csv"
    # test_data_path = "E:\\PYProject\\fresh_game\\output_data\\test_data_fea_0216_1.csv"

    train_data =readCsv(train_data_path).fillna(0).drop(['time'], axis=1).drop_duplicates().reset_index(drop=True)
    verify_data = readCsv(verify_data_path).fillna(0).drop(['time'], axis=1).drop_duplicates().reset_index(drop=True)
    test_data = readCsv(test_data_path).fillna(0).drop(['time'], axis=1).drop_duplicates().reset_index(drop=True)

    print len(train_data.drop_duplicates())
    print len(verify_data.drop_duplicates())
    print len(test_data.drop_duplicates())
    # print verify_data
    train_label = train_data['label']
    train_fea = train_data.drop(['user_id', 'item_id', 'item_category', 'label'], axis=1)
    verify_label = verify_data['label']

    verify_pos_ui = verify_data[verify_data['label'] == 1].iloc[:, [0, 1]].drop_duplicates()
    print len(verify_pos_ui)
    verify_fea= verify_data.drop(['user_id', 'item_id', 'item_category', 'label'], axis=1)
    test_fea = test_data.drop(['user_id','item_id','item_category'],axis=1)

    classifier = RandomForestClassifier(n_estimators=100, criterion='gini', max_depth=10, min_samples_split=3,
                                        max_features='sqrt', bootstrap=True, n_jobs=-1, random_state=1)
    classifier.fit(train_fea, train_label)
    #pre_ver_label = classifier.predict(verify_fea)
    pre_ver_pro = classifier.predict_proba(verify_fea)
    ver_pos = []
    # print verify_label
    for index in xrange(len(verify_label)):
        if verify_label[index] == 1:
            ver_pos.append(index)
    print '实际正例：%d' % len(ver_pos)
    pre_pro_index=[]
    for index in xrange(len(pre_ver_pro)):
        if pre_ver_pro[index][1] >0.85 :
            pre_pro_index.append(index)

    # pre_ver_pos = []
    # for index in xrange(len(pre_ver_label)):
    #     if pre_ver_label[index] == 1:
    #         pre_ver_pos.append(index)


    print '预测正例：%d' %len(pre_pro_index)
    predict_verify_ui = pd.DataFrame(verify_data, index=pre_pro_index).iloc[:, [0, 1]].drop_duplicates()
    print len(predict_verify_ui)
    # print metrics.classification_report(verify_label,pre_ver_label)
    evaluation(verify_pos_ui,predict_verify_ui)
