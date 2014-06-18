twittersentiment
================

### Installation
Alle erforderlichen Python Libraries installieren mit PIP:

```
$ pip install -r requirements.txt
```

Twitter Korpus von sentiment140.com downloaden und im Projektverzeichnis entpacken.
auf der commandline split ausführen "split -l 100000 $TWITTERCORPUS$ csvdata/split" :
[http://cs.stanford.edu/people/alecmgo/trainingandtestdata.zip]

### Ausführen
Die Klassifizierer trainieren mit
```
$ python trainer.py me
```
```
$ python trainer.py -h
usage: trainer.py [-h] {nb,me}

Train and save classifier model.

positional arguments:
  {nb,me}     choose between nb=NaiveBayes, me=MaxEnt
```

Das Hauptprogramm ausführen mit
```
$ cd twittersentiment
$ python main.py
```

Den NaiveBayes vs. MaxEnt Vergleich plotten:
```
$ python comparison.py step size
```
Der resultierende Plott wird im unterordner `./plots/` gespeichert.
