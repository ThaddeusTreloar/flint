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

def predict()