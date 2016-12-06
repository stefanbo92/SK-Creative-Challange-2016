import matplotlib.pyplot as plt

def plotError(errorVec):
    zeroVec=[]
    contVec=[]

    for i in range(len(errorVec)):
        zeroVec.append(0)
        contVec.append(i)
        
    plt.plot(contVec,errorVec,contVec,zeroVec)
    plt.ylabel('error')
    plt.xlabel('timestep')
    plt.show()

plotError([0,0.9,0.2,1.3,-0.2,-1,0,0.3])
