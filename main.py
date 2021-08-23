from cleaning import Preprocessing
from training_best_model import Training_best_model
def training():
    try:
        train=Preprocessing()
        x_train,x_test,y_train,y_test=train.cleaning_data()
        """We get our feature and target cleaned data"""
        best=Training_best_model()
        "Just to see how are training data looks"
        x_train.to_csv('data_files/x_train.csv',index=False)
        best.model_finder(x_train,x_test,y_train,y_test)



    except Exception:
        raise Exception
if __name__=='__main__':
    training()


