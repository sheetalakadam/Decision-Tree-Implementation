
# Date:04/12/2019
# Author: Sheetal Kadam(sak170006)


import numpy as np
import os
import graphviz
import math
import matplotlib.pyplot as plt  
from sklearn.metrics import confusion_matrix
from sklearn.tree import DecisionTreeClassifier # Import Decision Tree Classifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.ensemble import BaggingClassifier

def partition(x):
    """
    Partition the column vector x into subsets indexed by its unique values (v1, ... vk)

    Returns a dictionary of the form
    { v1: indices of x == v1,
      v2: indices of x == v2,
      ...
      vk: indices of x == vk }, where [v1, ... vk] are all the unique values in the vector z.
    """
    ans={}
    for value,key in enumerate(x):
        if(key not in ans):
            ans[key]=[value]
        else:
            ans[key].append(value)
    
    return ans
    raise Exception('Function not yet implemented!')
    
    
def entropy(y, w=None):
    """
    Compute the entropy of a vector y by considering the counts of the unique values (v1, ... vk), in z

    Returns the entropy of z: H(z) = p(z=v1) log2(p(z=v1)) + ... + p(z=vk) log2(p(z=vk))
    """
    
        
    entropy=0
  
    value_counts=partition(y) 
    
    for key,value in value_counts.items():
        temp=(w[value].sum()/w.sum())
        entropy=entropy + (-1*temp*(math.log(temp,2))) 
    
    return entropy
 
    
    raise Exception('Function not yet implemented!')


    
def mutual_information(x, y, w=None):
    
    """
    Compute the mutual information between a data column (x) and the labels (y). The data column is a single attribute
    over all the examples (n x 1). Mutual information is the difference between the entropy BEFORE the split set, and
    the weighted-average entropy of EACH possible split.

    Returns the mutual information: I(x, y) = H(y) - H(y | x)
    """
    
    partitionedx=partition(x)
    #total_count = len(x)
    
    
    entropyygivenx=0
    for key,value in partitionedx.items():
        
        probx=(w[value].sum()/w.sum())
      
        
        ytemp=[y[i] for i in value]
        wtemp=w[value]
        
        entropyygivenx=entropyygivenx+(probx*entropy(ytemp,wtemp))    
        
        
        
        
    return entropy(y,w)-entropyygivenx


    raise Exception('Function not yet implemented!')
    
def get_attribute_value_pairs(x):
    attribute_value_pairs=[]
    
    for index in range(x.shape[1]):
        unique_rows = set(x[:, index])
        
             
        for value in unique_rows:
            attribute_value_pairs.append((index,value))
    return (attribute_value_pairs)
            
            
def get_binary_vector(attribute_value_pair,x):
    return np.array(x[:,attribute_value_pair[0]]==attribute_value_pair[1]).astype('int')
      
   
  
