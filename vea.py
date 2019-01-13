#CS486 Assignment3 Question1
#20559425 Ye Wang

"""
This is python implementation on variable elimination problem
To test the program, compile the program with python3 vea.py
And then uncomment the test examples at the end

factors in factorList in the format: eg.p(E) = p(e=t) + p(e=f)
[[E],[[1,0.5][0,0.5]]]
(hard code the factors in and 1 represents true, 0 represents false)

individual functions can be tested by uncommenting the test examples at the end except inference function
inference function was tested by the example in class, the data is hard coded in this program
"""
import numpy as np
from copy import deepcopy

#helper function for finding needed value from source to match the goal and return the index
def find_ind(varlist,goal,source):
    ind_arr = []
    val_arr = []
    i = 0
    while i < len(varlist):
        j = 0
        while j < len(source[0]):
            if varlist[i] == source[0][j]:
                ind_arr.append(j)
                val_arr.append(goal[i])
            j += 1
        i += 1
    i = 0
    while i < len(source[1]):
        j = 0
        flag = True
        while j < len(ind_arr):
            if source[1][i][ind_arr[j]] != val_arr[j]:
                flag = False
                break
            j += 1
        if flag:
            return i
        i += 1

#helper function for summing the value from source that matching the status in goal
def sum_val(varlist,goal,source):
    sum = 0
    ind_arr = []
    val_arr = []
    i = 0
    while i < len(varlist):
        j = 0
        while j < len(source[0]):
            if varlist[i] == source[0][j]:
                ind_arr.append(j)
                val_arr.append(goal[i])
            j += 1
        i += 1
    i = 0
    while i < len(source[1]):
        j = 0
        flag = True
        while j < len(ind_arr):
            if source[1][i][ind_arr[j]] != val_arr[j]:
                flag = False
                break
            j += 1
        if flag:
            sum += source[1][i][-1]
        i += 1
    return sum

#helper function for finding the factors in factor list that contains hidden variable
def find_factors(factorlist,variable):
    #length = len(factorlist)
    result = []
    i = 0
    while i < len(factorlist):
        flag = False
        if variable in factorlist[i][0]:
            temp = factorlist.pop(i)
            result.append(temp)
            flag = True
        if flag:
            i = 0
        else:
            i += 1
    return result

def restrict(factor,variable,value):
    global n
    i = 0
    idx = None
    #find the index of variable in the array
    while i < len(factor[0]):
        if factor[0][i] == variable:
            idx = i
            break
        i += 1
    #restrict the factor
    i = 0
    while i < len(factor[1]):
        flag = False
        if factor[1][i][idx] != value:
            factor[1].pop(i)
            flag = True
        if flag:
            i = 0
        else:
            i += 1
    #remove the unnecessary data in the factor
    factor[0].pop(idx)
    i = 0
    while i < len(factor[1]):
        factor[1][i].pop(idx)
        i += 1

    return factor

def multiply(factor1,factor2):
    var_union = list(set().union(factor1[0],factor2[0]))
    var_union.sort()
    num_of_entry =  2 ** len(var_union)
    empty_entry = []
    product_factor = list()
    product_factor.append(var_union)
    product_factor.append(empty_entry)
    #reserve spaces for new data
    i = 0
    while i < num_of_entry:
        empty_temp_entry = []
        product_factor[1].append(empty_temp_entry)
        i += 1
    #fill the correct table entry in
    coe = 0.5
    while num_of_entry*coe >= 1:
        i = 0
        switch = False
        counter = 0
        while i < num_of_entry:
            if counter >= num_of_entry*coe:
                switch = not switch
                counter = 0
            if not switch:
                true = 1
                product_factor[1][i].append(true)
            else:
                false = 0
                product_factor[1][i].append(false)
            i += 1
            counter += 1
        coe *= 0.5
    #calculate the probabilities
    i = 0
    while i < num_of_entry:
        ind1 = find_ind(product_factor[0],product_factor[1][i],factor1)
        ind2 = find_ind(product_factor[0],product_factor[1][i],factor2)
        val1 = factor1[1][ind1][-1]
        val2 = factor2[1][ind2][-1]
        product = val1 * val2
        product_factor[1][i].append(product)
        i += 1
    return product_factor

def sumout(factor,variable):
    result_factor = []
    varlist = list(factor[0])
    varlist.remove(variable)
    new_var_list = varlist
    new_var_list.sort()
    result_factor.append(new_var_list)
    num_of_entry = 2 ** len(new_var_list)
    empty_entry = []
    result_factor.append(empty_entry)
    #reserve spaces for new data
    i = 0
    while i < num_of_entry:
        empty_temp_entry = []
        result_factor[1].append(empty_temp_entry)
        i += 1
    # fill the correct table entry in
    coe = 0.5
    while num_of_entry * coe >= 1:
        i = 0
        switch = False
        counter = 0
        while i < num_of_entry:
            if counter >= num_of_entry * coe:
                switch = not switch
                counter = 0
            if not switch:
                true = 1
                result_factor[1][i].append(true)
            else:
                false = 0
                result_factor[1][i].append(false)
            i += 1
            counter += 1
        coe *= 0.5
    #summing out the variable
    i = 0
    while i < num_of_entry:
        prob = sum_val(result_factor[0],result_factor[1][i],factor)
        result_factor[1][i].append(prob)
        i += 1
    return result_factor

