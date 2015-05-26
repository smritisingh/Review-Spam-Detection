# Review-Spam-Detection

## This project works on detection of Online spam reviews.

#### Our dataset is taken from Non-spam hotel reviews by TripAdvisor and Spam reviews by Amazon Mechanical Turk.

* DatabaseCreator.py : Database Creation
* HotelReview.db : SQLite database of the hotel Reviews 
* features.py : Linguistic and POS features generator
* SentimentScorer.py : Calculation of aspect-based sentiment score of a review text as a feature
* pca.py : feature vector dimentionality reducer
* major.py : Creation of Training and Test dataset as well as feature vector creator
* machinlearnpca.py : Naive Bayes, SVM and Decision Tree classifiers along with accuracy, confusion matrix, recall, precision and f1score calculation
* Unigram.py : unigram Spam hit score and non-spam hit score calculation
