#-*- coding: UTF-8 -*-
import pandas as pd

#读取数据
def readCsv(filePath):
    return pd.read_csv(filePath).drop(['user_geohash'],axis=1)

#保存数据
def saveCsv(data,filePath):
    data.to_csv(filePath,index=False)

#处理时间属性
def date2string(s):
    return s[0:4]+s[5:7]+s[8:10]+s[11:]

def deal_date(data):
    new_col = []
    for dateStr in data['time']:
        new_col.append(date2string(dateStr))
    data['time'] = new_col
    return data

def filter_data(xdata):
    groupData = xdata.groupby([xdata['user_id'],xdata['behavior_type']])['item_id'].count()
    group=groupData.reset_index()
    #print group
    pt=pd.pivot_table(group,values='item_id',index=['user_id'],columns='behavior_type',fill_value=0.0)
    pt=pt.reset_index()
    # print pt
    data=pt[['user_id',1,2,3,4]]
    data = data[(data[2]!=0) | (data[3]!=0)  | (data[4]!=0) ]
    data = data[(data[1]<1000)| (data[4]!=0)]
    # data0=data[data[4]==0]
    #data1=data[data[4]!=0]
    #data1['scanNum/buyNum']=data1[1]/data1[4]
    # data1= data1[data1['scanNum/buyNum']<100]
    data3=pd.merge(data,xdata,how='left',on='user_id')
    data3=data3.iloc[:,[0,5,6,7,8]]
    print data3
    return data3

if __name__ == '__main__':
    ori_data_path = "E:\\PYProject\\fresh_game\\input_data\\fresh_comp_offline\\tianchi_fresh_comp_train_user.csv"
    save_data_path = "E:\\PYProject\\fresh_game\\output_data\\filtered_data.csv"
    ori_data = readCsv(ori_data_path)
    ori_data = deal_date(ori_data)
    print '原始用户数量：'+str(len(ori_data['user_id'].drop_duplicates()))
    filter_ori_data = filter_data(ori_data)
    print '过滤后用户数量：'+str(len(filter_ori_data['user_id'].drop_duplicates()))
    saveCsv(filter_ori_data,save_data_path)
    print 'down!'