def id3(x, y, attribute_value_pairs=None, depth=0, max_depth=5, w=None):
    """
    Implements the classical ID3 algorithm given training data (x), training labels (y) and an array of
    attribute-value pairs to consider. This is a recursive algorithm that depends on three termination conditions
        1. If the entire set of labels (y) is pure (all y = only 0 or only 1), then return that label
        2. If the set of attribute-value pairs is empty (there is nothing to split on), then return the most common
           value of y (majority label)
        3. If the max_depth is reached (pre-pruning bias), then return the most common value of y (majority label)
    Otherwise the algorithm selects the next best attribute-value pair using INFORMATION GAIN as the splitting criterion
    and partitions the data set based on the values of that attribute before the next recursive call to ID3.

    The tree we learn is a BINARY tree, which means that every node has only two branches. The splitting criterion has
    to be chosen from among all possible attribute-value pairs. That is, for a problem with two features/attributes x1
    (taking values a, b, c) and x2 (taking values d, e), the initial attribute value pair list is a list of all pairs of
    attributes with their corresponding values:
    [(x1, a),
     (x1, b),
     (x1, c),
     (x2, d),
     (x2, e)]
     If we select (x2, d) as the best attribute-value pair, then the new decision node becomes: [ (x2 == d)? ] and
     the attribute-value pair (x2, d) is removed from the list of attribute_value_pairs.

    The tree is stored as a nested dictionary, where each entry is of the form
                    (attribute_index, attribute_value, True/False): subtree
    * The (attribute_index, attribute_value) determines the splitting criterion of the current node. For example, (4, 2)
    indicates that we test if (x4 == 2) at the current node.
    * The subtree itself can be nested dictionary, or a single label (leaf node).
    * Leaf nodes are (majority) class labels

    Returns a decision tree represented as a nested dictionary, for example
    {(4, 1, False):
        {(0, 1, False):
            {(1, 1, False): 1,
             (1, 1, True): 0},
         (0, 1, True):
            {(1, 1, False): 0,
             (1, 1, True): 1}},
     (4, 1, True): 1}
    """
    
    # pruning condition 1 - entire set of labels is pure
    if (len(set(y))==1) or len(y)== 0:
        return y[0]
    
    if attribute_value_pairs is None:
        attribute_value_pairs=get_attribute_value_pairs(x)
    
    # pruning condition2 - attribute value pairs is empty or depth reached so choose majority
    
    if len(attribute_value_pairs)==0 or depth==max_depth:
        
        ylabel, freq = np.unique(y, return_counts=True)
        return ylabel[np.argmax(freq)]
    
    
        
    dt={} # node
    information_gain_lst=[mutual_information(get_binary_vector(attr_value,x),y,w) for attr_value in attribute_value_pairs]
    
    # get attribute with max gain
    max_gain_index=information_gain_lst.index(max(information_gain_lst))
    decision_index, decision_value = attribute_value_pairs[max_gain_index]

    
    decision_attr = np.array(x[:, decision_index] == decision_value).astype('int')
    split_decision_attr = partition(decision_attr)
    if len(split_decision_attr)>1:
        
    
        # create branches for tree
        false_indices = split_decision_attr[0]
        true_indices = split_decision_attr[1]
            
        x_right = x[false_indices, :]
        y_right = y[false_indices]
        
        x_left = x[true_indices, :]
        y_left = y[true_indices]
        
        
        w_left=w[true_indices]
        w_right=w[false_indices]
        
        attribute_value_pairs = np.delete(attribute_value_pairs, max_gain_index, 0)
       # del(attribute_value_pairs[max_gain_index])
        
        dt[(decision_index, decision_value, True)] = id3(x_left, y_left, attribute_value_pairs=attribute_value_pairs, max_depth=max_depth, depth=depth+1,w=w_left)
        dt[(decision_index, decision_value, False)] = id3(x_right, y_right, attribute_value_pairs=attribute_value_pairs, max_depth=max_depth, depth=depth+1,w=w_right)
    else:
         attribute_value_pairs = np.delete(attribute_value_pairs, max_gain_index, 0)
       
    return dt

      

    raise Exception('Function not yet implemented!')

def learning_curve(dataset):
    
    # Load the training data
    M = np.genfromtxt(('./'+dataset+'.train'), missing_values=0, skip_header=0, delimiter=',', dtype=int)
    ytrn = M[:, 0]
    Xtrn = M[:, 1:]

    # Load the test data
    M = np.genfromtxt(('./'+dataset+'.test'), missing_values=0, skip_header=0, delimiter=',', dtype=int)
    ytst = M[:, 0]
    Xtst = M[:, 1:]
    
    testerr={}
    trnerr={}
    for i in range(1,11):
        decision_tree = id3(Xtrn, ytrn, max_depth=i)
        y_pred = [predict_example(x, decision_tree) for x in Xtst]
        testerr[i] = compute_error(ytst, y_pred)
        y_pred = [predict_example(x, decision_tree) for x in Xtrn]
        trnerr[i] = compute_error(ytrn, y_pred)
            
    fig=plt.figure()
    fig.suptitle(dataset, fontsize=20)
    plt.plot(trnerr.keys(), trnerr.values(), marker='o', linewidth=3, markersize=12)
    plt.plot(testerr.keys(), testerr.values(), marker='s', linewidth=3, markersize=12)
    plt.xlabel('Depth of tree', fontsize=16)
    plt.ylabel('Train/Test error', fontsize=16)
    
    plt.legend(['Train Error', 'Test Error'], fontsize=16)
    
  
    


def predict_example1(x, tree):
    """
    Predicts the classification label for a single example x using tree by recursively descending the tree until
    a label/leaf node is reached.

    Returns the predicted label of x according to tree
    """

    # INSERT YOUR CODE HERE. NOTE: THIS IS A RECURSIVE FUNCTION.
    predicted_value=1
    
    for key, value in tree.items():
        if (x[key[0]]==key[1])==key[2]:
            if type(value) is dict: # subtree exists
                predicted_value=predict_example1(x,value)
            else:
                predicted_value=value #leaf node
                break
    return predicted_value
        
    raise Exception('Function not yet implemented!')


def compute_error(y_true, y_pred, w=None):
    """
    Computes the average error between the true labels (y_true) and the predicted labels (y_pred)

    Returns the error = (1/n) * sum(y_true != y_pred)
    """
    if w is None:
        
        n=len(y_true)
    
        return ((1/n) * (sum([i!=j for i,j in zip(y_true,y_pred)])))
    
    else:
        t=(np.array(y_true)!=np.array(y_pred))==False
       
        indices=[i for i, x in enumerate(t) if x]
        wtemp=w[indices]
        return ((1/w.sum()) * (wtemp.sum()))
    
    raise Exception('Function not yet implemented!')


