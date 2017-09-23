data = pd.read_csv('./alitianchi/2017_不带缺失值.csv', index_col=0,dtype={"link_ID":str, "date":str, "time_interval":str})

data['travel_speed'] = data['length']/data['new_travel_time']
data['lane']=data['width']/3.0

###############
# 前两小时的特征
# 前几天前两小时的特征
for i in [3,6,9,21,42,84]: 
    name = 'travel_speed_mean_last_pre'+str(i)+'_2hour'
    travel_speed_mean_last_pre_2hour = data.query('map_hour in [2,5,8]')[['link_ID','doy','map_hour','travel_speed']].\
        groupby(['link_ID','doy','map_hour']).agg(np.mean).reset_index()
    travel_speed_mean_last_pre_2hour.sort_values(['link_ID', 'doy', 'map_hour'], inplace=True)
    travel_speed_mean_last_pre_2hour['travel_speed'] = pd.rolling_mean(travel_speed_mean_last_pre_2hour['travel_speed'],window=i,min_periods=1)
    travel_speed_mean_last_pre_2hour.columns = ['link_ID','doy','map_hour',name]
    travel_speed_mean_last_pre_2hour['map_hour'] = travel_speed_mean_last_pre_2hour['map_hour'] + 1
    data= data.merge(travel_speed_mean_last_pre_2hour, how='left',on=['link_ID', 'doy', 'map_hour'])
del travel_speed_mean_last_pre_2hour

# 同时段前几天前两小时的特征
for i in [1,2,3,7,14,28]:
    name = 'travel_speed_mean_last_day'+str(i)+'_2hour'
    travel_speed_mean_last_day_2hour = data.query('map_hour in [2,5,8]')[['link_ID','map_hour','doy','travel_speed']].\
        groupby(['link_ID','map_hour','doy']).agg(np.mean).reset_index()
    
    travel_speed_mean_last_day_2hour.sort_values(['link_ID','map_hour', 'doy'], inplace=True)
    for j in [2,5,8]:
        travel_speed_mean_last_day_2hour['travel_speed'][travel_speed_mean_last_day_2hour['map_hour'] == j]=\
            pd.rolling_mean(travel_speed_mean_last_day_2hour['travel_speed'][travel_speed_mean_last_day_2hour['map_hour'] == j],window=i,min_periods=1)
    
    travel_speed_mean_last_day_2hour.columns = ['link_ID','map_hour','doy',name]
    travel_speed_mean_last_day_2hour['map_hour'] = travel_speed_mean_last_day_2hour['map_hour'] + 1
    data = data.merge(travel_speed_mean_last_day_2hour, how='left',on=['link_ID', 'doy', 'map_hour'])
del travel_speed_mean_last_day_2hour

del data['map_hour']
data = data.query('hour in [7,8,14,15,17,18]')

###############
# 前一小时的特征
# 前几天前一小时的特征
for i in [3,6,9,21,42,84]:
    name = 'travel_speed_mean_last_pre'+str(i)+'_hour'
    travel_speed_mean_last_pre_hour = data.query('hour in [7,14,17]')[['link_ID','doy','hour','travel_speed']].\
        groupby(['link_ID','doy','hour']).agg(np.mean).reset_index()
    travel_speed_mean_last_pre_hour.sort_values(['link_ID', 'doy', 'hour'], inplace=True)
    travel_speed_mean_last_pre_hour['travel_speed'] = pd.rolling_mean(travel_speed_mean_last_pre_hour['travel_speed'],window=i,min_periods=1)
    travel_speed_mean_last_pre_hour.columns = ['link_ID','doy','hour',name]
    travel_speed_mean_last_pre_hour['hour'] = travel_speed_mean_last_pre_hour['hour'] + 1
    data = data.merge(travel_speed_mean_last_pre_hour, how='left',on=['link_ID', 'doy', 'hour'])
del travel_speed_mean_last_pre_hour

# 前几天同一时段前一小时的特征
for i in [1,2,3,7,14,28]:
    name = 'travel_speed_mean_last_day'+str(i)+'_hour'
    travel_speed_mean_last_day_hour = data.query('hour in [7,14,17]')[['link_ID','hour','doy','travel_speed']].\
        groupby(['link_ID','hour','doy']).agg(np.mean).reset_index()
    
    travel_speed_mean_last_day_hour.sort_values(['link_ID','hour', 'doy'], inplace=True)
    for j in [7,14,17]:
        travel_speed_mean_last_day_hour['travel_speed'][travel_speed_mean_last_day_hour['hour'] == j]=\
            pd.rolling_mean(travel_speed_mean_last_day_hour['travel_speed'][travel_speed_mean_last_day_hour['hour'] == j],window=i,min_periods=1)
    
    travel_speed_mean_last_day_hour.columns = ['link_ID','hour','doy',name]
    travel_speed_mean_last_day_hour['hour'] = travel_speed_mean_last_day_hour['hour'] + 1
    data = data.merge(travel_speed_mean_last_day_hour, how='left',on=['link_ID', 'doy', 'hour'])
