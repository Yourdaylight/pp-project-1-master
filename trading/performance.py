# Evaluate performance.
import numpy as np
import matplotlib.pyplot as plt
def read_ledger(ledger_file):
    '''
    Reads and reports useful information from ledger_file.
    '''
    res=[]
    with open(ledger_file,"r") as f:
        for line in f.readlines()[1:]:
            a=line.split(",")
            res.append(a)
    res=np.array(res)
    number=res.shape[0]
    print("The total number of transactions:",number)
    transcations=res[:,5].astype(float)
    day=res[:,1].astype(int)
    spend=transcations[np.where(transcations<0)]
    earned=transcations[np.where(transcations>0)]
    print("Total spend:{:.2f};Total earned:{:.2f}".format(sum(spend),sum(earned)))
    print("The overall profit {:.2f}".format(sum(spend)+sum(earned)))

    total=0
    y=[]
    for i in transcations:
        total+=i
        y.append(total)
    plt.plot(day,y)
    plt.xlabel("day")
    plt.ylabel("profit")
    plt.show()
    return res
if __name__=="__main__":
    ca=read_ledger("../ledger_crossing_averages.txt")

    # total=0
    # x=caa[:,1]
    # y=[]
    # for i in caa[:,5].astype(float):
    #     total+=i
    #     y.append(total)
    # # y=caa[:,5].astype(float)
    # plt.plot(x,y)
    # plt.show()

