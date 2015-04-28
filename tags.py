import os.path
import math
import pandas
from datetime import timedelta

def splitter(x): return str(x).split(',')
def clean(x): return x.lstrip().rstrip()
def split1(x): return clean(splitter(x)[0])

def split2(x): 
	taglist=splitter(x)
	if len(taglist)>1:
		return clean(taglist[1])
		
def split3(x): 
	taglist=splitter(x)
	if len(taglist)>2:
		 return clean(taglist[2])

def combine(folder):
	folder='C:\Users\Ish\Desktop\Epic\MovDerivation\\'+folder+'\\'
	dfc=pandas.DataFrame()
	for f in os.listdir(folder):
		df=pandas.DataFrame.from_csv(folder+f)
		df['user']=f[:len(f)-4]#strip file name of 'norm_distances'
		df.index=df.index-timedelta(hours=6)
		dfc=dfc.append(df)
	return dfc
	
def sepTags(df):
	df['Sent1']=df.Sentiment.apply(split1)
	df['Sent2']=df.Sentiment.apply(split2)
	df['Sent3']=df.Sentiment.apply(split3)
	df['Prep1']=df.Preparation.apply(split1)
	df['Prep2']=df.Preparation.apply(split2)
	df['Mov1']=df.Movement.apply(split1)
	df['Mov2']=df.Movement.apply(split2)
	df['Env1']=df.Environment.apply(split1)
	df['Env2']=df.Environment.apply(split2)
	df['CollOr1']=df['Collective Information'].apply(split1)
	df['CollOr2']=df['Collective Information'].apply(split2)

def cleanTagsSimple(df):
	df.Sent1[df.Sent1=='sarcastic']='comedic'
	
def cleanTags(df):
	df.Sent1[df.Sent1=='woried']='worried'
	df.Sent1[df.Sent1=='sarcastic']='comedic'
	df.Sent2[df.Sent2=='comedy']='comedic'
	df.Sent1[df.Sent1=='defiant?']='defiant'
	df.Prep1[(df.Prep1=='change existing plans')|\
	(df.Prep1=='changing existing plans')]='changing plans'
	df.Sent1[df.Prep1=='worried']='worried'
	df.Prep1[df.Prep1=='worried']=''
	df.Prep1[df.Prep1=='hunkering']=''
	try:
		df.Movement[df.Prep1=='hunkering']='hunkering'
		df.Movement[df.Movement=='home']='@home'
		df.Movement[df.Movement=='leaving']='leaves'
		df.Movement[df.Movement=='return home']='returns home'
		df.Movement[df.Movement=='ordered']='evac ordered'
		df.Movement[df.Movement=='leaving']='leaves' 
	except ValueError:
		print 'no movement'
	df.Env1[(df.Env1=='phsyical')|(df.Env1=='physical')]='personal'
	df.Env1[(df.Env1=='others')|(df.Env1=='social')]='social reporting'
	df['CollOrientation']=df['Collective Information']
	del df['Collective Information']
	try:
		df.CollOrientation[(df.CollOrientation=='pass on')|\
		(df.CollOrientation=='pass on information')|(df.CollOrientation=='pass on inormation')\
		|(df.CollOrientation=='passing')|(df.CollOrientation=='passing info')\
		|(df.CollOrientation=='pass on information,pass on')]='pass on info'
		df.CollOrientation[df.CollOrientation=='seeking']='seek'
		df.CollOrientation[(df.CollOrientation=='others')|\
		(df.CollOrientation=='sheeping')]='do what others do'
		df.CollOrientation[df.CollOrientation=='seeking']='seek'
	except TypeError:
		print 'no collective orientation'
