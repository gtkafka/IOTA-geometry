import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.patches as patches
import numpy as np
from math import sin  as S, cos as C, pi, sqrt
import time

def write_to_file(x, y,filename):
    fileobj= open(filename,'a')
    print >> fileobj, 'x', ' ', 'z'
    for key, value in zip(x,y):
        print >> fileobj, key,value
    fileobj.close()


def readfile(dataset,center=0):
    #Basic read file routine

    x,y,theta,xt,yt=[],[],[],[],[]

    with open(dataset) as f:
        data = f.read()
    data=data.split('\n')

    for row in data:
        if row.startswith('@') or row.startswith('*') \
            or row.startswith('$'):continue
        else:
            w=" ".join(row.split())
            s=w.split()
            wlen=len(s)
            if wlen >=2 :
                x.append(s[0])
                y.append(s[1])
                if wlen==3:
                    theta.append(s[2])
        xx=list(map(float,x))
        yy=list(map(float,y))

    if theta!=[]:
        tt=list(map(float,theta))
        for i in range(len(xx)):
            xt.append(xx[i]-center*S(tt[i]))
            yt.append(yy[i]-center*C(tt[i]))
            print xx[i], tt[i]
        xx=xt; yy=yt
    else: tt=[]

    marker=[]
    if dataset=='survey.marker':
        marker=[]
        for m in range(len(xx)-1):
            marker.append(xx[m+1]-xx[m]+0.31)
        write_to_file(xx,yy,str(dataset)+'x,z.txt')
    return(xx,yy, tt, marker)

def redraw(event):
    """Redraw the plot on a resize event"""
    if  np.size(plt.get_figlabels()):
        #Need to check if figure is closed or not and only then do the following
        #operations. Else, the following operations will create a new figure
        ax.clear()
        drawRectangle(ax)
        fig.canvas.draw()
    else:
        pass

def drawRectangle(ax,x,y,z,h,l,col):
    td2dis = ax.transData
    coords = td2dis.transform([x, y])
    #rotate transform
    tr = mpl.transforms.Affine2D().rotate_deg_around(coords[0], coords[1],z*180/pi)
    t = td2dis + tr
    rect1 = patches.Rectangle(((x-l/2),(y-h/2)),(l),(h),facecolor=col,alpha=1,transform=t,edgecolor='b' )
    ax.add_patch(rect1);
    plt.grid()

def make_title(figure):
    xa=min(q[1]);ya=min(q[0]);xb=max(q[1]);yb=max(q[0])
    width=round(xb-xa,2); height=round(yb-ya,2)
    fig.suptitle(str(width)+'m   x   '+str(height)+'m',fontsize=100)
    print 'xmin:',xa,'xmax:',xb,'ymin:',ya,'ymax:',yb,\
        'width:',xb-xa,'height:',yb-ya

def set_canvas():

    #figSize must me a multiple of the x and y lims (below).
    figSize = (40,22)
    fig = plt.figure('Patch rotate', figsize=figSize)
    ax = fig.add_subplot(111)
    
    ax.set_xlim(-10,10)
    ax.set_ylim(-10,1)
    fig.canvas.mpl_connect('resize_event', redraw)

    #ax.plot(f[0],f[1], color='red', markersize=30)
    return fig, ax

#PARAMETERS FOR MATPLOTLIB

mpl.rcParams['figure.dpi'] = 80   # default = 80
mpl.rcParams['savefig.dpi'] = 80  # default = 100

#PARAMETERS - QUAD Z-LENGTH AND X-WIDTH

ql,qh=.335,.4

#READ IN ELEMENTS:
#other available elements: bpms, dipoles and IOTA beamline.

q=readfile('survey.quads',0.105)

fig=set_canvas()[0]
ax=set_canvas()[1]
make_title(fig)

#draw in the elements

for i in range(len(q[0])):
    drawRectangle(ax,q[1][i],q[0][i],q[2][i], qh,ql,'r')

#quad centers:
ax.plot(q[1],q[0], 'o', color='yellow', markersize=14)

#plot and save image
plt.savefig('iota.png')
