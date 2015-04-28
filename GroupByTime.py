import numpy as np
import pandas

grouped=df.Sent1.groupby([lambda x: x.day, lambda x: x.hour])
res=grouped.agg(lambda x: x.value_counts().index[1] if len(x.value_counts())>1 \
else 'None')
resdf=pandas.DataFrame(res)

def getNums(tags):
    if tags=='angry':
        res=0
    elif tags=='worried':
        res=1
    elif tags=='ready':
        res=2
    elif tags=='bored':
        res=3
    elif tags=='relieved':
        res=4
    elif tags=='comedic':
        res=5
    elif tags=='excited':
        res=6
    elif tags=='happy':
        res=7
    else:
        res=-1
    return res # doesn't have defiant and coping

resdf['numTags']=resdf[0].apply(getNums)
resdf['flatind']=range(len(res))
nogap=resdf[resdf.numTags!=(-1)] #exclude gaps
clipped=nogap[nogap.flatind>=120]

tags=['angry','worried','ready','bored', \
	'relieved','comedic','excited', 'happy'] #for this data!!!!!
y=range(len(tags))
plt.yticks(y,tags)
time=['Oct27','Oct28','Oct29','Oct30','Oct31', 'Nov1']
x=np.arange(120,len(res),24)
plt.xticks(x,time)
plt.plot(clipped.flatind,clipped.numTags)
plt.xlim(xmin=120,xmax=250)
plt.show()