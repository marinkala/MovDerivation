import tags
import os.path
import pandas
import math
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import numpy as np
from datetime import timedelta

folder='C:\Users\Ish\Desktop\Epic\MovDerivation\NJUserCoding\\'
cols=['Sent1','Prep1','Env1','Movement','CollOr1']
Sent_tags=['angry','worried','defiant','coping','ready','bored', \
	'relieved','comedic','excited', 'happy']
Prep_tags=['food', 'physical','other supplies','rationing','power4life','power4comm', \
	'changing existing plans','booze'] #+ transport
Movement_tags=['@home', 'hunkering','evac ordered','leaves', \
	'arrives','returns home']
Env_tags=['personal', 'weather','assessment','social reporting']
CollOrientation_tags=['seeking','pass on','doing what others are doing']
SentColors=['DarkRed','OrangeRed','Orange','Yellow','LimeGreen','Green','SeaGreen',\
'MediumBlue','DarkViolet','Indigo']
PrepColors=['#00441b','#006d2c','#238b45','#41ae76','#66c2a4','#99d8c9',\
	'#f7fcfd','#e5f5f9']
MovColors=['#4a1486','#6a51a3','#807dba','#9e9ac8','#bcbddc','#dadaeb']
EnvColors=['#bd0026','#f03b20','#fd8d3c','#fecc5c']
CollColors=['#ae017e','#f768a1','#fbb4b9']
SentMark='o'
PrepMark='^'
MovMark='p'
EnvMark='s'
CollMark='*'
time=['Oct28','Oct29','Oct30','Oct31', 'Nov1','Nov2']
start=144 #144 hours from Oct 22 - Oct 28th
end=264 #120 hours (5 days) from start

def setUserOrder():
	users={}
	for f in os.listdir(folder):
		username=f[:len(f)-4]
		df=pandas.DataFrame.from_csv(folder+f)
		grouped=df.groupby([lambda x: x.month, lambda x: x.day, lambda x: x.hour])
		all_tags=0
		for col in df.columns:
			res=grouped[col].agg(lambda x: 1 if len(x.dropna())>0 else 0)
			all_tags+=sum(res)
		users[username]=all_tags
	sorted_users=sorted(users, key=users.get) #returns a sorted list of users
	return sorted_users

def switchAttr(c):
	if c=='Sent1':
		tags=Sent_tags
		colRange=SentColors
		mark=SentMark
	elif c=='Prep1':
		tags=Prep_tags
		colRange=PrepColors
		mark=PrepMark
	elif  c=='Movement':
		tags=Movement_tags
		colRange=MovColors
		mark=MovMark
	elif c=='Env1':
		tags=Env_tags
		colRange=EnvColors
		mark=EnvMark
	elif c=='CollOr1':
		tags=CollOrientation_tags
		colRange=CollColors
		mark=CollMark
	return tags,colRange,mark
	
#users=setUserOrder()
#pandas.Series(users).to_csv('SortedUsers.csv')
users=pandas.Series.from_csv('SortedUsers.csv')
num_users=len(users)

# Create figure object
fig = plt.figure(figsize=(17, num_users*0.55))
ax = fig.add_axes([0.10, 0.02, 0.80, 0.95])
ax.set_ylim(-1,num_users)
ax.set_xlim(start,end)

# y-axis tick marks, one per username
yticks = np.arange(0, num_users, 1)
ax.set_yticks(yticks)
ax.set_yticklabels(users)

#x-axis tick marks, one per day, starting at midnight
xticks=np.arange(start,end,24)
ax.set_xticks(xticks)
ax.set_xticklabels(time)

ax.tick_params(labeltop=True,labelright=True)
ax.grid()
#which='major',axis='both',color='k', linestyle='.', linewidth=0.2, alpha=0.6)

