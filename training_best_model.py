from training import training_models
import pickle
from application_logging import logger


class Training_best_model:
    def __init__(self):
        self.log_writer = logger.App_Logger()
        self.file_object = open('logs/processing.txt', 'a+')
        self.log_writer.log(self.file_object,"Entering Training_best_model class of training best model file")

    def model_finder(self,x_train,x_test,y_train,y_test):
        try:

            trainer=training_models.Training(self.file_object,self.log_writer)

            name,best_model=trainer.get_best_model(x_train,x_test,y_train,y_test)

            with open('Models/best_model.pickle', 'wb') as file:
                pickle.dump(best_model,file)

            self.log_writer.log(self.file_object,"Best model is " + name)
        except Exception as e:
            self.log_writer.log(self.file_object,'Exception occured at model finder method:' + str(e))
            raise Exception()


