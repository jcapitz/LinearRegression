#!/usr/bin/python

# import libraries
import seaborn as sns
import matplotlib.pyplot as plt
#%matplotlib inline

# set up figure
fig, axes = plt.subplots(2,2, figsize = (12,10))

# R-sq
### $R^2$ Criteria

##### This pairs the model name with the corresponding $R^2$ value

rsqdict = {}
for key, values in modeldict.iteritems():
    rsqdict[key] = values.fit().rsquared

pd.options.display.float_format = '{:20,.4f}'.format
    
dfr1 = DataFrame(rsqdict.items(), columns = ['model','R-sq']).sort(['model'], 
                                                                 ascending=[1]).reset_index(drop = True)

##### Now create a graph to illustrate the corner principle:

prsq = zip(paxis,rsqvals)

maxrsq = []
for j in range(1,6):
    maxrsq.append(max([prsq[i][1] for i in range(len(prsq)) if prsq[i][0] == j]))

axes[0,0].set_title('Corner Principle for $R^2$')
axes[0,0].scatter(paxis,rsqvals)
axes[0,0].plot(range(1,6),maxrsq)
axes[0,0].set_xlabel('p')
axes[0,0].set_ylabel('$R^2$')

# adj. R-sq
### Adjusted $R^2$ Criteria

adj_rsqdict = {}
for key, values in modeldict.iteritems():
    adj_rsqdict[key] = values.fit().rsquared_adj

dfr2 = DataFrame(adj_rsqdict.items(), columns = ['model','Adj. R-sq']).sort(['model'], 
                                                                 ascending=[1]).reset_index(drop = True)

adj_prsq = zip(paxis,adj_rsqvals)

adj_maxrsq = []
for j in range(1,6):
    adj_maxrsq.append(max([adj_prsq[i][1] for i in range(len(adj_prsq)) if adj_prsq[i][0] == j]))

axes[0,1].set_title('Corner Principle for Adjusted $R^2$')
axes[0,1].scatter(paxis,adj_rsqvals)
axes[0,1].plot(range(1,6),adj_maxrsq)
axes[0,1].set_xlabel('p')
axes[0,1].set_ylabel('adj. $R^2$')

# AIC
### AIC

aicdict = {}
for key, values in modeldict.iteritems():
    aicdict[key] = n * np.log(values.fit().ssr) - n * np.log(n) + 2 * values.fit().df_model

dfr3 = DataFrame(aicdict.items(), columns = ['model','AIC']).sort(['model'],
                                                           ascending=[1]).reset_index(drop = True)

paic = zip(paxis,aic)

minaic = []
for j in range(1,6):
    minaic.append(min([paic[i][1] for i in range(len(paic)) if paic[i][0] == j]))

axes[1,0].set_title('Corner Principle for AIC')
axes[1,0].scatter(paxis,aic)
axes[1,0].plot(range(1,6),minaic)
axes[1,0].set_xlabel('p')
axes[1,0].set_ylabel('AIC')

# Cp
### $C_p$

Cpdict = {}
for key, values in modeldict.iteritems():
    Cpdict[key] = (values.fit().ssr/full_mse) - n + 2 * values.fit().df_model

dfr4 = DataFrame(Cpdict.items(), columns = ['model','Cp']).sort(['model'],
                                                           ascending=[1]).reset_index(drop = True)

pcp = zip(paxis,Cp)

mincp = []
for j in range(1,6):
    mincp.append(min([pcp[i][1] for i in range(len(pcp)) if pcp[i][0] == j]))

axes[1,1].set_title('Corner Principle for $C_p$')
axes[1,1].scatter(paxis,Cp)
axes[1,1].plot(range(1,6),mincp)
axes[1,1].set_xlabel('p')
axes[1,1].set_ylabel('$C_p$')

plt.show()