del travel_speed_mean_last_day_hour
gc.collect()
data = data.query('hour in [8, 15, 18]')

###############
# 当前小时的各种特征
all_statistic = {'mean': True, 'median':True, 'q1':True, 'q3':True}
mean_median_statistic = {'mean': True, 'median':True, 'q1':False, 'q3':False}
mean_statistic= {'mean': True, 'median':False, 'q1':False, 'q3':False}
median_statistic= {'mean': False, 'median':True, 'q1':False, 'q3':False}
q1_statistic= {'mean': False, 'median':False, 'q1':True, 'q3':False}
q3_statistic= {'mean': False, 'median':False, 'q1':False, 'q3':True}

def group_statistic_speed_feature(data, group, mean=True, median=False, q1=False, q3=False):
    target='travel_speed'
    slice_ = group[:]
    slice_.append(target)
    result_name = '_'.join(group[1:])
    train_data = data.query('data_class == "train"')
    if mean:
        grp_mean = train_data[slice_].groupby(group).mean().reset_index()
        grp_mean.rename(columns={target:target+'_mean_'+result_name}, inplace=True)
        result = grp_mean
        print('got mean!')
    if median:
        grp_median = train_data[slice_].groupby(group).agg(np.median).reset_index()
        grp_median.rename(columns={target:target+'_median_'+result_name}, inplace=True)
        try:
            result = result.merge(grp_median, on=group)
        except:
            result = grp_median
        print('got median!')
    if q1:
        grp_q1 = train_data[slice_].groupby(group).quantile(0.25).reset_index()
        grp_q1.rename(columns={target:target+'_q1_'+result_name}, inplace=True)
        try:
            result = result.merge(grp_q1, on=group)
        except:
            result = grp_q1
        print('got q1!')
    if q3:
        grp_q3 = train_data[slice_].groupby(group).quantile(0.75).reset_index()
        grp_q3.rename(columns={target:target+'_q3_'+result_name}, inplace=True)
        try:
            result = result.merge(grp_q3, on=group)
        except:
            result = grp_q3
        print('got q3!')
    print('start merge!')
    data = data.merge(result, how = 'left',on=group)
    print('group statistic '+result_name+' finished!')
    return data

groups = [['link_ID','dow','hour','minute'],
          ['link_ID','dow','hour','minute_4'], 
          ['link_ID','dow','hour','minute_6'],
          ['link_ID','dow','hour','minute_10'],
          ['link_ID','dow','hour','minute_20'],
          ['link_ID','dow','hour','minute_30'],
          ['link_ID','dow','hour'], 
          ['link_ID','season','dow','hour'],
          
          ['link_ID','dom_7','dow','hour','minute'], 
          ['link_ID','dom_7','dow','hour','minute_4'], 
          ['link_ID','dom_7','dow','hour','minute_6'],  
          ['link_ID','dom_7','dow','hour','minute_10'],  
          ['link_ID','dom_7','dow','hour','minute_20'], 
          ['link_ID','dom_7','dow','hour','minute_30'],
          ['link_ID','dom_7','dow','hour'],
          
          ['link_ID','dom_15','dow','hour','minute'],  
          ['link_ID','dom_15','dow','hour','minute_4'], 
          ['link_ID','dom_15','dow','hour','minute_6'],  
          ['link_ID','dom_15','dow','hour','minute_10'],  
          ['link_ID','dom_15','dow','hour','minute_20'], 
          ['link_ID','dom_15','dow','hour','minute_30'], 
          ['link_ID','dom_15','dow','hour']
          
        ]

for g in groups:
    data = group_statistic_speed_feature(data, group=g, **all_statistic) 

data[features]= data[features].fillna(method='ffill', axis=1)
data[features]= data[features].fillna(method='backfill')

# 将速度特征转换成time和volume的内容
for feat in data.columns:
    if 'travel_speed_' in feat:
            data[feat.replace('speed','volume')]=data[feat]*data['lane']
            data[feat.replace('speed','time')]=data['length']/data[feat