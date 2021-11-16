from datetime import time
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from statistics import mean
import matplotlib.pyplot as plt
import sklearn
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
import datetime
import statsmodels.api as sm
from sklearn.model_selection import train_test_split, cross_val_score, KFold
from scipy import stats
import random


def read_data(path):
    data = pd.read_excel(path, parse_dates= ['Time'])
    return data
def model(data):
    
    Q1, Q2= data.quantile([0.10, 0.90])['Time']
    data = data[((data['Time'] >= Q1) & (data['Time'] <= Q2))]
    X = np.array(data['Time']).reshape(-1, 1)
        
    y = np.array(data['Score'])
    # створення моделі лінійної регресії
    linear = LinearRegression()
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.8)
    linear.fit(X_train, y_train)

    plt.scatter(X_test, y_test)
    plt.plot(X_test, linear.predict(X_test), color='r')
    

    record_new_data(data, X_test, linear.predict(X_test))
    
    plt.title("Линейная регрессия")
    plt.xlabel('Время с')
    plt.ylabel('Количество очков')
    plt.show()
def record_new_data(data,time,pred):
    a = data['Algorithm']
    for i in range(0,5):
        temp = random.randint(1,len(pred)-1)
        if pred[temp] >250:
            cond = 'Win'
        else:
            cond = 'Lose'
        data1 = a[0]+";" +cond+";"+ str(time[temp][0]) +";"+str(round(pred[temp])) +"\n"
        print(data1)
        f = open(r"C:\Users\13010\OneDrive\Рабочий стол\КПИ\Inteligent sistems\AI_Basics_Lab\AI_Basics_Lab4\dataHistory5.CSV", 'a')
        f.write(data1)
        f.close()

def corelation(data):   
    res = stats.spearmanr(data["Time"],data["Score"]  )
    print('Коефіцієнт кореляції Спірмена: ',res[0]) 

def main():
   
    data = pd.read_csv(r"C:\Users\13010\OneDrive\Рабочий стол\КПИ\Inteligent sistems\AI_Basics_Lab\AI_Basics_Lab4\dataHistory5.CSV", delimiter= ';')
    
    #print(data)
    #data.info()
    
    model(data)
    #corelation(data)

if __name__ == "__main__":
    main()