import shap
import numpy as np
import operator

class shaply():
    def __init__(self,model):
        self.model=model


    def get_shap_values(self,arr,columns):
        positive={}
        negative={}
        explainer=shap.TreeExplainer(self.model)
        shap_values = explainer(arr).values[0]
        print(shap_values)
        for name,value in zip(columns,shap_values):
            if value>0:
                positive[name]=value
            else:
                negative[name]=value
        sorted_positive =sorted(positive.items(),key=operator.itemgetter(1),reverse=True)
        sorted_positive=dict(sorted_positive)
        print(sorted_positive)
        return sorted_positive,negative




