#-*- coding: UTF-8 -*-
import pandas as pd

#读取数据
def readCsv(filePath):
    return pd.read_csv(filePath)

#保存数据
def saveCsv(data,filePath,flag=True):
    if flag == True:
        data.to_csv(filePath,index=False)
    elif flag == False:
        data.to_csv(filePath, index=False,header=None)

#划分数据集
def divide_data(data):
    test_data = data[((data['time'] >= 2014120800) & (data['time'] < 2014121200)) | ((data['time'] >= 2014121300) & (data['time'] < 2014121900))].reset_index(drop=True)
    verify_data = data[((data['time'] >= 2014120700) & (data['time'] < 2014121200)) | ((data['time'] >= 2014121300) & (data['time'] < 2014121800))].reset_index(drop=True)
    train_data = data[((data['time'] >= 2014120600) & (data['time'] < 2014121200)) | ((data['time'] >= 2014121300) & (data['time'] < 2014121700))].reset_index(drop=True)

    day17_data = data[(data['time'] >= 2014121700) & (data['time'] <= 2014121724)].reset_index(drop=True)
    day18_data = data[(data['time'] >= 2014121800) & (data['time'] <= 2014121824)].reset_index(drop=True)
    return train_data,verify_data,test_data,day17_data,day18_data

if __name__ == '__main__':
    ori_odata_path = "E:\\PYProject\\fresh_game\\input_data\\fresh_comp_offline\\tianchi_fresh_comp_train_user.csv"
    ori_data_path = "E:\\PYProject\\fresh_game\\output_data\\filtered_data.csv"
    train_data_save_path = "E:\\PYProject\\fresh_game\\output_data\\train_data0215.csv"
    verify_data_save_path = "E:\\PYProject\\fresh_game\\output_data\\verify_data0215.csv"
    test_data_save_path = "E:\\PYProject\\fresh_game\\output_data\\test_data0215.csv"
    day17_path = "E:\\PYProject\\fresh_game\\output_data\\day17_data.csv"
    day18_path = "E:\\PYProject\\fresh_game\\output_data\\day18_data.csv"

    ori_data = readCsv(ori_data_path)
    train_data,verify_data,test_data,day17_data,day18_data = divide_data(ori_data)

    print '训练集数量：' + str(len(train_data))
    print '验证集数量：' + str(len(verify_data))
    print '测试集数量：' + str(len(test_data))
    print '17号数量：' + str(len(day17_data))
    print '18号数量：' + str(len(day18_data))
    print '17号UI数量：' + str(len(day17_data[['user_id','item_id']].drop_duplicates()))
    print '18号UI数量：' + str(len(day18_data[['user_id','item_id']].drop_duplicates()))
    print '17号正例UI数量：' + str(len(day17_data[day17_data['behavior_type']==4][['user_id','item_id']].drop_duplicates()))
    print '18号正例UI数量：' + str(len(day18_data[day18_data['behavior_type']==4][['user_id','item_id']].drop_duplicates()))

    print '开始保存数据集！'
    saveCsv(train_data,train_data_save_path,False)
    saveCsv(test_data,test_data_save_path,False)
    saveCsv(verify_data,verify_data_save_path,False)
    saveCsv(day17_data,day17_path)
    saveCsv(day18_data,day18_path)
    print '保存完毕！'