import pygame as pg
from pygame.locals import *
import sys,time
import random as r
sortindex=0
now=0
#seln=0
selindex=0
d=0
path=[]
MIDU=int(sys.argv[2])if len(sys.argv)>2 else 50
class btree:
    def __init__(self,value=None):
        self.data=value
        self.left=None
        self.right=None
    def insertleft(self,value):
        self.left=btree(value)
        return self.left
    def insertright(self,value):
        self.right=btree(value)
        return self.right
root=btree()
class colorblock:
    def __init__(self,num,color='red'):
        if isinstance(color,str):
            if color=='green':
                self.color=(0,255,0)
            elif color=='red':
                self.color=(255,0,0)
            elif color=='blue':
                self.color=(0,0,255)
            else:
                raise NameError
        else:
            self.color=color
        self.num=num
def printtext(text,font,x,y,bs,color=(255,255,255),shadow=0):
    screen = bs
    if shadow:
        image=font.render(text,True,(0,0,0))
        screen.blit(image,(x+shadow,y+shadow))
    image=font.render(text,True,color)
    screen.blit(image,(x,y))
    pg.display.update()
def isdonesort(lists):
    for n in range(len(lists)-1):
        if lists[n]>lists[n+1]:
            return False
    return True
def selectsort(lists):
    global sortindex,MIDU,now,selindex
    sortindex+=1
    if sortindex>MIDU-1:
        #lists[now]=seln
        temp=lists[now]
        lists[now]=lists[selindex]
        lists[selindex]=temp
        if now<MIDU-1:
            now+=1
        selindex=now
        sortindex=now
    # select sort
    #print(sortindex,lists[now],lists[selindex],lists)
    if lists[sortindex]<lists[selindex]:
        #seln=lists[sortindex]
        selindex=sortindex
    return (colorblock(now,'green'),colorblock(sortindex),colorblock(selindex,'blue'))
def maopaosort(lists):
    global sortindex,MIDU,now
    if now==0:
        now=MIDU-1
    sortindex+=1
    if sortindex>=now:
        now-=1
        sortindex=0
    if lists[sortindex]>lists[sortindex+1]:
        temp=lists[sortindex]                                                                 
        lists[sortindex]=lists[sortindex+1]
        lists[sortindex+1]=temp
    return (colorblcok(sortindex),colorblock(sortindex+1))
def monkeysort(lists):# THE SILLY SORT
    r.shuffle(lists)
    return (colorblcok(r.randint(0,MIDU-1)),colorblock(r.randint(0,MIDU-1)))
def insertsort(lists):
    global sortindex,MIDU,now,selindex
    if sortindex==0:# fisrt run init
        selindex=-1
        sortindex=1
    selindex+=1
    if lists[selindex]>=lists[sortindex]:
        temp=lists[sortindex]
        lists.pop(sortindex)
        lists.insert(selindex,temp)
        sortindex+=1
        selindex=-1
    if sortindex>MIDU-1:
        sortindex-=1
    return (colorblock(selindex if selindex>0 else selindex+1),colorblock(sortindex,'green'))
'''
def shellSort(arr): 
    MIDU = len(arr)
    gap = int(n/2)
    while gap > 0: 
        for sortindex in range(gap,MIDU): 
            temp = arr[sortindex] 
            selindex =sortindex
            while  selindex >= gap and arr[selindex-gap] >temp: 
                arr[selindex] = arr[selindex-gap] 
                selindex -= gap 
            arr[selindex] = temp 
        gap = int(gap/2)
'''
def shellsort(lists):
    global sortindex,MIDU,now,selindex,d
    if now==0:# fisrt run
        now=1
        d=MIDU//2
    if selindex>=d and lists[selindex-d]>lists[sortindex]:
        temp=lists[selindex]
        lists.pop(selindex)
        lists.insert(sortindex,temp)
        selindex-=d
    else:
        sortindex+=1
        selindex=sortindex
    if sortindex>MIDU-1:
        d=d//2
        sortindex=d
        selindex=sortindex
    return (colorblock(selindex),colorblock(sortindex,'green')) 
def _insert(node,value):
    if value>node.data:
        if node.right:
            _insert(node.right,value)
        else:
            node.insertright(value)
    else:
        if node.left:
            _insert(node.left,value)
        else:
            node.insertleft(value)
def bintreesort(lists):
    global MIDU,sortindex,now,root,path
    if not root.data:
        root=btree(lists[sortindex])
    if sortindex>=MIDU-1:
        now=1
        sortindex=0
    if now==0:
        sortindex+=1
        # gen tree
        _insert(root,lists[sortindex])
    elif now==3:
        now=1
    else:
        if not path:
            path.append(root)
        print([i.data for i in path])
        if path[-1].data:
            if path[-1].left:
                path.append(path[-1].left)
                now=3
                return [sortindex]
            lists[sortindex]=path[-1].data
            sortindex+=1
            if path[-1].right:
                now=3
                path.append(path[-1].right)
                return [sortindex]
            path.pop()
                
            
def clean(lists):
    global sortindex,selindex,now,d
    d=0
    sortindex=0
    selindex=0
    now=0
    r.shuffle(lists)

sorts={'maopaosort':maopaosort,'selectsort':selectsort,'insertsort':insertsort,'bintreesort':bintreesort,'shellsort':shellsort}
def start(mode):
    global sorts
    pg.init()
    window=((1000,600))
    scr=pg.display.set_mode(window)
    pg.display.set_caption('Lowwwwww')
    bs=pg.Surface(window)
    lists=[i for i in range(MIDU)]
    r.shuffle(lists)
    #lists.reverse()
    color=[(255,255,255) for i in range(MIDU)]
    basecolor=color.copy()
    sure=[(0,255,0) for i in range(MIDU)]
    nowtime=0
    while True:
        #time.sleep(0.01)
        color=basecolor.copy()
        bs.fill((0,0,0))
        for e in pg.event.get():
            if e.type==12:
                sys.exit()
        keys=pg.key.get_pressed()
        if keys[K_q]:
            sys.exit()
        elif keys[K_c]:
            clean(lists)
            nowtime=0
        if isdonesort(lists):
            color=sure.copy()
        else:
            nowtime=time.clock()
            d=sorts.get(mode,monkeysort)(lists)
            if d:
                for c in d:
                    color[c.num]=c.color
        # draw
        x=0
        count=0
        for num in lists:
            pg.draw.rect(bs,color[count],(x,(600-num),1000//MIDU,num),0)
            count+=1
            x+=1000//MIDU
        printtext('{:.4f}'.format(nowtime)+' '+str(MIDU)+' array '+ mode,pg.font.Font(None,80),4,4,bs)
        scr.blit(bs,(0,0))
        pg.display.update()
        
start(sys.argv[1] if len(sys.argv)>1 else 'selectsort')
        