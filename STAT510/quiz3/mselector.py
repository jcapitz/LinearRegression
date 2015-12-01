#!/usr/bin/python

from statsmodels.formula.api import ols

def foresel(df, response, alpha = 0.1):
    ''' Performs forward selection for regression.
    args:
        df = data frame with response and covariates
        alpha = a float indicating confidence level
        response = string that represents the response variable
            e.g. 'Y'
    attributes:
        summary = ols(formula,data).fit().summary()
    '''
    # initial assignments
    covariates = set(df.columns)
    covariates.remove(response)
    candidates = []
    
    while True:
        
        oldpval = alpha
        rejects = set()
    
        for variable in covariates:
            candidatesubset = candidates + [variable]
            formula = '{} ~ {}'.format(response, ' + '.join(candidatesubset))
            pval = ols(formula,df).fit().pvalues[-1]
            if pval < oldpval:
                var2add = variable
                oldpval = pval
                optmodel = formula
            else:
                rejects.add(variable)
                
        candidates.append(var2add)
        covariates.remove(var2add)
        
        if covariates == rejects:
            
            print 'The optimal model is {}'.format(optmodel)
            
            break
            
    return ols(optmodel,df).fit().summary()


def backsel(df, response, alpha = 0.1):
    '''
    Performs backward selection for regression.
    args:
        df = data frame with response and covariates
        alpha = a float indicating confidence level
        response = string that represents the response variable
            e.g. 'Y'
    attributes:
        summary = ols(formula,data).fit().summary()
    '''
    # initial assignments
    covariates = set(df.columns)
    covariates.remove(response)
    formula = '{} ~ {}'.format(response,' + '.join(list(covariates)))
    
    while True:
        
        pvals = ols(formula,df).fit().pvalues
        candidates = pvals[pvals > alpha]
        
        if candidates.empty:
            break
            
        dropvar = candidates[candidates == max(candidates)].index[0]
        covariates.remove(dropvar)
        
        formula = '{} ~ {}'.format(response,' + '.join(list(covariates)))
    
    print 'The optimal model is {}'.format(formula)
    
    return ols(formula,df).fit().summary()


def stepwsel(df , response, alpha = 0.1):
    '''
    Performs stepwise selection for regression.
    ARGS:
        DF = Data frame with response and covariates
        alpha = a float indicating confidence level
        response = string that represents the response variable
            e.g. 'Y'
    attributes:
        summary = ols(formula,data).fit().summary()
    '''
    # initial assignments
    covariates = set(df.columns) # variables in dataframe
    covariates.remove(response) # remove Y
    candidates = []
    dropvar =[]
    optmodelpvals = [0]
    
    while True:
        
        oldpval = alpha # initial value to enter adding variable if statement
        rejects = set() # space for variables not entered in model
        
        if any(optmodelpvals) > alpha: # drop non-significant
            dropvar = list(optmodelpvals[optmodelpvals > .1].index)
            if 'Intercept' in dropvar:
                dropvar.remove('Intercept')
        
        for variable in covariates:
            candidatesubset = candidates + [variable]
            [candidatesubset.remove(element) for element in dropvar] # remove variables in dropvar
            formula = '{} ~ {}'.format(response, ' + '.join(candidatesubset)) # create model based on subset
            pval = ols(formula,df).fit().pvalues # get pvalues
            
            if pval[-1] < oldpval: # if the pavalue of the variable just added is significant then considered to be added
                var2add = variable # place holder
                oldpval = pval[-1] # update
                optmodelpvals = pval
                optmodelvars = candidatesubset
            else:
                rejects.add(variable) # add to rejected if not significant
              
        candidates.append(var2add)
        
        if covariates == rejects:
            optmodelvars.remove(dropvar[0])
            optmodel = '{} ~ {}'.format(response, ' + '.join(optmodelvars))
            print 'The optimal model is {}'.format(optmodel)
            break
            
        covariates.remove(var2add)
            
    return ols(optmodel,df).fit().summary()
