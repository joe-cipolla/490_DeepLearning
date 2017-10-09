# Question 1:
# Get a convergent solution for all letters:
alpha = 1.0
eta = 0.5
maxNumIterations = 1000
epsilon = 0.1
numTrainingDataSets = 4
seed_value = 1

vWeightTracker, wWeightTracker, hiddenBiasTracker, outputBiasTracker, SSETracker, letterTracker, outputArrayTracker = main(
    alpha=alpha,
    eta=eta,
    maxNumIterations=maxNumIterations,
    epsilon=epsilon,
    numTrainingDataSets=numTrainingDataSets,
    seed_value=seed_value,
    numHiddenNodes = 10
)
plotSSE(SSETracker, letterTracker, alpha=alpha,
    eta=eta,
    maxNumIterations=maxNumIterations,
    epsilon=epsilon,
    numTrainingDataSets=numTrainingDataSets,
    seed_value=seed_value)

# Question 2:
# Explore sensitivity of SSE to alpha
eta = 0.5
maxNumIterations = 1000
epsilon = 0.1
numTrainingDataSets = 4
seed_value = 1
maxNumIterations = 10000
for a in [0.5,1.0,1.5]:
    vWeightTracker, wWeightTracker, hiddenBiasTracker, outputBiasTracker, SSETracker, letterTracker, outputArrayTracker = main(
        alpha=a,
        eta=eta,
        maxNumIterations=maxNumIterations,
        epsilon=epsilon,
        numTrainingDataSets=numTrainingDataSets,
        seed_value=seed_value
    )
    plotSSE(SSETracker, letterTracker, alpha=a,
            eta=eta,
            maxNumIterations=maxNumIterations,
            epsilon=epsilon,
            numTrainingDataSets=numTrainingDataSets,
            seed_value=seed_value)

# Explore sensitivity of SSE to eta
alpha = 1.0
maxNumIterations = 10000
epsilon = 0.1
numTrainingDataSets = 4
seed_value = 1
for e in [0.1,0.5,1.0]:
    vWeightTracker, wWeightTracker, hiddenBiasTracker, outputBiasTracker, SSETracker, letterTracker, outputArrayTracker = main(
        alpha=alpha,
        eta=e,
        maxNumIterations=maxNumIterations,
        epsilon=epsilon,
        numTrainingDataSets=numTrainingDataSets,
        seed_value=seed_value
    )
    plotSSE(SSETracker, letterTracker, alpha=alpha,
            eta=e,
            maxNumIterations=maxNumIterations,
            epsilon=epsilon,
            numTrainingDataSets=numTrainingDataSets,
            seed_value=seed_value)

# Both together now
maxNumIterations = 3000
epsilon = 0.1
numTrainingDataSets = 4
seed_value = 1
alpha = np.arange(0.4,2.1,.1)
eta   = np.arange(0.1,2.1,.1)
tuneGrid = np.zeros((len(alpha),len(eta)))
for a in range(len(alpha)):
    for e in range(len(eta)):
        vWeightTracker, wWeightTracker, hiddenBiasTracker, outputBiasTracker, SSETracker, letterTracker, outputArrayTracker = main(
            alpha=alpha[a],
            eta=eta[e],
            maxNumIterations=maxNumIterations,
            epsilon=epsilon,
            numTrainingDataSets=numTrainingDataSets,
            seed_value=seed_value
        )
        tuneGrid[a,e]=len(SSETracker)

tuneGrid
plt.figure()
CS = plt.contour(eta, alpha, tuneGrid,linestyles='dashed')
plt.clabel(CS, inline=1, fontsize=10)
plt.title('Contours of iterations reached before epsilon reaches 0.1 \n (maxIter = 3000)')
plt.xlabel('eta')
plt.ylabel('alpha')

# tuneGrid = np.load('tuneGrid.p')
# np.amin(tuneGrid,axis=1)
# Lowest value of iterations for eta = 2.1, alpha = 1.3