def pretty_print(tree, depth=0):
    """
    Pretty prints the decision tree to the console. Use print(tree) to print the raw nested dictionary representation
    DO NOT MODIFY THIS FUNCTION!
    """
    if depth == 0:
        print('TREE')

    for index, split_criterion in enumerate(tree):
        sub_trees = tree[split_criterion]

        # Print the current node: split criterion
        print('|\t' * depth, end='')
        print('+-- [SPLIT: x{0} = {1} {2}]'.format(split_criterion[0], split_criterion[1], split_criterion[2]))

        # Print the children
        if type(sub_trees) is dict:
            pretty_print(sub_trees, depth + 1)
        else:
            print('|\t' * (depth + 1), end='')
            print('+-- [LABEL = {0}]'.format(sub_trees))


def render_dot_file(dot_string, save_file, image_format='png'):
    """
    Uses GraphViz to render a dot file. The dot file can be generated using
        * sklearn.tree.export_graphviz()' for decision trees produced by scikit-learn
        * to_graphviz() (function is in this file) for decision trees produced by  your code.
    DO NOT MODIFY THIS FUNCTION!
    """
    if type(dot_string).__name__ != 'str':
        raise TypeError('visualize() requires a string representation of a decision tree.\nUse tree.export_graphviz()'
                        'for decision trees produced by scikit-learn and to_graphviz() for decision trees produced by'
                        'your code.\n')

    # Set path to your GraphViz executable here
    os.environ["PATH"] += os.pathsep + 'C:/Program Files (x86)/Graphviz2.38/bin/'
    graph = graphviz.Source(dot_string)
    graph.format = image_format
    graph.render(save_file, view=True)


def to_graphviz(tree, dot_string='', uid=-1, depth=0):
    """
    Converts a tree to DOT format for use with visualize/GraphViz
    DO NOT MODIFY THIS FUNCTION!
    """

    uid += 1       # Running index of node ids across recursion
    node_id = uid  # Node id of this node

    if depth == 0:
        dot_string += 'digraph TREE {\n'

    for split_criterion in tree:
        sub_trees = tree[split_criterion]
        attribute_index = split_criterion[0]
        attribute_value = split_criterion[1]
        split_decision = split_criterion[2]

        if not split_decision:
            # Alphabetically, False comes first
            dot_string += '    node{0} [label="x{1} = {2}?"];\n'.format(node_id, attribute_index, attribute_value)

        if type(sub_trees) is dict:
            if not split_decision:
                dot_string, right_child, uid = to_graphviz(sub_trees, dot_string=dot_string, uid=uid, depth=depth + 1)
                dot_string += '    node{0} -> node{1} [label="False"];\n'.format(node_id, right_child)
            else:
                dot_string, left_child, uid = to_graphviz(sub_trees, dot_string=dot_string, uid=uid, depth=depth + 1)
                dot_string += '    node{0} -> node{1} [label="True"];\n'.format(node_id, left_child)

        else:
            uid += 1
            dot_string += '    node{0} [label="y = {1}"];\n'.format(uid, sub_trees)
            if not split_decision:
                dot_string += '    node{0} -> node{1} [label="False"];\n'.format(node_id, uid)
            else:
                dot_string += '    node{0} -> node{1} [label="True"];\n'.format(node_id, uid)

    if depth == 0:
        dot_string += '}\n'
        return dot_string
    else:
        return dot_string, node_id, uid
    
    

    
def bagging_predict(x,ft):
    fbag=[predict_example1(x,tree) for tree in ft]
    return max(set(fbag), key=fbag.count)
    

def bagging(x, y, max_depth, num_trees):
    ft=[]
    for i in range(0,num_trees):
        idx=np.random.choice(x.shape[0],x.shape[0])
        x_boot= x[idx,:]
        y_boot=y[idx]
        
        ft.append(id3(x_boot, y_boot, max_depth=max_depth,w=np.ones(len(y_boot))))
        
    return ft

# helper functions for boosting

def initiaize_weights(total):
    return np.ones(total)/total
    
def choose_alpha(error):
   
    return (np.log((1-error)/error))/2

def get_err(D,misclassified):
    
    return np.sum(misclassified*D)/np.sum(D)

def update_weights(D_old,alpha,y_pred,y):
    
    t= (D_old*np.exp(-alpha* y*y_pred))
    return t/np.sum(t)

def boosting(x, y, max_depth, num_stumps):
    # initialize weights
    D={}
    D[0]= initiaize_weights(len(y))
    h_ens=[]
  
    
    for i in range(num_stumps):
        hi=id3(x,y,max_depth=max_depth,w=D[i])
        y_pred= [predict_example1(xi, hi) for xi in x]
       # misclassified=~np.equal(y_pred,y)
        #ei=get_err(D[i],misclassified)
        ei=compute_error(y,y_pred,D[i])
       
        if ei>0.5:
            y_pred=1-np.array(y_pred)
            ei=1-ei
            #misclassified=~np.equal(y_pred,y)
            
        alphai=choose_alpha(ei)
        D[i+1]=update_weights(D[i],alphai,y_pred,y)
        h_ens.append((alphai,hi))
  
    return h_ens

