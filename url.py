import pandas as pd #for data frames
import numpy as np  #for array manipulation
import random      
from tkinter import *    #constructing gui
from tkinter import messagebox
import pandas
# Machine Learning Packages
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
# Load Url Data 
urls_data = pd.read_csv("/home/munish/Desktop/urldata.csv")
type(urls_data)
#creating our tokenizer
urls_data.head()
def makeTokens(f):
    tkns_BySlash = str(f.encode('utf-8')).split('/')	# make tokens after splitting by slash
    total_Tokens = []
    for i in tkns_BySlash:
        tokens = str(i).split('-')	# make tokens after splitting by dash
        tkns_ByDot = []
        for j in range(0,len(tokens)):
            temp_Tokens = str(tokens[j]).split('.')	# make tokens after splitting by dot
            tkns_ByDot = tkns_ByDot + temp_Tokens
        total_Tokens = total_Tokens + tokens + tkns_ByDot
    total_Tokens = list(set(total_Tokens))	#remove redundant tokens
    if 'com' in total_Tokens:
        total_Tokens.remove('com')	#removing .com since it occurs a lot of times and it should not be included in our features
    return total_Tokens
# Labels
y = urls_data["label"]
# Features
url_list = urls_data["url"]

# Using Designed Tokenizer
vectorizer = TfidfVectorizer(tokenizer=makeTokens)
#Store vectors into X variable as Our XFeatures
X = vectorizer.fit_transform(url_list)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
# Model Building
#using logistic regression
logit = LogisticRegression()	
logit.fit(X_train, y_train)
# Accuracy of Our Model
print("Accuracy ",logit.score(X_test, y_test))

#PREDICTION OF MODEL

# Model Building
#logit = LogisticRegression()	#using logistic regression
#logit.fit(X_train, y_train)
# Accuracy of Our Model with our Custom Token
#print("Accuracy ",logit.score(X_test, y_test))


#working on GUI
root = Tk()
root.title("URL-CHECK MASTER")  #setting the title of gui
frame = Frame(root)
frame.pack()
bottomframe = Frame(root)
bottomframe.pack( side = BOTTOM )
L1 = Label(frame, text="Enter the URL: ")
L1.pack( side = LEFT)
E1 = Entry(frame,bd =5, width=150)
E1.pack(side = RIGHT)
def helloCallBack():
	url = [0]
	url[0]=E1.get() 
	url=vectorizer.transform(url)
	newurl = logit.predict(url)
	if newurl=='good':
		messagebox.showinfo( "BENIGN URL")
	elif newurl=='bad':
		messagebox.showinfo( "MALICIOUS URL")
B = Button(bottomframe, text ="SUBMIT", command = helloCallBack)
B.pack()
root.mainloop()