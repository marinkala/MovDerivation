import numpy as np

grouped=df.Prep1.groupby([lambda x: x.day, lambda x: x.hour])
res=grouped.agg(lambda x: x.value_counts().index[1] if len(x.value_counts())>1 \
else 'None')
resdf=pandas.DataFrame(res)

def getNums(tags):
   if tags=='food':
       res=0
   elif tags=='other supplies':
       res=1
   elif tags=='power4life':
       res=2
   elif tags=='power4comm':
       res=3
   elif tags=='changing plans':
       res=4
   elif tags=='booze':
       res=5
   else:
       res=-1
   return res

resdf['numTags']=resdf[0].apply(getNums)
resdf['flatind']=range(len(res))
nogap=resdf[resdf.numTags!=(-1)] #exclude gaps
clipped=nogap[nogap.flatind>=120]

tags=['food','supplies','power for life', 'power for comm',\
'changing plans','alchohol']

y=range(len(tags)) #for this data!!!!!
y=range(len(tags))
time=['Oct27','Oct28','Oct29','Oct30','Oct31', 'Nov1']
fig=plt.figure()
fig.subplots_adjust(left=0.2)
x=np.arange(120,len(res),24)
plt.xticks(x,time)
plt.yticks(y,tags)
plt.plot(clipped.flatind,clipped.numTags,'o-')
plt.xlim(xmin=162,xmax=len(res)+2)
plt.ylim(ymin=-0.15,ymax=len(tags)-1+0.15)
plt.show()