def predict_example(x, h_ens):
    """ where h_ens is an ensemble of weighted hypotheses. The ensemble is
represented as an array of pairs [(alpha_i, h_i)], where each hypothesis and weight are represented
by the pair: (alpha_i, h_i).    
    
   
 res=0
        totalalpha=0
        for h in h_ens:
            totalalpha=totalalpha+h[0]
            res=res + (h[0]*predict_example1(x,h[1]))
        
        if (res/totalalpha)>0.5:
            return 1
        else:
            return 0
    prediction={}
    for h in h_ens:
       
        p=predict_example1(x,h[0])
        if p not in prediction:
            prediction[p]=h[1]
        else:
            prediction[p]=prediction[p]+ h[1]
            
    return max(prediction.items(), key= lambda x: x[1])[0]
    """
    if type(h_ens[0]) is tuple:
            
        prediction={}
        totalalpha=0
        for h in h_ens:
           
            p=predict_example1(x,h[1])
            totalalpha=totalalpha+h[0]
            if p not in prediction:
                prediction[p]=h[0]
            else:
                prediction[p]=prediction[p]+ h[0]
        
        return max(prediction.items(), key= lambda x: x[1])[0]
        
       
    else:
        return bagging_predict(x,h_ens)
        
    raise Exception('Function not yet implemented!')
        


if __name__ == '__main__':
     # Load the training data
    M = np.genfromtxt('./mushroom.train', missing_values=0, skip_header=0, delimiter=',', dtype=int)
    ytrn = M[:, 0]
    Xtrn = M[:, 1:]

    # Load the test data
    M = np.genfromtxt('./mushroom.test', missing_values=0, skip_header=0, delimiter=',', dtype=int)
    ytst = M[:, 0]
    Xtst = M[:, 1:]
    
        #a. Bagging
    d=[3,5]
    bag_size=[5,10]
    print('Bagging experiments:')
    for depth in d:
        for num_trees in bag_size:
            print('With max_depth ',depth,' and bag size ',num_trees )
            temp=bagging(Xtrn,ytrn,depth, num_trees)
            yp=[predict_example(x, temp) for x in Xtst]
            tst_err = compute_error(ytst, yp)
            print(confusion_matrix(ytst,yp))
            print('Test Error = {0:4.2f}%.'.format(tst_err * 100))                   
    
    
    #b. Boosting
    d=[1,2]
    ensemble_size=[5,10]
    print('Boosting experiments:')
    for depth in d:
        for k in ensemble_size:
            print('With max_depth ',depth,' ensemble size ',k )
            temp=boosting(Xtrn,ytrn,depth, k)
            yp=[predict_example(x, temp) for x in Xtst]
            tst_err = compute_error(ytst, yp)
            print(confusion_matrix(ytst,yp))
            print('Test Error = {0:4.2f}%.'.format(tst_err * 100))                       
    

# Scikit Cimparison
            
   
 
    for j in [3,5]:
        
        
        clf_stump=DecisionTreeClassifier(max_depth=j)
        print(j)
        for i in [5,10]:
            
            baglfy=BaggingClassifier(base_estimator=clf_stump,n_estimators=i)
            baglfy=baglfy.fit(Xtrn,ytrn)
            #bag_tr_err=y==baglfy.predict(x)
            y_pred = baglfy.predict(Xtst)
            print(confusion_matrix(ytst,y_pred))
            print('Test Error = {0:4.2f}%.'.format(tst_err * 100)) 
    
    for j in [1,2]:
        
        
        clf_stump=DecisionTreeClassifier(max_depth=j)
        print(j)
        for i in [5,10]:
            
            bstlfy=AdaBoostClassifier(base_estimator=clf_stump,n_estimators=i)
            bstlfy=bstlfy.fit(Xtrn,ytrn)
            #bag_tr_err=y==baglfy.predict(x)
            y_pred = bstlfy.predict(Xtst)
            print(confusion_matrix(ytst,y_pred))
    
    #temp=bagging(Xtrn,ytrn,3,3)
    #yp=[bagging_predict(x, temp) for x in Xtst]
    #tst_err = compute_error(ytst, yp)
   
    #temp=boosting(Xtrn,ytrn,1,5)
    
   # yp=[predict_example(x, temp) for x in Xtst]
   # tst_err = compute_error(ytst, yp)
    
    
    #print(confusion_matrix(ytst,yp))
    
    
    
    #print('Test Error = {0:4.2f}%.'.format(tst_err * 100))
    
    
    

   

    
    
   
    
