import matplotlib.pyplot as plt
import numpy as np
import csv

# Set constants
L1 = 6.25
L2 = 12

cycle1 = np.loadtxt("/Users/aidanbeckett/Library/Mobile Documents/com~apple~CloudDocs/Documents/MATLAB/ME31/angles1.csv", delimiter=',')
cycle2 = np.loadtxt("/Users/aidanbeckett/Library/Mobile Documents/com~apple~CloudDocs/Documents/MATLAB/ME31/angles2.csv", delimiter=',')

dance1 = np.loadtxt("/Users/aidanbeckett/Library/Mobile Documents/com~apple~CloudDocs/Documents/MATLAB/ME31/dance1.csv", delimiter=',')
dance2 = np.loadtxt("/Users/aidanbeckett/Library/Mobile Documents/com~apple~CloudDocs/Documents/MATLAB/ME31/dance2.csv", delimiter=',')

for i in range(len(cycle1)):
    angles = [cycle1[i]/180*np.pi - np.pi/2, cycle2[i]/180*np.pi]
    
    # Use forward kinematics to calculate position of each leg
    leg1x = [0, L1*np.cos(angles[0])]
    leg1y =[0, L1*np.sin(angles[0])]
    leg2x = [L1*np.cos(angles[0]), L1*np.cos(angles[0]) + L2*np.cos(angles[0] + angles[1])]
    leg2y =[L1*np.sin(angles[0]), L1*np.sin(angles[0]) + L2*np.sin(angles[0] + angles[1])]

    # Plot the two legs to creat the digital twin
    plt.clf() #clear figure
    plt.plot(leg1x, leg1y)
    plt.plot(leg2x, leg2y)
    plt.xlim([-9,9])
    plt.ylim([-18,0])
    plt.pause(0.02)

plt.show()
