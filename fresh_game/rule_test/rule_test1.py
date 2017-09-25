#-*- coding: UTF-8 -*-
import pandas as pd

#读取数据
def readCsv(file_path,header=True):
    if header == True:
        return pd.read_csv(file_path).drop_duplicates()
    elif header ==False:
        return pd.read_csv(file_path,header=None).drop_duplicates()

#保存数据
def saveCsv(data,filePath,flag=True):
    if flag == True:
        data.to_csv(filePath,index=False)
    elif flag ==False:
        data.to_csv(filePath, index=False,header=None)

def rule2(data,item_data):
    data = data[(data['time'] >= 2014121700) & (data['time'] <= 2014121724)]

    car_data = data[data['behavior_type'] == 3].iloc[:, [0, 1, 3, 4]]
    buy_data = data[data['behavior_type'] == 4].iloc[:, [0, 1, 3, 4]]
    # car_data = car_data.rename(columns={'item_id':'car_item_id','time':'car_time'})
    # buy_data = buy_data.rename(columns={'item_id':'buy_item_id','time':'buy_time'})

    # print car_data[['user_id','item_id']].drop_duplicates()
    # print buy_data[['user_id', 'item_id']].drop_duplicates()
    car_data = car_data.rename(columns={'item_category': 'car_item_category', 'time': 'car_time'})
    buy_data = buy_data.rename(columns={'item_category': 'buy_item_category', 'time': 'buy_time'})
    print '放购物车UI：%d' % len(car_data[['user_id', 'item_id']].drop_duplicates())
    ####### step 1:去除当天购买 ###########
    car_not_buy = pd.merge(car_data, buy_data, how='left', on=('user_id', 'item_id'))
    car_not_buy = car_not_buy[(car_not_buy['buy_time'].isnull()) | (car_not_buy['buy_time'] < car_not_buy['car_time'])].iloc[:,[0, 1, 2, 3]]
    print 'step 1:过滤当天购买了的UI：%d' % len(car_not_buy[['user_id', 'item_id']].drop_duplicates())
    #print car_not_buy
    ###### step 2: 打分取出topK个UI #######
    not_buy_data = pd.merge(data,car_not_buy,on=('user_id', 'item_id'),how='left')
    not_buy_data = not_buy_data[not_buy_data['car_time'].notnull()]
    group_data = not_buy_data.groupby([not_buy_data['user_id'],not_buy_data['item_id'],not_buy_data['behavior_type']])['time'].count()
    group_data = group_data.reset_index()
    group_data['scores'] = group_data['behavior_type']*group_data['time']
    group_data =group_data.groupby([group_data['user_id'],group_data['item_id']])['scores'].sum().reset_index()
    print group_data
    group_data = group_data.sort(['scores'],ascending=False)
    #print group_data
    top_k_data = group_data[:13000]
    print top_k_data
   # group_data = group_data[group_data['scores']>= (group_data['scores'].mean())].sort(['scores'],ascending=False).reset_index(drop=True).drop(['scores'],axis=1)

    car_topK = pd.merge(car_data,top_k_data,on=('user_id','item_id'),how='inner').rename(columns={'car_item_category':'item_category'})

    ###### step 2：去除购买了同类型的 ######
    buy_data = buy_data.rename(columns={'buy_item_category': 'item_category', 'item_id': 'buy_item_id'})
    car_topK = car_topK.rename(columns={'car_item_category': 'item_category', 'item_id': 'car_item_id'})
    car_not_buy_cate = pd.merge(car_topK, buy_data, how='left', on=('user_id', 'item_category'))
    # print car_not_buy_cate
    car_not_buy_cate = car_not_buy_cate[(car_not_buy_cate['buy_time'].isnull()) | (
    car_not_buy_cate['buy_time'] < car_not_buy_cate['car_time'])].iloc[:, [0, 1, 2, 3]].rename(
        columns={'car_item_id': 'item_id', 'car_time': 'time'})
    print 'step 2:过滤当天购买了的同类型UI：%d' % len(car_not_buy_cate[['user_id', 'item_id']].drop_duplicates())
    ui_in_item = pd.merge(car_not_buy_cate,item_data,how='inner',on='item_id').iloc[:,[0,1]].drop_duplicates()
    print '最后的UI对：%d' %len(ui_in_item)
    return ui_in_item


