import tags
import os.path
import pandas
import matplotlib.pyplot as plt
import numpy as np

folder='C:\Users\Ish\Desktop\Epic\MovDerivation\UserCoding\\'
cols=['Sent1','Prep1','Movement','Env1','CollOrientation']
Sent_tags=['angry','worried','defiant','coping','ready','bored', \
	'relieved','comedic','excited', 'happy']
Prep_tags=['food', 'other supplies','rationing','power4life','power4comm', \
	'transport','changing plans','booze']
Movement_tags=['@home', 'hunkering','evac ordered','leaves', \
	'arrives','returns home']
Env_tags=['personal', 'weather','assessment','social reporting']
CollOrientation_tags=['seek','pass on info','do what others do']
colors=['DarkRed','OrangeRed','Orange','Yellow','LimeGreen','Green','SeaGreen',\
'MediumBlue','DarkViolet','Indigo']
time=['Oct27','Oct28','Oct29','Oct30','Oct31', 'Nov1']

def switchTags(c):
	if c=='Sent1':
		res=Sent_tags
	elif c=='Prep1':
		res=Prep1_tags
	elif  c=='Movement':
		res=Movement_tags
	elif c=='Env':
		res=Env_tags
	elif c=='CollOrientation':
		res=CollOrientation_tags
	return res

num_users=52
for f in os.listdir(folder):
	df=pandas.DataFrame.from_csv(folder+f)
	user=f[:len(f)-19]
	tags.sepTags(df)
	tags.cleanTags(df)
	grouped=df.groupby([lambda x: x.day, lambda x: x.hour])
	count=0
	plt.figure()
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
		clipped=resdf[resdf.flatind>=120] #starting with Oct 27th
		#tags=c+'_tags'
		taglist=switchTags(col) #get the right taglist
		hues=colors[:len(taglist)]
		use_colors=dict(zip(taglist,hues))
		x=np.arange(120,len(res),24)
		plt.xticks(x,time)
		plt.yticks(xrange(len(cols)),cols)
		plt.scatter(clipped.flatind,len(clipped.flatind)*[count],\
		c=[use_colors[i] for i in clipped[col]], s=120)
		plt.xlim(xmin=120)
		plt.ylim(ymin=-0.5,ymax=4.5)
		plt.title(user)
		count+=1
	plt.savefig('C:\Users\Ish\Desktop\Epic\MovDerivation\Trajectories\\'+user+'.png')
	plt.close()
		

