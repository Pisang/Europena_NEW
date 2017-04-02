import csv
from os import path
from random import shuffle

import numpy

import gensim.models.doc2vec
from sklearn.linear_model import LogisticRegression


class Doc2vec_clustering:

    featuresize = 100

    def build_Model(self, path_to_files):
        sentences = LabeledLineSentence_v2(
            filename=path.join(path_to_files, 'metadata_translation_v2_groundtruth_dense.csv'))

        model = gensim.models.doc2vec.Doc2Vec(min_count=1, window=40, size=self.featuresize, negative=2, workers=4)
        train_sent_array = sentences.to_array().__getitem__(0)

        model.build_vocab(train_sent_array)

        # train in different sequences
        for epoch in range(10):
            model.train(sentences.sentences_perm())
            model.alpha -= 0.002
            model.min_alpha = model.alpha

        model.save(path.join(path_to_files, 'dec2vec_model.d2v'))

        result = sentences.to_array()
        return result

    def do_clustering_v2(self, path_to_files):
        result = self.build_Model(path_to_files)
        sent_array = result.__getitem__(0)
        label_array = result.__getitem__(1)

        model = gensim.models.doc2vec.Doc2Vec.load(path.join(path_to_files, 'dec2vec_model.d2v'))

        feature_arrays = numpy.zeros((len(sent_array), self.featuresize))
        for i in range(len(sent_array)):
            feature_arrays[i] = model.docvecs[sent_array.__getitem__(i).__getitem__(1)]

        # For evaluation: split groundtrutz into trainings- and test- set (1/4 : 3/4)
        length_3_4 = int(len(feature_arrays) / 4 * 3 + 1)
        length_1_4 = int(len(feature_arrays) / 4 + 1)
        train_arrays = numpy.zeros((length_3_4, self.featuresize))
        test_arrays = numpy.zeros((length_1_4, self.featuresize))
        train_labels = numpy.empty(length_3_4, dtype='|S10')
        test_labels = numpy.empty(length_1_4, dtype='|S10')

        index_train = 0
        index_test = 0

        for j in range(len(label_array)):
            if j % 4 == 1:
                test_arrays[index_test] = feature_arrays[j]
                test_labels[index_test] = label_array[j]
                index_test += 1
            else:
                train_arrays[index_train] = feature_arrays[j]
                train_labels[index_train] = label_array[j]
                index_train += 1

        classifier = LogisticRegression()
        classifier.fit(train_arrays, train_labels)

        prediction_arr = classifier.predict(test_arrays)

        pred_index = 0
        for j in range(len(test_labels)):
            # print('prediction: ', prediction_arr[j], ' --- truth: ', test_labels[j])
            if prediction_arr[j] != b'irish':
                pred_index += 1

        score = classifier.score(test_arrays, test_labels)
        print('Test score: ', round(score*100, 2), '%')

        # print(model.docvecs['classical'])
        print('Most similar to irish_4: \n', model.docvecs.most_similar('irish_4'))


class LabeledLineSentence_v2(object):
    def __init__(self, filename):
        self.filename = filename

    def to_array(self):
        self.sentences = []
        self.genre_labels = []

        with open(self.filename, newline='', encoding="UTF-8") as file:

            line = ''
            myreader = csv.reader(file, delimiter=';')
            myList = list(myreader)

            first_row = True
            item_no = 0
            classical_index = 0
            irish_index = 0
            folclore_index = 0
            invironment_index = 0
            spoken_index = 0

            for row in myList:
                sentence = ''
                label = ''
                item_no = item_no + 1

                # skip titles
                if first_row:
                    first_row = False
                    continue

                row_index = 0
                for column in row:
                    row_index = row_index + 1
                    # use only the following rows from the csv:
                    #   - (id)
                    #   - contributor (not translated)
                    #   - creator (only translated if country == france)
                    #   - date
                    #   - describtion - trans
                    #   - spatial
                    #   - subject - trans
                    #   - type - trans
                    #   - year
                    if (row_index < len(row)) and row_index in [1, 2, 5, 7, 8, 16, 17, 18, 19, 20]:
                        sentence = sentence + ' ' + column
                    else:
                        label = column

                        ## count from 1 - n for every genre
                        if label == 'classical':
                            classical_index = classical_index + 1
                            item_no = classical_index
                        if label == 'irish':
                            irish_index = irish_index + 1
                            item_no = irish_index
                        if label == 'folklore':
                            folclore_index = folclore_index + 1
                            item_no = folclore_index
                        if label == 'invironment':
                            invironment_index = invironment_index + 1
                            item_no = invironment_index
                        if label == 'spoken':
                            spoken_index = spoken_index + 1
                            item_no = spoken_index

                self.genre_labels.append(label)
                self.sentences.append(gensim.models.doc2vec.LabeledSentence(sentence.split(), [label + '_%s' % item_no]))
                # self.sentences.append(LabeledSentence(sentence.split(), [label]))

        return [self.sentences, self.genre_labels]

    def sentences_perm(self):
        shuffle(self.sentences)
        return self.sentences
