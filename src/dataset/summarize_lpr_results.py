import numpy as np
import pandas as pd
import shutil

data=pd.read_csv('log/dataset/ocr_results.csv',skiprows=1,names=['file',
    'oocr',
    'eh','ehocr','eht','ehtocr',
    'ch','chocr','cht','chtocr',
    'bf','bfocr','bft','bftocr',
    'res1','res2','res3','res4','res5','res6','res7'])

print('\n')
print('oocr mean:%f std:%f 90th:%f'%(np.mean(data['oocr']),np.std(data['oocr']),np.percentile(np.sort(data['oocr']),90)))

print('\n')
print('eh mean:%f std:%f 90th:%f'%(np.mean(data['eh']),np.std(data['eh']),np.percentile(np.sort(data['eh']),90)))
print('ehocr mean:%f std:%f 90th:%f'%(np.mean(data['ehocr']),np.std(data['ehocr']),np.percentile(np.sort(data['ehocr']),90)))
print('eht mean:%f std:%f 90th:%f'%(np.mean(data['eht']),np.std(data['eht']),np.percentile(np.sort(data['eht']),90)))
print('ehtocr mean:%f std:%f 90th:%f'%(np.mean(data['ehtocr']),np.std(data['ehtocr']),np.percentile(np.sort(data['ehtocr']),90)))

print('\n')
print('ch mean:%f std:%f 90th:%f'%(np.mean(data['ch']),np.std(data['ch']),np.percentile(np.sort(data['ch']),90)))
print('chocr mean:%f std:%f 90th:%f'%(np.mean(data['chocr']),np.std(data['chocr']),np.percentile(np.sort(data['chtocr']),90)))
print('cht mean:%f std:%f 90th:%f'%(np.mean(data['cht']),np.std(data['cht']),np.percentile(np.sort(data['cht']),90)))
print('chtocr mean:%f std:%f 90th:%f'%(np.mean(data['chtocr']),np.std(data['chtocr']),np.percentile(np.sort(data['chtocr']),90)))

print('\n')
print('bf mean:%f std:%f 90th:%f'%(np.mean(data['bf']),np.std(data['bf']),np.percentile(np.sort(data['bf']),90)))
print('bfocr mean:%f std:%f 90th:%f'%(np.mean(data['bfocr']),np.std(data['bfocr']),np.percentile(np.sort(data['bfocr']),90)))
print('bft mean:%f std:%f 90th:%f'%(np.mean(data['bft']),np.std(data['bft']),np.percentile(np.sort(data['bft']),90)))
print('bftocr mean:%f std:%f 90th:%f'%(np.mean(data['bftocr']),np.std(data['bftocr']),np.percentile(np.sort(data['bftocr']),90)))

print('\n')

oocr_mean=np.mean(data['oocr'])

ehocr_mean=np.mean(data['ehocr'])

ehtocr_mean=np.mean(data['ehtocr'])

chocr_mean=np.mean(data['chocr'])

chtocr_mean=np.mean(data['chtocr'])

bfocr_mean=np.mean(data['bfocr'])

bftocr_mean=np.mean(data['bftocr'])

r=50
count=0

print('Selected test files:')
for idx,row in data.iterrows():
  if (oocr_mean-r<=row['oocr']<=oocr_mean+r) and \
      (ehocr_mean-r<=row['ehocr']<=ehocr_mean+r) and \
      (chocr_mean-r<=row['chocr']<=chocr_mean+r) and \
      (bfocr_mean-r<=row['bfocr']<=bfocr_mean+r):
    print(row['file'])
    shutil.copyfile('ocr_plates/%s'%(row['file']),'ocr_plates/selected_plates/%s'%(row['file']))
    count+=1
print('Total selected test files:%d'%(count))
