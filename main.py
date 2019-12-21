import pygame as pg
#from pygame.locals import *
import sys,time
import random as r
sortindex=0
now=0
#seln=0
selindex=0
MIDU=int(sys.argv[2])if len(sys.argv)>2 else 50
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
    return (now,sortindex)
def maopaosort(lists):
    global sortindex,MIDU
    sortindex+=1
    if sortindex>=MIDU-1:
        sortindex=0
    if lists[sortindex]>lists[sortindex+1]:
        temp=lists[sortindex]                                                                 
        lists[sortindex]=lists[sortindex+1]
        lists[sortindex+1]=temp
    return (sortindex,sortindex+1)
def clean(lists):
    global sortindex,selindex,now
    sortindex=0
    selindex=0
    now=0
    r.shuffle(lists)

sorts=(maopaosort,selectsort)
def start(mode):
    global sorts
    pg.init()
    window=((1000,600))
    scr=pg.display.set_mode(window)
    pg.display.set_caption('Lowwwwww')
    bs=pg.Surface(window)
    lists=[i for i in range(MIDU)]
    r.shuffle(lists)
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
        if isdonesort(lists):
            color=sure.copy()
        else:
            nowtime=int(time.clock())
            d=sorts[1](lists) if mode=='selectsort' else sorts[0](lists)
            if d:
                for c in d:
                    color[c]=(255,0,0)
        # draw
        x=0 
        for num in lists:
            pg.draw.rect(bs,color[num],(x,(600-num),1000//MIDU,num),0)
            x+=1000//MIDU
        printtext(str(nowtime)+' '+str(MIDU)+' array',pg.font.Font(None,100),4,4,bs)
        scr.blit(bs,(0,0))
        pg.display.update()
        
start(sys.argv[1] if len(sys.argv)>1 else 'selectsort')
        