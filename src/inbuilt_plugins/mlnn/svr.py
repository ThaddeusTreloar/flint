'''
Flint: free and open ML/NN financial forecasting software
Copyright (C) 2021 Thaddeus Treloar

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see https://www.gnu.org/licenses/gpl-3.0.txt.
'''


import numpy as np

from sklearn.svm import SVR
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

def train(ticker_data, settings):
    
    y = np.array(ticker_data["eod"][settings.INST_RANGE:])
    x = np.array([x for x in zip(ticker_data["eod"][settings.INST_RANGE-1:settings.INST_RANGE+settings.INTERVAL_RANGE], ticker_data["sma"])])

    print(y.size)

    regression = make_pipeline(StandardScaler(), SVR(C=1, epsilon=0.01, kernel="linear"))

    regression.fit(x, y)

    predictions = []
    rolling_close = ticker_data["eod"][settings.INST_RANGE:]
    sma_rolling_list  = ticker_data["eod"][settings.INST_RANGE:] 
    
    
    for i in range(settings.PREDICT_RANGE): 
        prev_close = rolling_close[-1]
        prev_sma   = functools.reduce(lambda a, b: a+b, sma_rolling_list)/10
        predictions.append(round(regression.predict(np.array([[y[-1], prev_sma]]))[0], 3))
        rolling_close.append(predictions[-1])
        del sma_rolling_list[0]
        sma_rolling_list.append(predictions[-1])
    
    print(predictions)
    print(ticker_data["test-data"])

    #regression.predict(np.array([[y[-1], sma_quick]])))
    #print(ticker_data["test-data"][0])
    #print(regression.score(np.array([[y[-1], sma_quick]]), np.array([ticker_data["test-data"][0]])))

def predict():
    pass