def rule1(data,item_data):
    data  = data[(data['time'] >= 2014121700) & (data['time'] <= 2014121724)]
    car_data = data[data['behavior_type'] == 3].iloc[:,[0,1,3,4]]
    buy_data = data[data['behavior_type'] == 4].iloc[:,[0,1,3,4]]
    # car_data = car_data.rename(columns={'item_id':'car_item_id','time':'car_time'})
    # buy_data = buy_data.rename(columns={'item_id':'buy_item_id','time':'buy_time'})

    # print car_data[['user_id','item_id']].drop_duplicates()
    # print buy_data[['user_id', 'item_id']].drop_duplicates()

    #########去除购买的########
    car_data = car_data.rename(columns={'item_category':'car_item_category','time':'car_time'})
    buy_data = buy_data.rename(columns={'item_category':'buy_item_category','time':'buy_time'})
    print '放购物车UI：%d' %len(car_data[['user_id','item_id']].drop_duplicates())
    ####### step 1:去除当天购买 ###########
    car_not_buy = pd.merge(car_data,buy_data,how='left',on=('user_id','item_id'))
    car_not_buy = car_not_buy[(car_not_buy['buy_time'].isnull())|(car_not_buy['buy_time']<car_not_buy['car_time'])].iloc[:,[0,1,2,3]]
    print 'step 1:过滤当天购买了的UI：%d' %len(car_not_buy[['user_id','item_id']].drop_duplicates())
    #print car_not_buy
    ###### step 2：去除购买了同类型的 ######
    buy_data = buy_data.rename(columns={'buy_item_category':'item_category','item_id':'buy_item_id'})
    car_not_buy = car_not_buy.rename(columns={'car_item_category':'item_category','item_id':'car_item_id'})
    car_not_buy_cate = pd.merge(car_not_buy,buy_data,how='left',on=('user_id','item_category'))
    #print car_not_buy_cate
    car_not_buy_cate = car_not_buy_cate[(car_not_buy_cate['buy_time'].isnull()) | (car_not_buy_cate['buy_time'] < car_not_buy_cate['car_time'])].iloc[:,[0,1,2,3]].rename(columns={'car_item_id':'item_id','car_time':'time'})
    print 'step 2:过滤当天购买了的同类型UI：%d' %len(car_not_buy_cate[['user_id','item_id']].drop_duplicates())
    #print  car_not_buy_cate

    ###### step 3：取出最后放购物车时间为23点，20点，15点 ######
    car_not_buy_cate_time = car_not_buy_cate.groupby(car_not_buy_cate['user_id'])[['time']].agg('max').reset_index().rename(columns={'time':'last_time'})
    car_not_buy_cate_time  = pd.merge(car_not_buy_cate,car_not_buy_cate_time,how='inner',on='user_id')
    cnb_time_in = car_not_buy_cate_time[(car_not_buy_cate_time['last_time'] == 2014121715) | (car_not_buy_cate_time['last_time'] == 2014121720) | (car_not_buy_cate_time['last_time'] == 2014121723)]
    #cnb_time_in = car_not_buy_cate_time[(car_not_buy_cate_time['last_time'] > 2014121716)]
    print 'step 3:根据最后放购物车时间过滤UI：%d' % len(cnb_time_in[['user_id', 'item_id']].drop_duplicates())
    # print car_data
    # print buy_data
    #
    # buy_car_data = pd.merge(car_data,buy_data,how='left',on=('user_id','item_category'))
    # print buy_car_data
    # buyed_car_data = buy_car_data[(buy_car_data['buy_time'].isnull()) |(buy_car_data['buy_time'] < buy_car_data['car_time'])]
    # buyed_time_data = buyed_car_data[buyed_car_data['car_time'] > 2014121817].iloc[:,[0,1]].rename(columns={'car_item_id':'item_id'}).drop_duplicates()
    ui_in_item = pd.merge(cnb_time_in,item_data,how='inner',on='item_id').iloc[:,[0,1]].drop_duplicates()
    print '最后的UI对：%d' %len(ui_in_item)
    return ui_in_item



