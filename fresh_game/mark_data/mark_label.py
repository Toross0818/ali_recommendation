#-*- coding: UTF-8 -*-
import pandas as pd


#读取数据
def readCsv(file_path,header=True):
    if header== True:
        return pd.read_csv(file_path)
    elif header==False:
        return pd.read_csv(file_path,header=None)

#保存数据
def saveCsv(data,filePath,flag=True):
    if flag == True:
        data.to_csv(filePath,index=False)
    elif flag ==False:
        data.to_csv(filePath, index=False,header=None)

#判断行为，打标
def mark_label(type):
    if type == 4:
        return 1
    else:
        return 0

#打标
def mark_data(data):
    new_col = []
    for type in data['behavior_type']:
        new_col.append(mark_label(type))
    data['label'] = new_col
    return data.iloc[:, [0, 1,5]]

def mark_ori_data(ori_data,pos_data):
    data_label = pd.merge(ori_data,pos_data,on=('user_id','item_id'),how='left')
    data_label = data_label.fillna(0)
    return data_label

#数据进行采样
def sample_negData(data):
    data0 = data[data['label'] == 0]
    # print data0
    data1 = data[data['label'] == 1]
    # print len(data0)
    # print len(data1)
    data0 = data0.sample(n=17000)
    data = [data0, data1]
    data = pd.concat(data)
    return data

if __name__ == '__main__':
    train_data_path = "E:\\PYProject\\fresh_game\\output_data\\train_data0215.csv"
    verify_data_path = "E:\\PYProject\\fresh_game\\output_data\\verify_data0215.csv"
    test_data_path = "E:\\PYProject\\fresh_game\\output_data\\test_data0215.csv"
    day17_path = "E:\\PYProject\\fresh_game\\output_data\\day17_data.csv"
    day18_path = "E:\\PYProject\\fresh_game\\output_data\\day18_data.csv"

    train_data_labeled_path = "E:\\PYProject\\fresh_game\\output_data\\train_data_labeled.csv"
    verify_data_labeled_path = "E:\\PYProject\\fresh_game\\output_data\\verify_data_labeled.csv"

    ori_train_data = readCsv(train_data_path,False).rename(columns={0: 'user_id',1:'item_id',3:'item_category',4:'time'}).drop([2],axis=1)
    ori_verify_data = readCsv(verify_data_path,False).rename(columns={0: 'user_id',1:'item_id',3:'item_category',4:'time'}).drop([2],axis=1)
    ori_test_data = readCsv(test_data_path,False).rename(columns={0: 'user_id',1:'item_id',3:'item_category',4:'time'}).drop([2],axis=1)
    print len(ori_verify_data.drop_duplicates())
    print len(ori_test_data.drop_duplicates())
    day17_data = readCsv(day17_path)
    day18_data = readCsv(day18_path)

    day17_labeled_data = mark_data(day17_data).drop_duplicates()
    day18_labeled_data = mark_data(day18_data).drop_duplicates()

    day17_pos_data = day17_labeled_data[day17_labeled_data['label'] == 1].drop_duplicates()
    day18_pos_data = day18_labeled_data[day18_labeled_data['label'] == 1].drop_duplicates()


    print len(day17_labeled_data[day17_labeled_data['label'] == 1].drop_duplicates())
    print len(day18_labeled_data[day18_labeled_data['label'] == 1].drop_duplicates())

    train_data_labeled = mark_ori_data(ori_train_data,day17_pos_data).drop_duplicates()
    verify_data_labeled = mark_ori_data(ori_verify_data,day18_pos_data).drop_duplicates()

    print len(train_data_labeled.drop_duplicates())
    print len(verify_data_labeled.drop_duplicates())


    train_data_labeled = sample_negData(train_data_labeled).drop_duplicates()
    print len(train_data_labeled)
    print'开始保存数据：'
    saveCsv(train_data_labeled,train_data_labeled_path)
    saveCsv(verify_data_labeled,verify_data_labeled_path)
    print 'down!'