time=['Oct27','Oct28','Oct29','Oct30','Oct31', 'Nov1']
x=np.arange(120,len(res),24)
plt.xticks(x,time)
use_colors={0:'red',1:'orange',2:'yellow',3:'green',4:'cyan',\
5:'blue',6:'magenta',7:'black'}
plt.scatter(clipped.flatind,len(clipped.flatind)*[1],\
c=[use_colors[i] for i in clipped.numTags], s=120)
ax=plt.gca()
ax.yaxis.set_visible(False)
plt.show()