import matplotlib.pyplot as plt
import dynamics
import math

class PredatorPrey(dynamics.Dynamics):
    def __init__(self, preyBirth, preyDeath, predBirth, predDeath, time_step):
        numEquations = 2                            # set the number of state equations

        # set constants
        self.preyInc = preyBirth
        self.preyDec = preyDeath
        self.predInc = predBirth
        self.predDec = predDeath
        self.initialPestAmount = 1 #do not set above 3
        self.pestAmount = self.initialPestAmount

        super().__init__(numEquations, time_step)   # initialize super class dynamics (Euler Method)

        # create variables to hold the state history for plotting
        self.Q = [[] for i in range(numEquations)]
        self.T = []

    def initialize(self, preyWeight, predWeight):
        # set state variable initial values
        self.q[0] = preyWeight
        self.q[1] = predWeight
        # initialize state history used for plotting
        self.Q = [[self.q[i]] for i in range(len(self.q))]
        self.T = [0.0]

    def advance(self, count):
        #bounds the max amount of insects desired on average
        if(self.q[1] > 50):
            self.pestAmount = self.initialPestAmount
        
        #Reapplication by pesticide remaining, kept for testing purposes
        #if(self.pestAmount < .2):
        #    self.pestAmount = self.initialPestAmount
        # compute "count" updates of the state equations
        for i in range(count):
            #Original equation, kept for swapping with below line for testing.
            #self.dq[0] = (self.preyInc * self.q[0]) - (self.preyDec * self.q[0] * self.q[1]) 
            self.dq[0] = (self.preyInc * self.q[0]) - ((self.preyDec + (1/(1+math.exp(-self.pestAmount)))/30) * self.q[0] * self.q[1])
            self.dq[1] = (self.predInc * self.q[0] * self.q[1]) - ((self.predDec + (1/(1+math.exp(-self.pestAmount)))) * self.q[1])
            self.step()
        # save the updated state variables after the "count" updates for plotting
        [self.Q[i].append(self.q[i]) for i in range(len(self.q))]
        self.T.append(self.now())
        if(self.pestAmount > self.dt*2):
            self.pestAmount -= self.dt*2

    def print(self):
        # custom print for current simulation
        print('time={0:10f} prey={1:10f} predator={2:10f} pestAmount={3:10f} pestModifier={4:10f}'.format(self.time, self.q[0], self.q[1], self.pestAmount, (1/(1+math.exp(-self.pestAmount)))))

    def plot(self):
        # custom plot for current simulation
        plt.figure()
        plt.subplot(311)
        plt.plot(self.T, self.Q[0], 'k')
        plt.ylabel('prey')

        plt.subplot(312)
        plt.plot(self.T, self.Q[1], 'r')
        plt.ylabel('predator')

        plt.subplot(313)
        plt.plot(self.T, self.Q[0], 'k', self.T, self.Q[1], 'r--')
        plt.ylabel('prey - predator')
        plt.xlabel('time')

        plt.figure()
        plt.plot(self.Q[0], self.Q[1], 'b')
        plt.ylabel('predator')
        plt.xlabel('prey')

        plt.show()




# set parameters for predator-prey simulation

# parameters describing the simulation time
endTime = 5000.0       # length of simulation (i.e. end time)
dt = 0.005             # time step size used to update state equations

# parameters describing the real system
preyBirth = 0.05
preyDeath = 0.001
predBirth = 0.0005
predDeath = 0.01
initPreyWt = 150.0
initPredWt = 50.0

# create the simulation and initialize state variables
P = PredatorPrey(preyBirth, preyDeath, predBirth, predDeath, dt)
P.initialize(initPreyWt, initPredWt)

# run the simulation
displayInterval = 100         # number of state updates before saving state
while P.now() < endTime:
    P.advance(displayInterval)
    P.print()               # call print to see numeric values of state per display interval

P.plot()                    # call custom plot

