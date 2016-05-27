# model3_1.py

import histone
import math
from numpy.random import sample
import matplotlib.pyplot as pyplot
from matplotlib.backends.backend_pdf import PdfPages
import numpy as np
"""
this file is from model3.py, with new histone file, 
which creates all cases of A, and R to A and R individually.

"""

##############################

NUM_OF_HISTONE = 81
BEFORE_PROMOTER = 40
WINDOW = 10
TIME1 = 1000
TIME2 = 1000
delta = 5

##############################


def main():
    testnum = 0
    for A in range(2):
        for R in range(2):
            submain(A,R)
            testnum += 1
            print(A*50+R*25)
#     submain(1,1)    ## test case   


def submain(A,R):
    for secA in range(2):
        for secR in range(2):
            subsubmain(A,R,secA,secR)
            print("   done")
    
#     subsubmain(1,0,0,1)

def subsubmain(A,R,secondA,secondR):
    
    fig= pyplot.figure()
    trackerList, TEextTrackerList = setHistones(A, R, secondA, secondR)
    time = np.linspace(0,TIME1+TIME2-1,TIME1+TIME2)
    
    submain1(fig,trackerList,R,A,secondR,secondA)
    submain3(fig,trackerList)
    submain4(fig,time,TEextTrackerList)
    submain5(fig,trackerList)


    title = "exp2/exp2_1_histonesA{}R{}_to_A{}R{}.pdf".format(A,R,secondA,secondR)
    pp = PdfPages(title)
    pp.savefig(fig)
    pp.close()

    
#     pyplot.show()
    
def setHistones(A,R,secondA,secondR):
    histoneList = histone.createRandomHistoneList(A=A)
    T = 0
    Eext = 0
    return histone.trackingHistones2(histoneList=histoneList,
                                   R=R,A=A,
                                   secR =secondR,
                                   secA =secondA,
                                   T=T, Eext=Eext,TIME1=TIME1, TIME2=TIME2)
    
def submain1(fig,trackerList,R,A,secondR,secondA):
    """
    this function is to create a graph of all histones status
    """
    bx = fig.add_subplot(3,1,1)
    bx.tick_params(left ="off",labelleft="off")

    for h in range(NUM_OF_HISTONE):
        trackerM = [i for i in range(TIME1+TIME2) if trackerList[h][i] == "m"]
        y = [h for i in range(len(trackerM))]
        bx.plot(trackerM,y,",",color = "blue")
        trackerA = [i for i in range(TIME1+TIME2) if trackerList[h][i] == "a"]
        y = [h for i in range(len(trackerA))]
        bx.plot(trackerA,y,",",color = "red")

    bx.set_xlim(-0.5,TIME1+TIME2)
    bx.set_xticks([0,TIME1,TIME2])
#     bx.set_ylabel("histones' status")

    bx.set_ylim(-1,NUM_OF_HISTONE+0.5)
    bx.set_title(r"Percentage of histones: $R={}, A={} \to R={}, A = {}$".format(R,A,secondR,secondA))

def submain3(fig,trackerList):
    """
    this function creates a bar graph of histones within the window
    """
    bx = fig.add_subplot(6,1,3)
    time = [i for i in range(TIME1,TIME1+TIME2,delta)]

    list_a1,list_a2 = turnTrackerlistToList_a1a2(trackerList)

    bx.plot(time, list_a1,"-",color="blue")
    bx.plot(time, list_a2,"-",color="red")

    # bx.set_xlim(TIME1,TIME1+TIME2)
    bx.set_ylim(0,10)
    bx.set_ylabel("percentage\n in\n  windown")
    bx.set_xlim(0,TIME1+TIME2)

    bx.grid(True,axis='y')

def submain4(fig,time,TEextTrackerList):
    """
    this function is to create a graph of T status
    """
    cx = fig.add_subplot(6,1,4)
    # T_List = T_list_maker(trackerList)
    T_List = [TEextTrackerList[i][0] for i in range(TIME1+TIME2)]
    cx.plot(time,T_List,"-",color="red",drawstyle="steps")
    #cx.scatter(time,T_List)
    cx.set_xlabel("time")
    cx.set_xticks((0,TIME1,TIME2))
    cx.set_xlim(-0.5,TIME1+TIME2)
    cx.set_yticks([])
