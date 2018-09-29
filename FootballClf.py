import pickle
import csv
import os
import datetime

class FootballClf():

    def __init__(self):
        self._clfs_dir = 'clfs'
        self._indexfile = 'index.csv'
        
    def save(self, clf, clf_name, version, comment, filename, colnames):
        full_filename=filename + '.' + type(clf).__name__
        outfile = open(os.path.join ('.', self._clfs_dir, full_filename),'wb')
        pickle.dump(clf,outfile)
        outfile.close()

        with open(os.path.join(self._clfs_dir, self._indexfile), 'a') as csvfile:
            fieldnames = ['date', 'clf_name', 'version', 'comment', 'filename', 'colnames']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            now_stamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            writer.writerow({'date': now_stamp, 'clf_name': clf_name, 'version' : version, 'comment' : comment, 
                             'filename' : full_filename, 'colnames':colnames})
        csvfile.close()

    def load_by_name(self, clf_name):

        filename=None
        clf = None
        with open('clfs/index.csv') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row['clf_name']==clf_name:
                    filename = row['filename']
            csvfile.close()

        if filename is not None:
            infile = open('clfs'  + '/' + filename,'rb')
            clf = pickle.load(infile)
            infile.close()
            return clf