# Natural Language Processing Progrm in Python to Explore Text


A python program to explore text using NLTK and NER library 

Prerequisite

1) Stanford Named Entity Recognizer server

  i)   The server could be downloaded from [here](http://nlp.stanford.edu/software/stanford-ner-2012-11-11.zip)  
  ii)  The server can be run using the following command -
```
java -mx1000m -cp stanford-ner.jar edu.stanford.nlp.ie.NERServer -loadClassifier
classifiers/english.muc.7class.distsim.crf.ser.gz -port 8080 -outputFormat inlineXML  
```
> Note : The port number by default is set as 8080 which is used by NER api to connect to the server. Server should be started before running the program.

2) wxPython to be installed for UI

To run the program 
```
python ExploreText.py 
```