or_circl = mlines.Line2D([], [], linestyle='none',c='OrangeRed', marker='o',markersize=10)
y_circl = mlines.Line2D([], [], linestyle='none',c='Yellow', marker='o',markersize=10)
g_circl = mlines.Line2D([], [], linestyle='none',c='Green', marker='o',markersize=10)
b_circl = mlines.Line2D([], [], linestyle='none',c='MediumBlue', marker='o',markersize=10)
tri1 = mlines.Line2D([], [], linestyle='none',marker='^', c='#00441b',markersize=10)
tri4 = mlines.Line2D([], [], linestyle='none',marker='^', c='#41ae76',markersize=10)
tri5 = mlines.Line2D([], [], linestyle='none',marker='^', c='#66c2a4',markersize=10)
tri8 = mlines.Line2D([], [], linestyle='none',marker='^', c='#e5f5f9',markersize=10)
sq1=mlines.Line2D([], [], linestyle='none',marker='s', c='#bd0026',markersize=10)
sq2=mlines.Line2D([], [], linestyle='none',marker='s', c='#f03b20',markersize=10)
sq3=mlines.Line2D([], [], linestyle='none',marker='s', c='#fd8d3c',markersize=10)
sq4=mlines.Line2D([], [], linestyle='none',marker='s', c='#fecc5c',markersize=10)
pen1=mlines.Line2D([], [], linestyle='none',marker='p', c='#4a1486',markersize=10)
pen4=mlines.Line2D([], [], linestyle='none',marker='p', c='#9e9ac8',markersize=10)
pen6=mlines.Line2D([], [], linestyle='none',marker='p', c='#dadaeb',markersize=10)
star1=mlines.Line2D([], [], linestyle='none',marker='*', c='#ae017e',markersize=12)
star2=mlines.Line2D([], [], linestyle='none',marker='*', c='#f768a1',markersize=12)
star3=mlines.Line2D([], [], linestyle='none',marker='*', c='#fbb4b9',markersize=12)

fig.legend([or_circl, y_circl,g_circl, b_circl,tri1,tri4,tri5,tri8,\
sq1,sq2,sq3,sq4,pen1,pen4,pen6,star1,star2,star3],\
['Worried','Coping','Bored','Comedic','Food','Power4life',\
'Power4comm', 'Booze','Personal Env', 'Weather','Env assessment',\
'Social reporting','@home', 'Leaves', 'Returns home', 'Seeking info',\
'Pass on info','Do what others do'])

loopCount=0
for u in users:
	df=pandas.DataFrame.from_csv(folder+u+'.csv')
	user=u
	df.index=df.index-timedelta(hours=6)
	tags.sepTags(df)
	tags.cleanTagsSimple(df)
	grouped=df.groupby([lambda x: x.month, lambda x: x.day, lambda x: x.hour])
	count=0
	#plt.yticks(xrange(len(cols*num_users)),cols*num_users)
	for col in cols:
		res=grouped[col].agg(lambda x: x.value_counts().index[1] \
		if len(x.value_counts())>1 else 'None')
		resdf=pandas.DataFrame(res)
		resdf['flatind']=range(len(res))
		resdf=resdf.dropna()
		nan_inds=resdf.index[(resdf[col]=='None')|\
		(resdf[col]=='nan')|(resdf[col]=='')]
		resdf=resdf.drop(nan_inds)
		clipped=resdf[resdf.flatind>=start] #starting with Oct 27th
		#tags=c+'_tags'
		taglist, hues, marks=switchAttr(col) #get the right taglist
		use_colors=dict(zip(taglist,hues))
		#plt.yticks(xrange(len(cols)),cols)
		sign=(-1)**count
		step=math.floor((count+1)/2.0)
		plt.scatter(clipped.flatind,len(clipped.flatind)*[loopCount+sign*step*0.2],\
		c=[use_colors[i] for i in clipped[col]], s=170, marker=marks)
		count+=1
	loopCount+=1
	#if loopCount>4:
		#break
fig.savefig('C:\Users\Ish\Desktop\Epic\MovDerivation\NJTrajectorySorted.png')