# Question 4
# Explore sensitivity of SSE & convergence iterations to initial weight arrays
alpha = 1.3
eta = 2.1
maxNumIterations = 3000
epsilon = 0.1
numTrainingDataSets = 4
seed_value =np.arange(1,100)
vW = dict()
wW = dict()
hiddenBias = dict()
outputBias = dict()
SSE = dict()
iterStop = dict()
letters = dict()
op = dict()
for s in range(len(seed_value)):
    vWeightTracker, wWeightTracker, hiddenBiasTracker, outputBiasTracker, SSETracker, letterTracker, outputArrayTracker = main(
        alpha=alpha,
        eta=eta,
        maxNumIterations=maxNumIterations,
        epsilon=epsilon,
        numTrainingDataSets=numTrainingDataSets,
        seed_value=seed_value[s]
    )
    wW[s] = vWeightTracker.pop(len(vWeightTracker))
    vW[s] = wWeightTracker.pop(len(wWeightTracker))
    hiddenBias[s] = hiddenBiasTracker.pop(len(hiddenBiasTracker))
    outputBias[s] = outputBiasTracker.pop(len(outputBiasTracker))
    iterStop[s] = len(SSETracker)
    SSE[s] = SSETracker.pop(len(SSETracker))
    letters[s] = letterTracker.pop(len(letterTracker))
    op[s] = outputArrayTracker.pop(len(outputArrayTracker))

i, sse = zip(*SSE.items())
plt.hist(sse,bins=30)
plt.title('Histogram of SSE for 100 random starts')
plt.xlabel('SSE')
plt.ylabel('Count')

# w weights ->
d = pd.DataFrame(wW.items(),columns=['seed','value'])

wWaverages = np.zeros([5,6])
wWstd = np.zeros([5,6])
for o in np.arange(5): #5 outputs
    for h in np.arange(6): #6 hidden
        wWaverages[o][h] = np.mean([d.value[i][o][h] for i in np.arange(d.shape[0])])
        wWstd[o][h] = np.std([d.value[i][o][h] for i in np.arange(d.shape[0])])
wWaverages
wWstd

for h in np.arange(5):
    plt.hist([d.value[i][0][h] for i in np.arange(d.shape[0])],alpha = .7)
    plt.title('Weights for 6 hidden nodes in W array for output=0 node over 100 runs')
    plt.xlabel('Weight')

# v weights ->
d = pd.DataFrame(vW.items(),columns=['seed','value'])

vWaverages = np.zeros([6,25])
vWstd = np.zeros([6,25])
for i in np.arange(25): #5 outputs
    for h in np.arange(6): #6 hidden
        vWaverages[h][i] = np.mean([d.value[x][h][i] for x in np.arange(d.shape[0])])
        vWstd[h][i] = np.std([d.value[x][h][i] for x in np.arange(d.shape[0])])
vWaverages
vWstd

for h in np.arange(25):
    plt.hist([d.value[x][h][0] for x in np.arange(d.shape[0])],alpha = .3)
    plt.title('Weights for 25 input nodes in V array for hidden=0 node over 100 runs')
    plt.xlabel('Weight')

plt.hist([iterStop[x] for x in np.arange(len(iterStop))],bins=50)
plt.title('Hist of iterations at which SSE < (eplison=0.1) for 100 starts')
plt.xlabel('Stop Iteration Number')


# Question 3:
# Explore sensitivity of SSE to # of hidden nodes
alpha = 1.3
eta = 2.1
maxNumIterations = 5000
epsilon = 0.1
numTrainingDataSets = 4
seed_value = 1
numH = [2,8,14,20,26]
f, axarr = plt.subplots(1, 5, sharey=True)
for i, row in zip(np.arange(len(numH)), axarr):
    hidden_nodes = numH[i]
    vWeightTracker, wWeightTracker, hiddenBiasTracker, outputBiasTracker, SSETracker, letterTracker, outputArrayTracker = main(
        alpha=alpha,
        eta=eta,
        maxNumIterations=maxNumIterations,
        epsilon=epsilon,
        numTrainingDataSets=numTrainingDataSets,
        seed_value=seed_value,
        numHiddenNodes = hidden_nodes
    )
    plotSubplots(SSETracker, letterTracker, alpha=alpha,
            eta=eta,
            maxNumIterations=maxNumIterations,
            epsilon=epsilon,
            numTrainingDataSets=numTrainingDataSets,
            seed_value=seed_value,
            axi = row,
            numHiddenNodes=hidden_nodes)