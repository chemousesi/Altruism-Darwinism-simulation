import matplotlib.pyplot as plt
import numpy as np
#create figure
plt.figure()

#define width of candlestick elements
width = .4
width2 = .05

param_values = [ 1, 2 ,3,4 ,5, 6, 7, 8, 9, 10]


#define up and down prices
altruists = np.empty((10, 10))
profiteers = np.empty((10, 10))

for i in range(10):
    new_arr= np.random.randint(10, 20, 10)
    altruists[i] = new_arr
    new_arr = np.random.randint(10, 20, 10)
    profiteers[i] = new_arr

#profiteers = np.random.randint(10, 20, 10)

# Calculate the mean    
mean_values_alt = np.mean(altruists, axis=1)
mean_values_prof = np.mean(profiteers, axis=1)

# calculate max
max_values_alt = np.max(altruists, axis=1)
max_values_prof = np.max(profiteers, axis=1)
#calculate min 
min_values_alt = np.min(altruists, axis=1)
min_values_prof = np.min(profiteers, axis=1)


# Calculate the standard deviation
std_values_alt = np.std(altruists, axis=1)
std_values_profiteers = np.std(profiteers, axis=1)

#define colors to use
col1 = 'green'
col2 = 'red'

#plotaltruists
plt.bar(param_values, 2*std_values_alt,width=width,bottom=mean_values_alt-std_values_alt,color=col1)
plt.bar(param_values,max_values_alt-min_values_alt,width2,bottom=min_values_alt,color=col1)
#plt.bar(param_values,down.high-down.open,width2,bottom=down.open,color=col2)

#plot profiteers
plt.bar(param_values, 2*std_values_profiteers,width=width,bottom=mean_values_prof-std_values_profiteers,color=col2)
plt.bar(param_values,max_values_prof-min_values_prof,width2,bottom=min_values_prof,color=col2)

plt.ylim(0)
#display candlestick chart
plt.show()