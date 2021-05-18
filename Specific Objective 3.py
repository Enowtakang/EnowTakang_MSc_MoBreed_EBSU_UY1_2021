import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn import preprocessing


def predict_ttp():
    files = ['1.xlsx', '2.xlsx', '3.xlsx', '4.xlsx', '5.xlsx',
             '6.xlsx', '7.xlsx', '8.xlsx', '9.xlsx', '10.xlsx',
             '11.xlsx', '12.xlsx', '13.xlsx', '14.xlsx', '15.xlsx',
             '16.xlsx', '17.xlsx', '18.xlsx', '19.xlsx', '20.xlsx']

    for file in files:

        # define the data path
        data_path = f'C:/Python Projects/Specific Objective 3/{file}'

        # Read the dataset with pandas
        dataset = pd.read_excel(data_path)

        # Create an array with the dataset values
        array = dataset.values

        """
        Scaling the array
        """

        scaler = preprocessing.StandardScaler().fit(array)

        # print(scaler)

        array_scaled = scaler.transform(array)

        # print(array_scaled)

        X = array_scaled[:, 1:5]

        y = array_scaled[:, 0]

        """
        Create an instance of the model, 
        then use it for prediction.
        """

        model = LinearRegression()

        model.fit(X, y)

        Xnew = [[10, 10, 10, 8]]

        ynew = model.predict(Xnew)

        print("X=%s, Predicted=%s" % (Xnew[0], ynew[0]))


predict_ttp()
