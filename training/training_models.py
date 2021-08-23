from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import GridSearchCV
from sklearn.metrics  import r2_score
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
class Training:
    def __init__(self,file_object,logger_object):
        self.file_object=file_object
        self.logger_object=logger_object
        self.linearReg = LinearRegression()
        self.RandomForestReg = RandomForestRegressor()
        self.GradientBoost=GradientBoostingRegressor()
        self.logger_object.log(self.file_object,"Entered training mode!!Finding best model")

    def finding_best_params_for_random_forest(self,x_train,y_train):
        """
        Hyperparameters for Random Forest
        """
        self.logger_object.log(self.file_object,
                               'Entered the RandomForestReg method of the Model_Finder class')
        try:
            # initializing with different combination of parameters
            self.param_grid_Random_forest_Tree = {
                "n_estimators": [10, 20, 30],
                "max_features": ["auto", "sqrt", "log2"],
                "min_samples_split": [2, 4, 8],
                "bootstrap": [True, False]
            }

            # Creating an object of the Grid Search class
            self.grid = GridSearchCV(self.RandomForestReg, self.param_grid_Random_forest_Tree, verbose=3, cv=5)
            # finding the best parameters
            self.grid.fit(x_train,y_train)

            # extracting the best parameters
            self.n_estimators = self.grid.best_params_['n_estimators']
            self.max_features = self.grid.best_params_['max_features']
            self.min_samples_split = self.grid.best_params_['min_samples_split']
            self.bootstrap = self.grid.best_params_['bootstrap']

            # creating a new model with the best parameters
            self.decisionTreeReg = RandomForestRegressor(n_estimators=self.n_estimators, max_features=self.max_features,
                                                         min_samples_split=self.min_samples_split,
                                                         bootstrap=self.bootstrap)
            # training the mew models
            self.decisionTreeReg.fit(x_train,y_train)
            self.logger_object.log(self.file_object,
                                   'RandomForestReg best params: ' + str(
                                       self.grid.best_params_) + '. Exited the RandomForestReg method of the Model_Finder class')
            return self.decisionTreeReg
        except Exception as e:
            self.logger_object.log(self.file_object,
                                   'Exception occured in RandomForestReg method of the Model_Finder class. Exception message:  ' + str(
                                       e))
            self.logger_object.log(self.file_object,
                                   'RandomForestReg Parameter tuning  failed. Exited the knn method of the Model_Finder class')
            raise Exception()

    def get_best_params_for_linearReg(self,x_train,y_train):

        """Hyperparameters for Linear Reg
                                """
        self.logger_object.log(self.file_object,
                               'Entered the get_best_params_for_linearReg method of the Model_Finder class')
        try:
            # initializing with different combination of parameters
            self.param_grid_linearReg = {
                'fit_intercept': [True, False], 'normalize': [True, False], 'copy_X': [True, False]

            }
            # Creating an object of the Grid Search class
            self.grid = GridSearchCV(self.linearReg, self.param_grid_linearReg, verbose=3, cv=5)
            # finding the best parameters
            self.grid.fit(x_train,y_train)

            # extracting the best parameters
            self.fit_intercept = self.grid.best_params_['fit_intercept']
            self.normalize = self.grid.best_params_['normalize']
            self.copy_X = self.grid.best_params_['copy_X']

            # creating a new model with the best parameters
            self.linReg = LinearRegression(fit_intercept=self.fit_intercept, normalize=self.normalize,
                                           copy_X=self.copy_X)
            # training the mew model
            self.linReg.fit(x_train,y_train)
            self.logger_object.log(self.file_object,
                                   'LinearRegression best params: ' + str(
                                       self.grid.best_params_) + '. Exited the get_best_params_for_linearReg method of the Model_Finder class')
            return self.linReg
        except Exception as e:
            self.logger_object.log(self.file_object,
                                   'Exception occured in get_best_params_for_linearReg method of the Model_Finder class. Exception message:  ' + str(
                                       e))
            self.logger_object.log(self.file_object,
                                   'LinearReg Parameter tuning  failed. Exited the get_best_params_for_linearReg method of the Model_Finder class')
            raise Exception()
    def finding_best_params_for_gradient_boost(self,x_train,y_train):
        """
        Hyperparameters for Gradient Boost
        """
        self.logger_object.log(self.file_object,
                               'Entered the Gradient Boost method of the Model_Finder class')
        try:
            # initializing with different combination of parameters
            self.param_grid_Gradient_Boost = {
                "n_estimators": [10, 20, 30],
                "max_features": ["auto", "sqrt", "log2"],
                "min_samples_split": [2, 4, 8],
                "max_depth": [2,4,6,10]
            }

            # Creating an object of the Grid Search class
            self.grid = GridSearchCV(self.GradientBoost, self.param_grid_Gradient_Boost, verbose=3, cv=5)
            # finding the best parameters
            self.grid.fit(x_train,y_train)

            # extracting the best parameters
            self.n_estimators = self.grid.best_params_['n_estimators']
            self.max_features = self.grid.best_params_['max_features']
            self.min_samples_split = self.grid.best_params_['min_samples_split']
            self.max_depth = self.grid.best_params_['max_depth']

            # creating a new model with the best parameters
            self.GBR = GradientBoostingRegressor(n_estimators=self.n_estimators, max_features=self.max_features,
                                                         min_samples_split=self.min_samples_split,
                                                         max_depth=self.max_depth)
            # training the mew models
            self.GBR.fit(x_train,y_train)
            self.logger_object.log(self.file_object,
                                   'Gradient Boosted best params: ' + str(
                                       self.grid.best_params_) + '. Exited the Gradient boost method of the Model_Finder class')
            return self.decisionTreeReg
        except Exception as e:
            self.logger_object.log(self.file_object,
                                   'Exception occured in Gradient Boost method of the Model_Finder class. Exception message:  ' + str(e))
            raise Exception()

    def get_best_model(self, x_train,x_test,y_train, y_test):
        """Get best model"""

        self.logger_object.log(self.file_object,
                               'Entered the get_best_model method of the Model_Finder class')
        # create best model for Linear Regression
        try:

            self.LinearReg = self.get_best_params_for_linearReg(x_train,y_train)
            self.prediction_LinearReg = self.LinearReg.predict(x_test)  # Predictions using the LinearReg Model
            self.LinearReg_error = r2_score(y_test, self.prediction_LinearReg)

            # create best model for random
            self.randomForestReg = self.finding_best_params_for_random_forest(x_train,y_train)
            self.prediction_randomForestReg = self.randomForestReg.predict(
                x_test)  # Predictions using the randomForestReg Model
            self.prediction_randomForestReg_error = r2_score(y_test, self.prediction_randomForestReg)

            self.GradientBoost=self.finding_best_params_for_gradient_boost(x_train,y_train)
            self.prediction_gbr=self.GradientBoost.predict(x_test)
            self.gbr_error=r2_score(y_test,self.prediction_gbr)


            # comparing three models
            if self.gbr_error >self.LinearReg_error  and self.gbr_error >= self.prediction_randomForestReg_error:
                return 'Gradient Boosted',self.GradientBoost
            elif self.prediction_randomForestReg_error >= self.gbr_error and self.prediction_randomForestReg_error >= self.LinearReg_error:
                return 'Random Forest',self.randomForestReg
            else:
                return 'Linear Regression',self.LinearReg
        except Exception as e:
            self.logger_object.log(self.file_object,
                                   'Exception occured in get_best_model method of the Model_Finder class. Exception message:  ' + str(e))
            self.logger_object.log(self.file_object,
                                   'Model Selection Failed. Exited the get_best_model method of the Model_Finder class')
            raise Exception()