#-*- coding: UTF-8 -*-
import pandas as pd

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

#merge特征
def merge_fea_data(ori_data,u_fea,i_fea,ui_fea):
    ori_u_data = pd.merge(ori_data,u_fea,on='user_id',how='left')
    ori_u_i_data = pd.merge(ori_u_data,i_fea,on='item_id',how='left')
    ori_u_i_c_data = pd.merge(ori_u_i_data,ui_fea,on=('user_id','item_id'),how='left')
    # print ori_u_i_c_data
    return  ori_u_i_c_data.fillna(0)

def merge_fea_data(ori_data,u_fea,i_fea,ui_fea,c_fea):
    ori_u_data = pd.merge(ori_data,u_fea,on='user_id',how='left')
    ori_u_i_data = pd.merge(ori_u_data,i_fea,on='item_id',how='left')
    ori_u_i_c_data = pd.merge(ori_u_i_data,ui_fea,on=('user_id','item_id'),how='left')
    # print ori_u_i_c_data
    # print c_fea
    cri_u_i_C_ui_data = pd.merge(ori_u_i_c_data,c_fea,how='left',on='item_category')
    # print ori_u_i_c_data
    return  cri_u_i_C_ui_data

if __name__ == '__main__':
    # ori_train_data_path = "E:\\PYProject\\fresh_game\\output_data\\train_data_labeled.csv"
    # ori_verify_data_path = "E:\\PYProject\\fresh_game\\output_data\\verify_data_labeled.csv"
    # ori_test_data_path = "E:\\PYProject\\fresh_game\\output_data\\test_data0215.csv"
    # item_data_path = "E:\\PYProject\\fresh_game\\input_data\\fresh_comp_offline\\tianchi_fresh_comp_train_item.csv"
    # # cf_train_path = "E:\\PYProject\\fresh_game\\input_data\\fea_0214\\cate_fea_train.csv"
    # # cf_verify_path = "E:\\PYProject\\fresh_game\\input_data\\fea_0214\\cate_fea_verify.csv"
    # # cf_test_path = "E:\\PYProject\\fresh_game\\input_data\\fea_0214\\cate_fea_test.csv"
    #
    # uif_train_path = "E:\\PYProject\\fresh_game\\input_data\\fea_0216\\0216_ui_t_f_train.csv"
    # uif_verify_path = "E:\\PYProject\\fresh_game\\input_data\\fea_0216\\0216_ui_t_f_verify.csv"
    # uif_test_path = "E:\\PYProject\\fresh_game\\input_data\\fea_0216\\0216_ui_t_f_test.csv"
    #
    #
    # uf_train_path="E:\\PYProject\\fresh_game\\input_data\\fea_0216\\0216_u_t_f_train.csv"
    # uf_verify_path = "E:\\PYProject\\fresh_game\\input_data\\fea_0216\\0216_u_t_f_verify.csv"
    # uf_test_path= "E:\\PYProject\\fresh_game\\input_data\\fea_0216\\0216_u_t_f_test.csv"
    #
    # if_train_path = "E:\\PYProject\\fresh_game\\input_data\\fea_0216\\0216_i_t_f_train.csv"
    # if_verify_path = "E:\\PYProject\\fresh_game\\input_data\\fea_0216\\0216_i_t_f_verify.csv"
    # if_test_path = "E:\\PYProject\\fresh_game\\input_data\\fea_0216\\0216_i_t_f_test.csv"


    train_data_path = "E:\\PYProject\\fresh_game\\output_data\\train_data_fea_0216_1.csv"
    verify_data_path = "E:\\PYProject\\fresh_game\\output_data\\verify_data_fea_0216_1.csv"
    test_data_path = "E:\\PYProject\\fresh_game\\output_data\\test_data_fea_0216_1.csv"
    item_data_path = "E:\\PYProject\\fresh_game\\input_data\\fresh_comp_offline\\tianchi_fresh_comp_train_item.csv"

    cf_train_path = "E:\\PYProject\\fresh_game\\input_data\\fea_0216\\0216_c_f_train.csv"
    cf_verify_path = "E:\\PYProject\\fresh_game\\input_data\\fea_0216\\0216_c_f_verify.csv"
    cf_test_path = "E:\\PYProject\\fresh_game\\input_data\\fea_0216\\0216_c_f_test.csv"

    uif_train_path = "E:\\PYProject\\fresh_game\\input_data\\fea_0216\\0216_ui_f_train.csv"
    uif_verify_path = "E:\\PYProject\\fresh_game\\input_data\\fea_0216\\0216_ui_f_verify.csv"
    uif_test_path = "E:\\PYProject\\fresh_game\\input_data\\fea_0216\\0216_ui_f_test.csv"


    uf_train_path="E:\\PYProject\\fresh_game\\input_data\\fea_0216\\0216_u_f_train.csv"
    uf_verify_path = "E:\\PYProject\\fresh_game\\input_data\\fea_0216\\0216_u_f_verify.csv"
    uf_test_path= "E:\\PYProject\\fresh_game\\input_data\\fea_0216\\0216_u_f_test.csv"


    if_train_path = "E:\\PYProject\\fresh_game\\input_data\\fea_0216\\0216_i_f_train.csv"
    if_verify_path = "E:\\PYProject\\fresh_game\\input_data\\fea_0216\\0216_i_f_verify.csv"
    if_test_path = "E:\\PYProject\\fresh_game\\input_data\\fea_0216\\0216_i_f_test.csv"


    train_data_save_path = "E:\\PYProject\\fresh_game\\output_data\\0216_2\\train_data_fea_0216_2.csv"
    verify_data_save_path = "E:\\PYProject\\fresh_game\\output_data\\0216_2\\verify_data_fea_0216_2.csv"
    test_data_save_path = "E:\\PYProject\\fresh_game\\output_data\\0216_2\\test_data_fea_0216_2.csv"



    ori_train_data = readCsv(train_data_path)
    ori_verify_data = readCsv(verify_data_path)
    ori_test_data = readCsv(test_data_path)

    uf_train = readCsv(uf_train_path,header=False).rename(columns={0:'user_id'})
    if_train = readCsv(if_train_path, header=False).rename(columns={0: 'item_id'})
    uif_train = readCsv(uif_train_path, header=False).rename(columns={0: 'user_id',1:'item_id'})
    cf_train = readCsv(cf_train_path,header=False).rename(columns={0: 'item_category'})

    uf_verify = readCsv(uf_verify_path, header=False).rename(columns={0: 'user_id'})
    if_verify  = readCsv(if_verify_path, header=False).rename(columns={0: 'item_id'})
    uif_verify = readCsv(uif_verify_path, header=False).rename(columns={0: 'user_id',1:'item_id'})
    cf_verify = readCsv(cf_verify_path,header=False).rename(columns={0: 'item_category'})

    uf_test = readCsv(uf_test_path, header=False).rename(columns={0: 'user_id'})
    if_test = readCsv(if_test_path, header=False).rename(columns={0: 'item_id'})
    uif_test = readCsv(uif_test_path, header=False).rename(columns={0: 'user_id',1:'item_id'})
    cf_test = readCsv(cf_test_path,header=False).rename(columns={0: 'item_category'})
    print uif_verify
    print uif_test

    train_data = merge_fea_data(ori_train_data,uf_train,if_train,uif_train,cf_train)
    verify_data = merge_fea_data(ori_verify_data, uf_verify, if_verify, uif_verify,cf_verify)
    test_data = merge_fea_data(ori_test_data, uf_test, if_test, uif_test,cf_test)

    print len(verify_data)
    print len(test_data)
    saveCsv(train_data,train_data_save_path)
    saveCsv(verify_data,verify_data_save_path)
    saveCsv(test_data,test_data_save_path)
    print 'down!'