def rule3(data,item_data):
    data = data[(data['time'] >= 2014121700) & (data['time'] <= 2014121724)]
    car_data = data[data['behavior_type'] == 3].iloc[:, [0, 1, 3, 4]]
    buy_data = data[data['behavior_type'] == 4].iloc[:, [0, 1, 3, 4]]
    # car_data = car_data.rename(columns={'item_id':'car_item_id','time':'car_time'})
    # buy_data = buy_data.rename(columns={'item_id':'buy_item_id','time':'buy_time'})

    # print car_data[['user_id','item_id']].drop_duplicates()
    # print buy_data[['user_id', 'item_id']].drop_duplicates()

    #########去除购买的########
    car_data = car_data.rename(columns={'item_category': 'car_item_category', 'time': 'car_time'})
    buy_data = buy_data.rename(columns={'item_category': 'buy_item_category', 'time': 'buy_time'})
    print '放购物车UI：%d' % len(car_data[['user_id', 'item_id']].drop_duplicates())
    ####### step 1:去除当天购买 ###########
    car_not_buy = pd.merge(car_data, buy_data, how='left', on=('user_id', 'item_id'))
    car_not_buy = car_not_buy[
                      (car_not_buy['buy_time'].isnull()) | (car_not_buy['buy_time'] < car_not_buy['car_time'])].iloc[:,
                  [0, 1, 2, 3]]
    print 'step 1:过滤当天购买了的UI：%d' % len(car_not_buy[['user_id', 'item_id']].drop_duplicates())

    ###### step 2：去除购买了同类型的 ######
    buy_data = buy_data.rename(columns={'buy_item_category': 'item_category', 'item_id': 'buy_item_id'})
    car_not_buy = car_not_buy.rename(columns={'car_item_category': 'item_category', 'item_id': 'car_item_id'})
    car_not_buy_cate = pd.merge(car_not_buy, buy_data, how='left', on=('user_id', 'item_category'))
    # print car_not_buy_cate
    car_not_buy_cate = car_not_buy_cate[(car_not_buy_cate['buy_time'].isnull()) | (
    car_not_buy_cate['buy_time'] < car_not_buy_cate['car_time'])].iloc[:, [0, 1, 2, 3]].rename(
        columns={'car_item_id': 'item_id', 'car_time': 'time'})
    print 'step 2:过滤当天购买了的同类型UI：%d' % len(car_not_buy_cate[['user_id', 'item_id']].drop_duplicates())

    ###### step 3：取出最后放购物车时间为23点，20点，15点 ######
    car_not_buy_cate_time = car_not_buy_cate.groupby(car_not_buy_cate['user_id'])[['time']].agg(
        'max').reset_index().rename(columns={'time': 'last_time'})
    car_not_buy_cate_time = pd.merge(car_not_buy_cate, car_not_buy_cate_time, how='inner', on='user_id')
    cnb_time_in = car_not_buy_cate_time[(car_not_buy_cate_time['last_time'] == 2014121712)|(car_not_buy_cate_time['last_time'] == 2014121720)|(car_not_buy_cate_time['last_time'] == 2014121719)|(car_not_buy_cate_time['last_time'] == 2014121709)|(car_not_buy_cate_time['last_time'] == 2014121710)  | (car_not_buy_cate_time['last_time'] == 2014121722)|(car_not_buy_cate_time['last_time'] == 2014121721) | (car_not_buy_cate_time['last_time'] == 2014121723)]
    #cnb_time_in = car_not_buy_cate_time[(car_not_buy_cate_time['last_time'] > 2014121718)]

    print 'step 3:根据最后放购物车时间过滤UI：%d' % len(cnb_time_in[['user_id', 'item_id']].drop_duplicates())

    # ###### step 2: 打分取出topK个UI #######
    # not_buy_data = pd.merge(data, cnb_time_in, on=('user_id', 'item_id'), how='left')
    # print not_buy_data
    # not_buy_data = not_buy_data[not_buy_data['last_time'].notnull()]
    # print not_buy_data
    # group_data =not_buy_data.groupby([not_buy_data['user_id'], not_buy_data['item_id'], not_buy_data['behavior_type']])['time_x'].count()
    # group_data = group_data.reset_index()
    # group_data['scores'] = group_data['behavior_type'] * group_data['time_x']
    # group_data = group_data.groupby([group_data['user_id'], group_data['item_id']])['scores'].sum().reset_index()
    # group_data = group_data[group_data['scores']>1]


    i_in_item = pd.merge(cnb_time_in, item_data, how='inner', on='item_id').iloc[:, [0, 1]].drop_duplicates()
    print '最后的UI对：%d' % len(i_in_item)
    return i_in_item


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
    #ori_data_path = "E:\\PYProject\\fresh_game\\input_data\\fresh_comp_offline\\tianchi_fresh_comp_train_user.csv"
    data_path = "E:\\PYProject\\fresh_game\\output_data\\test_data0215.csv"
    item_path = "E:\\PYProject\\fresh_game\\input_data\\fresh_comp_offline\\tianchi_fresh_comp_train_item.csv"
    res_save_path = 'E:\\PYProject\\fresh_game\\output_data\\res1.csv'
    #res_path = 'E:\\PYProject\\FeatureDivdeTest\\output\\tianchi_mobile_recommendation_predict.csv'

    data = readCsv(data_path,False).rename(columns={0: 'user_id',1:'item_id',2:'behavior_type',3:'item_category',4:'time'})
    #print  data
    true_ui = data[(data['time'] >= 2014121800) & (data['time'] <= 2014121824) &(data['behavior_type']==4)][['user_id','item_id']].drop_duplicates()
    item_data = readCsv(item_path)
    #d17 = data[(data['time'] >= 2014121700) & (data['time'] <= 2014121724) &(data['behavior_type']==3)][['user_id','item_id']].drop_duplicates()
    #print true_ui
    true_ui_in = pd.merge(true_ui,item_data,on=['item_id'],how='inner')[['user_id','item_id']].drop_duplicates()
    #pre_ui_in = pd.merge(d17,item_data,on=['item_id'],how='inner')[['user_id','item_id']].drop_duplicates()
    print true_ui_in
    #print pre_ui_in
    # res1=rule1(data,item_data)
    #res2 = rule2(data,item_data)
    res3 = rule3(data,item_data)
    evaluation(true_ui_in,res3)

    # print len(res1)
    # print len(res2)
    # res = pd.merge(res1,res2,on=('user_id', 'item_id'),how='inner')
    # print res
    #saveCsv(res3,res_save_path)
    print 'down!'