def normalize(factor):
    length = len(factor[1])
    result_factor = list()
    result_factor.append(factor[0])
    result_factor.append(factor[1])
    sum = 0
    #calculate the sum of the original factor
    i = 0
    while i < length:
        sum += factor[1][i][-1]
        i += 1
    #normalize the factor
    i = 0
    while i < length:
        result_factor[1][i][-1] = factor[1][i][-1] / sum
        i += 1
    #check if the normalized factor summed up to one
    check_sum = 0
    i = 0
    while i < length:
        check_sum += result_factor[1][i][-1]
        i += 1
    if check_sum < 1 - 0.0005:
        print("fatal error, incorrect normalization")
        return -1
    return result_factor

def inference(factorList,queryVariables,orderedListOfHiddenVariables,evidenceList):
    global n
    len_evi = len(evidenceList)
    #restrict the factors in factor list with evidence variables
    i = 0
    while i < len_evi:
        j = 0
        while j < n:
            if evidenceList[i][0] in factorList[j][0]:
                restrict(factorList[j],evidenceList[i][0],evidenceList[i][1])
            j += 1
        i += 1
    #remove the evidence variable from orderedListOfHiddenVariables
    i = 0
    while i < len_evi:
        orderedListOfHiddenVariables.remove(evidenceList[i][0])
        i += 1
    #remove the query variable from orderedListOfHiddenVariables
    i = 0
    while i < len(queryVariables):
        orderedListOfHiddenVariables.remove(queryVariables[i][0])
        i += 1
    #sum out factors based on the ordered list
    orderedListOfHiddenVariables.reverse()
    while len(orderedListOfHiddenVariables) > 0:
        current_hid_var = orderedListOfHiddenVariables.pop()
        result = find_factors(factorList,current_hid_var)
        #multipy the factors that contains the same hidden variables
        while len(result) > 1:
            fac1 = result.pop()
            fac2 = result.pop()
            prod_fac = multiply(fac1,fac2)
            result.append(prod_fac)
        #sum out the final factor
        temp = sumout(result[0],current_hid_var)
        #print("factorList: ",factorList)
        factorList.append(temp)
    #multipy the rest of the factors in the list
    while len(factorList) > 1:
        fac3 = factorList.pop()
        fac4 = factorList.pop()
        new_fac = multiply(fac3,fac4)
        factorList.append(new_fac)
    #normaliaze the factor
    final_distribution = normalize(factorList[0])
    print("final distribution is: ",final_distribution)
    final_result = -1
    #find the final prob with queryVariables
    if final_distribution[0][0] == queryVariables[0][0]:
        i = 0
        while i < len(final_distribution):
            if final_distribution[1][i][0] == queryVariables[0][1]:
                final_result = final_distribution[1][i][-1]
            i += 1
    print("final_result: ",final_result)
    return final_distribution


#n is the length of the factor list(hard code this)
n = 6
#some initialization
fl = [[['E'],[[1,0.0003],[0,0.9997]]],
      [['B'],[[1,0.0001],[0,0.9999]]],
      [['R','E'],[[1,1,0.9],[1,0,0.0002],[0,1,0.1],[0,0,0.9998]]],
      [['W','A'],[[1,1,0.8],[1,0,0.4],[0,1,0.2],[0,0,0.6]]],
      [['A','B','E'],[[1,1,1,0.96],[1,1,0,0.95],[1,0,1,0.2],[1,0,0,0.01],
                         [0,1,1,0.04],[0,1,0,0.05],[0,0,1,0.8],[0,0,0,0.99]]],
      [['G','A'],[[1,1,0.4],[1,0,0.04],[0,1,0.6],[0,0,0.96]]]]
qv = [['B',1]]
olohv = ['B','E','R','A','W','G']
el = [['W',1],['G',1]]
#param_taker()
inference(fl,qv,olohv,el)
"""
#testing examples
factor = []
varlist = ['X','Y','Z']
data = [[1,1,1,0.1],[1,1,0,0.9],[1,0,1,0.2],[1,0,0,0.8],[0,1,1,0.4],[0,1,0,0.6],[0,0,1,0.3],[0,0,0,0.7]]
factor.append(varlist)
factor.append(data)
result = restrict(factor,'X',1)
print("restricted factor: ",result)
result = restrict(factor,'Z',0)
print("restricted factor: ",result)
result = restrict(factor,'Y',0)
print("restricted factor: ",result)

factor1 = [['A','B'],[[1,1,0.1],[1,0,0.9],[0,1,0.2],[0,0,0.8]]]
factor2 = [['B','C'],[[1,1,0.3],[1,0,0.7],[0,1,0.6],[0,0,0.4]]]
result = multiply(factor1,factor2)
print("product factor: ",result)

factor = [['A','B','C'],[[1,1,1,0.03],[1,1,0,0.07],[1,0,1,0.54],[1,0,0,0.36],[0,1,1,0.06],[0,1,0,0.14],[0,0,1,0.48],[0,0,0,0.32]]]
result = sumout(factor,'C')
print("summed out factor: ", result)

factor = [['B'],[[1,0.000030480091],[0,0.0190554223]]]
result = normalize(factor)
print("normalized factor: ",result)

factor = [['B','S'],[[1,1,0.6],[1,0,0.1],[0,1,0.4],[0,0,0.9]]]
result = sumout(factor,'B')
print("summed out factor: ",result)
"""