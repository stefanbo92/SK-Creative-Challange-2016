import matplotlib.pyplot as plt

def plotError(errorVec)
    zeroVec=[]
    contVec=[]

    for i in range(len(errorVec)):
        zeroVec.append(0)
        contVec.append(i)
        
    plt.plot(contVec,errorVec,contVec,zeroVec)
    plt.ylabel('error')
    plt.xlabel('timestep')
    plt.show()
