# Reddit Flair Prediction

This project is made to predict the flair of a reddit submission on the [India sub-reddit](https://www.reddit.com/r/india/). Each sub-reddit has flairs associated to it which are like categories of the different types of submissions. Flairs to a post are added by the User posting and hence every post does not necessarily have an associated flair. The India sub-reddit has 10 extremely popular flairs that we will be predicting from. They are:
1. Non-Political         
2. Politics              
3. Policy/Economy        
4. AskIndia              
5. Science/Technology     
6. Business/Finance       
7. Reddiquette          
8. Sports               
9. Photography          
10. Coronavirus

The project is divided into four parts:
1. Data Collection
2. Exploratory data analysis of data collected
3. Training models for flair predictor
4. Deploying best model as a Django web-app

### [Data Collection](https://github.com/saum7800/reddit-flair-prediction/blob/master/1reddit%20data%20collection.ipynb)

I have described how I have procured the dataset in this [notebook](https://nbviewer.jupyter.org/github/saum7800/reddit-flair-prediction/blob/master/1reddit%20data%20collection.ipynb). If you are running this notebook on your loca machine, make sure you **do not** run the last cell as it will overwrite the dataset present with newer data which may not work properly with the subsequent notebooks.


### [Exploratory Data Analysis](https://github.com/saum7800/reddit-flair-prediction/blob/master/2reddit%20exploratory%20data%20analysis.ipynb)

After procuring the large dataset from part 1, we will clean up and explore the new dataset to find interesting nuances that we may not have expected and also reaffirm some expected outcomes. The notebook contains interactive plots in the result and is hence best viewed on nbviewer [here](https://nbviewer.jupyter.org/github/saum7800/reddit-flair-prediction/blob/master/2reddit%20exploratory%20data%20analysis.ipynb).

### Flair Predictor Models

The problem at hand is a multi-class text-classification problem. I made a 70-30 train-test split to the dataset consisting of 100000+ reddit submissions. The following are the results from the various algortihms explored in decreasing order of accuracy:

| Algorithm/Model             | Accuracy |
|-----------------------------|----------|
| Pre-trained Distil-BERT     | 67%      |
| LSTM Deep Network           | 62%      |
| Logistic Regression         | 62%      |
| Complement Naive Bayes      | 61%      |
| Linear SVM                  | 61%      |
| Multinomial Naive Bayes     | 60%      |
| Pre-trained gnews embedding | 59%      |
| FeedForward Deep Network    | 58%      |
| Random Forest Classifier    | 57%      |
| Nearest Centroid            | 48%      |

Clearly, Google's state-of-the-art Language Model [BERT](https://github.com/google-research/bert) outperforms the remaining models. It is interesting, however, to notice that simple Probabilistic Classifiers such as Naive Bayes are performing better than deep neural networks. Here is the Classification Report for the trained DistilBERT model on the test set.

| Flair              | Precision | Recall | F1   | Support |
|--------------------|-----------|--------|------|---------|
| AskIndia           | 0.72      | 0.80   | 0.76 | 3810    |
| Business/Finance   | 0.47      | 0.41   | 0.44 | 1385    |
| Coronavirus        | 0.59      | 0.64   | 0.61 | 280     |
| Non-Political      | 0.66      | 0.68   | 0.67 | 10242   |
| Photography        | 0.66      | 0.41   | 0.50 | 328     |
| Policy/Economy     | 0.57      | 0.60   | 0.59 | 3894    |
| Politics           | 0.74      | 0.76   | 0.75 | 9075    |
| Science/Technology | 0.50      | 0.47   | 0.49 | 1360    |
| Sports             | 0.75      | 0.74   | 0.75 | 468     |
| Reddiquette        | 0.67      | 0.18   | 0.29 | 965     |
|                    |           |        |      |         |
| accuracy           |           |        | 0.67 | 31807   |


### Django Application

Through the [Django web application](http://34.87.119.42/), you can input a link of the reddit post to the website and get basic information regarding the post along with the predicted Flair. To set up the website on your LocalHost follow these steps:

1. Clone this repository and cd to ```reddit-flair-prediction/4web_app/predict```
2. Download distilbert_predictor_final and distilbert_predictor_final.preproc from [here](https://drive.google.com/open?id=1qv4zsncDvFt07-uIIGCbNVZMWp-GUIQM) and extract it to current folder
3. make a virual environment 
4. cd to ```reddit-flair-prediction/4web_app/```
5. install the dependencies of the web app with ```pip install -r requirements.txt```  
6. run the server with ```python manage.py runserver``` and open the link that comes in the terminal

### Automated Testing

If you wish to test the accuracy of the model on your own dataset, you can submit a POST request to the automated testing endpoint with a .txt file containing a link to the post on every line. In return, you will get a JSON response containing keys as your submitted links and values to be the predicted flairs. You may upload a file to [http://34.87.119.42/automated_testing/](http://34.87.119.42/automated_testing/) or directly submit a POST request with a python script such as:

```python
import requests
url = 'http://34.87.119.42/automated_testing/'
files = {'upload_file': open('<YOUR TEXT FILE>.txt','rb')}
r = requests.post(url, files=files)
pred = r.json()
print(pred["<LINK FROM TEXT FILE>"])
```