#     cx.set_yticklabels(("O%","100%"))
    cx.set_ylim(-0.5,1+.5)

    first = index_First_T_on(TEextTrackerList)
    textstr = 'delay:\n %d'%(first)
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
    cx.text(0.8, 0.9, textstr,transform=cx.transAxes,fontsize=10,
        verticalalignment='top', bbox=props)


def submain5(fig,trackerList):
    """
    this function is to create a statistics of histones methylated 
    before and after the shock.
    """
    list_of_lists = turnTrackerlistToList_b1b2c1c2(trackerList)

    bx = fig.add_subplot(6,2,9)
    cx = fig.add_subplot(6,2,10)
    bx.set_xlim(-0.5,TIME1//delta)
    cx.set_xlim(-0.5,TIME1//delta)
    cx.set_yticks([])

    xaxis = [i for i in range(NUM_OF_HISTONE)]
    print(len(list_of_lists[0]))
    bx.barh(xaxis,list_of_lists[0],color="b",align="center")
    cx.barh(xaxis,list_of_lists[2],color="b",align="center")
    bx = fig.add_subplot(6,2,11)
    cx = fig.add_subplot(6,2,12)   
    bx.barh(xaxis,list_of_lists[1],color="b",align="center")
    cx.barh(xaxis,list_of_lists[3],color="b",align="center")
    bx.set_xlim(-0.5,TIME2//delta)
    cx.set_xlim(-0.5,TIME2//delta)

def turnTrackerlistToList_a1a2(trackerList):
    list_a1 = [0 for _ in range(TIME1,TIME1+TIME2,delta)] # list of # of methylated histones
    list_a2 = [0 for _ in range(TIME1,TIME1+TIME2,delta)] # list of # of acetilated histones
    for i in range(NUM_OF_HISTONE//2- WINDOW//2,NUM_OF_HISTONE//2 + WINDOW//2 +1):
        counter = 0
        for t in range(TIME1,TIME1+TIME2,delta):
            if(trackerList[i][t] =="m"):
                list_a1[counter] += 1
            elif(trackerList[i][t] =="a"):
                list_a2[counter] += 1
            counter += 1
    return list_a1, list_a2

def turnTrackerlistToList_b1b2c1c2(trackerList):
#     list_b1 = [0 for _ in range(0,TIME1,delta)] # list of # of methylated histones before shock
#     list_b2 = [0 for _ in range(0,TIME1,delta)] # list of # of acetilated histones before shock
#     list_c1 = [0 for _ in range(TIME1,TIME1+TIME2,delta)] # list of # of methylated histones after shock
#     list_c2 = [0 for _ in range(TIME1,TIME1+TIME2,delta)] # list of # of accetilated histone after shock
    list_b1 = [0 for _ in range(NUM_OF_HISTONE)] # list of # of methylated histones before shock
    list_b2 = [0 for _ in range(NUM_OF_HISTONE)] # list of # of acetilated histones before shock
    list_c1 = [0 for _ in range(NUM_OF_HISTONE)] # list of # of methylated histones after shock
    list_c2 = [0 for _ in range(NUM_OF_HISTONE)] # list of # of accetilated histone after shock

    counter = 0    
    for i in range(NUM_OF_HISTONE):
        for t in range(0,TIME1,delta):
            if(trackerList[i][t] =="m"):
                list_b1[i] += 1
            elif(trackerList[i][t] =="a"):
                list_b2[i] += 1
        
        for t in range(TIME1,TIME1+TIME2,delta):
            if(trackerList[i][t] == "m"):
                list_c1[counter] +=1
            elif(trackerList[i][t] == "a"):
                list_c2[counter] +=1
        counter += 1
    return [list_b1,list_b2,list_c1,list_c2]
def index_First_T_on(list):
    for i in range(len(list)):
        if(list[i][0] != 0):
            return i
    return 0
        

if __name__ == "__main__":
    main()
