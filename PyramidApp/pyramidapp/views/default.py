from pyramid.response import Response
from pyramid.view import view_config
from pyramid.renderers import render_to_response
from sqlalchemy.exc import DBAPIError

from ..models import MyModel

import re

from urllib.request import urlretrieve
from zipfile import ZipFile
from itertools import chain

import pandas as pd
import numpy as np
import seaborn as sb

import bokeh as bk
from bokeh.models import ColumnDataSource, HoverTool, CategoricalColorMapper, Slider, LinearInterpolator
from bokeh.io import curdoc, show, output_notebook, push_notebook, output_file
from bokeh.layouts import widgetbox, column, row, gridplot
from bokeh.plotting import figure
import matplotlib.pyplot as plt

output_notebook()


@view_config(route_name="first", renderer='../templates/first.jinja2')


@view_config(route_name='home', renderer='../templates/mytemplate.jinja2')
def my_view(request):
    try:
        query = request.dbsession.query(MyModel)
        one = query.filter(MyModel.name == 'one').first()
    except DBAPIError:
        return Response(db_err_msg, content_type='text/plain', status=500)
    return {'one': one, 'project': 'PyramidApp'}


@view_config(route_name="second", renderer='../templates/second.jinja2')
def second(request):
    image = request.POST['my_uploaded_file'].filename
    plt.style.use('seaborn-muted')
    file_address = 'https://archive.ics.uci.edu/ml/machine-learning-databases/00395/PARKINSON_HW.zip'
    zip_retrieved = urlretrieve(file_address,'parkinsons.zip')
    zip_retrieved
    zip_get = ZipFile(zip_retrieved[0],'r')
    zip_get
    list_of_files = ZipFile.extractall(zip_get)
    print(list_of_files)
    zip_get.namelist()[:10]
    pattern = re.compile('.+\/.+[CPH]+.+\.txt$')
    list_of_texts = sorted(list(set(chain.from_iterable([re.findall(pattern,i) for i in zip_get.namelist()]))))
    list_of_texts[:10]
    control_pattern = r'.*\/control\/.*\.txt$'
    park_pattern =r'.*\/parkinson\/.*\.txt$'
    control_files = sorted(list(chain.from_iterable([re.findall(control_pattern,i) for i in list_of_texts])))
    park_files = sorted(list(chain.from_iterable([re.findall(park_pattern,i) for i in list_of_texts])))
    control_files
    park_files[-10:]
    column_names = ['X' , 'Y', 'Z', 'Pressure', 'GripAngle', 'Timestamp', 'Test ID']
    df = pd.read_csv(control_files[0],';',names=column_names)
    df.head()
    df_2 = pd.read_csv(control_files[1],';',names=column_names)
    df_2.head()
    df_2['ZeroedTimeStamp'] = df_2['Timestamp'] - df_2['Timestamp'].min()
    df_2.head()
    df_2.set_index('ZeroedTimeStamp',inplace=True)
    ax = df_2[df_2['Test ID'] == 0].plot(x='X',y='Y',color='blue',alpha=0.5)
    df_2[df_2['Test ID'] == 1].plot(x='X',y='Y',ax=ax,color='orange',alpha=0.5)
    plt.xlim([0,450])
    plt.legend(['Static','Dynamic'])
    plt.show()
    df_2[df_2['Test ID'] == 1].head()
    ax = df_2[df_2['Test ID'] == 0].Pressure.plot(color='blue')
    df_2[df_2['Test ID'] == 1].Pressure.plot(color='orange')
    plt.show()
    ax = df_2[df_2['Test ID'] == 0].GripAngle.plot(color='blue')
    df_2[df_2['Test ID'] == 1].GripAngle.plot(color='orange')
    plt.show()
    df_2['Test ID'] = df_2['Test ID'].astype('str')
    size_map = LinearInterpolator(
        x = [600, df_2['Pressure'].max()],
        y = [2,15]
    )
    source = ColumnDataSource(df_2)
    colormap = CategoricalColorMapper(factors=['0','1'],palette=['blue','orange'])
    fig = figure(title='Control Tablet Results: Static vs. Dynamic Test')
    fig.circle('X','Y',source=source,color={'field':'Test ID','transform':colormap},size={'field':'Pressure','transform':size_map},alpha=.05)
    #fig.legend(['Dynamic vs. Static'])
    fig.title.text_color='olive'
    show(fig)
    df.head()
    df_static = df[df['Test ID'] == 0]
    df_dynamic = df[df['Test ID'] == 1]
    df_static['ZeroedTimestamp'] = df_static['Timestamp'] - df_static['Timestamp'].min()
    df_dynamic['ZeroedTimestamp'] = df_dynamic['Timestamp'] - df_dynamic['Timestamp'].min()
    df_combined = df_static.merge(df_dynamic,how='inner',suffixes=['_S','_D'],left_on='ZeroedTimestamp',right_on='ZeroedTimestamp')
    df_combined.head()
    ax = df_combined.plot('X_S','Y_S',figsize=(14,10))
    df_combined.plot('X_D','Y_D',ax=ax)
    plt.xlim([0,450])
    plt.legend(['Static','Dynamic'],fontsize=14)
    plt.annotate('Dynamic Test slows the test taker by about {:.2%}'.format(1-len(df_static)/len(df_dynamic)),xy=[80,310],xytext=[110,340],arrowprops={'facecolor':'orange','arrowstyle':'fancy'},fontsize=14)
    plt.title('Dynamic vs. Static Test in Same Span of Time',fontsize=16)
    plt.show()
    df_combined_with_zero = df_static.merge(df_dynamic,how='inner',suffixes=['_S','_D'],left_on='ZeroedTimestamp',right_on='ZeroedTimestamp')
    df_combined_with_zero.fillna(0,inplace=True)
    ax = df_combined_with_zero['Pressure_S'].plot(color='#41f4e2',alpha=0.5,figsize=(10,8),label='Static')
    df_combined_with_zero['Pressure_D'].plot(ax=ax,color='#f49b42',alpha=0.5,label='Dynamic')
    plt.ylim([500,1000])
    plt.title('Static vs. Dynamic Pressure Applied During Spiral Drawing')
    plt.legend()
    plt.show()
    x = np.arange(0,1.001,.001)
    y = 3*-2*np.pi*x
    figg = plt.figure(figsize=(10,8))
    ax = figg.add_subplot(111,polar=True)
    ax.plot(y,x)
    plt.show()
    x_array = df_combined.iloc[:,0].values

    x_rate = np.zeros_like(x_array)

    for i in range(len(x_array)):
        if i == 0:
            x_rate[i] = 1
        else:
            x_rate[i] = abs(x_array[i] - x_array[i-1])
    y_array = df_combined.iloc[:,1].values

    y_rate = np.zeros_like(y_array)

    for i in range(len(y_array)):
        if i == 0:
            y_rate[i] = 1
        else:
            y_rate[i] = abs(y_array[i] - y_array[i-1])
    x_array = x_array - 200
    plt.figure(figsize=(8,6))
    plt.plot(x_array,linestyle='none',marker='.')
    plt.vlines([0,20,135,320,580,860,1225,1530],-200,200,linestyles='-.',colors='#42dcf4')
    plt.show()
    x = np.arange(len(x_array))

    freq = 3/len(x_array)
    x_wave = x/(len(x)/200)*(np.sin((1.5*np.pi*x*freq)))
    plt.figure(figsize=(12,10))
    plt.plot(x_array)

    plt.plot(x_wave)
    plt.show()
    df_rate = pd.DataFrame(x_rate,columns=['x'])
    df_rate = df_rate.join(pd.DataFrame(y_rate,columns=['y']))
    df_rate.rolling(100).mean().plot(figsize=[12,10])
    plt.show()
    df_park = pd.read_csv(park_files[0],';',names=column_names)
    df_park['ZeroedTimeStamp'] = df_park['Timestamp'] - df_park['Timestamp'].min()
    df_park_XY = df_park.loc[:,['X','Y','ZeroedTimeStamp']].set_index('ZeroedTimeStamp')
    df_park_XY.pct_change(25).plot(kind='hist',bins=20)
    plt.title('Parkinsons Steadiness')
    plt.show()
    df_2_XY = df_2.iloc[:,[0,1]]
    df_2_XY.pct_change(25).plot(kind='hist',bins=20)
    plt.title('Control Steadiness')
    plt.show()
    df_park['X_lag_avg'] = df_park['X'].diff(1).rolling(100).mean()
    df_2['X_lag_avg'] = df_2['X'].diff(1).rolling(100).mean()
    ax = df_park.dropna()['X_lag_avg'].plot(kind='hist',label='Parkinsons',figsize=(10,8))
    df_2.dropna()['X_lag_avg'].plot(kind='hist',alpha=0.5,label='Control',ax=ax)
    #plt.xlim([0,2500])
    plt.suptitle('Variability in X Coordinate Change Rate',fontsize=14)
    plt.title('Measured by Rolling Mean Difference in X Coordinate')
    plt.legend(loc=0)
    plt.show()
    np.mean(df_park['X_lag_avg'])
    np.mean(df_2['X_lag_avg'])
    np.std(df_park['X_lag_avg'])
    np.std(df_2['X_lag_avg'])
    control_dfs = [pd.read_csv(control_files[i],';',names=column_names) for i,v in enumerate(control_files)]
    control_dfs
    control_combined_df = pd.DataFrame()

    for i, c_df in enumerate(control_dfs):

        for x in list(c_df['Test ID'].unique()):
            new_df = c_df[c_df['Test ID'] == x]
            new_df['Subject'] = i
            new_df['ZeroedTimestamp'] = new_df['Timestamp'] - new_df['Timestamp'].min()
            new_df['X_diff'] = new_df['X'].diff(1).rolling(100).mean().abs()
            new_df['Y_diff'] = new_df['Y'].diff(1).rolling(100).mean().abs()
            control_combined_df = control_combined_df.append(new_df,ignore_index=True)
    len(control_combined_df)
    control_group = control_combined_df.groupby(['Subject','Test ID']).mean()
    control_group.reset_index(inplace=True)
    control_group[control_group['Test ID'] != 2]['X_diff'].plot()
    plt.show()
    control_group.set_index('ZeroedTimestamp',inplace=True)
    control_group['X_diff'].plot(kind='hist',figsize=(13,11),bins=25)
    plt.show()
    from park_tools import data_prep
    control_files = data_prep.retrieve_uci_data()
    control_files
    park_files = data_prep.retrieve_uci_data(group='parkinson')
    park_files[:5]
    park_dfs = data_prep.make_combined_df(park_files)
    park_dfs_sub_61 = park_dfs[park_dfs['Subject'] == 61]
    park_dfs_sub_61.head()
    park_dfs_sub_61['Pressure_diff'] = park_dfs_sub_61['Pressure'].diff(1).rolling(100).mean()
    park_dfs_sub_61['Grip_diff'] = park_dfs_sub_61['GripAngle'].diff(1).rolling(100).mean()
    park_dfs_sub_61 = park_dfs_sub_61.dropna()
    park_dfs_sub_61.plot(x='Pressure_diff',y='Y_diff',marker='*',linestyle='none',figsize=(12,10))
    plt.xlim(min(park_dfs_sub_61['Pressure_diff']),max(park_dfs_sub_61['Pressure_diff']))
    plt.show()
    park_dfs_sub_61['Grip_diff'].hist(bins=20)
    park_dfs_sub_61['Pressure_diff'].hist(bins=20,alpha=0.3)
    plt.show()
    park_dfs_sub_61['Test ID'] = park_dfs_sub_61['Test ID'].astype('object')
    park_dfs_sub_61['Subject'] = park_dfs_sub_61['Subject'].astype('object')

    park_dfs_sub_61.dtypes
    normed = data_prep.normalize_df(park_dfs_sub_61)
    normed.head()
    normed[['X_diff_avg_100','Y_diff_avg_100']].plot(kind='hist',alpha=.4,figsize=(6,5),color=['orange','blue'])
    plt.xlim([-3,3])
    plt.title('X and Y average Speed over rolling 100-frame window')
    plt.show()
    normed[['X_diff','Y_diff']].plot(kind='hist',alpha=.4,figsize=(6,5),color=['orange','blue'])
    plt.xlim([-3,3])
    plt.show()
    normed_control = data_prep.make_combined_df(control_files).dropna()
    normed_control['Test ID'] = normed_control['Test ID'].astype('object')
    normed_control['Subject'] = normed_control['Subject'].astype('object')
    normed_control.head()
    normed_control_last = normed_control[normed_control['Subject'] == normed_control['Subject'].max()]
    normed_control_last = data_prep.normalize_df(normed_control_last)
    normed_control_last.head()
    ax = normed_control_last[['X_diff_avg_100','Y_diff_avg_100']].plot(kind='hist',alpha=.4,color='orange',label='Control Subject 14',figsize=(14,12))
    park_dfs_sub_61[['X_diff_avg_100','Y_diff_avg_100']].plot(kind='hist',alpha=.4,figsize=(6,5),color='#42f48f',ax=ax,label='Parkinson\'s Subject 61')
    plt.xlim([-5,5])
    plt.xlabel('Average speed variance across 100 periods')
    plt.title('Control vs. Parkinson\'s Distribution of velocity shifts')
    plt.legend()
    plt.show()
    fig, ax = plt.subplots(nrows=1,ncols=2,sharex=True,sharey=True,figsize=(14,6))
    ax[0].hist(normed_control_last[['X_diff_avg_100','Y_diff_avg_100']].values,bins=10,color=['orange','orange'],label='Control')
    ax[0].set_title('Control')
    ax[1].hist(park_dfs_sub_61[['X_diff_avg_100','Y_diff_avg_100']].values,bins=10,color=['blue','blue'],label='Parkinson\'s')
    ax[1].set_title('Parkinson\'s')
    plt.legend()
    fig.suptitle('Control vs. Parkinson\'s variation in Velocity',size=16)
    plt.show()
    ax = normed_control_last['X_diff_avg_100'].plot(figsize=(12,10))
    #park_dfs_sub_61['X_diff_avg_100'].plot(ax=ax)
    plt.show()
    norm_control_X_x, norm_control_X_y = ecdf(normed_control_last['X_diff_avg_100'])
    norm_control_Y_x, norm_control_Y_y = ecdf(normed_control_last['Y_diff_avg_100'])
    norm_park_X_x, norm_park_X_y = ecdf(park_dfs_sub_61['X_diff_avg_100'])
    norm_park_Y_x, norm_park_Y_y = ecdf(park_dfs_sub_61['Y_diff_avg_100'])
    plt.figure(figsize=(15,12))

    ax = plt.plot(norm_control_X_x, norm_control_X_y,marker='.',linestyle='none',label='Control X')
    plt.plot(norm_control_Y_x, norm_control_Y_y,marker='*',linestyle='none',label='Control Y')
    ax = plt.plot(norm_park_X_x, norm_park_X_y,marker='.',linestyle='none',label='Park X')
    plt.plot(norm_park_Y_x, norm_park_Y_y,marker='*',linestyle='none',label='Park Y')
    plt.legend()
    plt.show()
    return render_to_response ('../templates/second.jinja2',{},request=request)




db_err_msg = """\
Pyramid is having a problem using your SQL database.  The problem
might be caused by one of the following things:

1.  You may need to run the "initialize_PyramidApp_db" script
    to initialize your database tables.  Check your virtual
    environment's "bin" directory for this script and try to run it.

2.  Your database server may not be running.  Check that the
    database server referred to by the "sqlalchemy.url" setting in
    your "development.ini" file is running.

After you fix the problem, please restart the Pyramid application to
try it again.
"""
