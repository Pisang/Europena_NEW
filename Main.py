import logging
import os

import pandas as pd

from Doc2vec_clustering import Doc2vec_clustering
from DocManager import DocManager
from HardcodedRules import HardcodedRules


class Main:
    original_file = 'metadata_translation_v2'
    #original_file = 'Test'
    docManager = DocManager()

    def do_doc2vec(self):
        pass

    def do_word2vec(self):
        pass

    def do_KMeans_on_tfidf(self):
        pass

    def prepare_Document(file_path):

        # use only the following rows from the csv:
        #   - (id)
        #   - contributor (not translated)
        #   - creator (only translated if country == france)
        #   - date
        #   - describtion - trans
        #   - spatial
        #   - subject - trans
        #   - title
        #   - type - trans
        #   - year
        list_of_rows = ['contributor', 'creator', 'date', 'description', 'spatial', 'subject', 'title', 'type', 'year']

        file_path_open = file_path + Main.original_file + '.csv'
        reduced_file = Main.docManager.reduceRows(file_path_open, list_of_rows)

        clean_file = Main.docManager.do_clinsing_csv(reduced_file)
        file_path_clean = file_path + Main.original_file + '_clean.csv'

        clean_file.to_csv(file_path_clean, sep=';', encoding='utf-8', index_label='id')

    def apply_hardcoded_Rules(dataframe, file_path):
        rules = HardcodedRules()

        metadata_file_path = file_path+Main.original_file+'.csv'
        groundtruth_file_path = file_path+Main.original_file+'_groundtruth.csv'

        rules.applyRules(metadata_file_path, groundtruth_file_path)

    def make_groundtruth_dense(file_path):
        filename_gt = file_path + Main.original_file + '_groundtruth.csv'

        sparce_groundtruth = pd.read_csv(filename_gt, sep=';', encoding="utf-8", index_col='id')
        dense_groundtruth = sparce_groundtruth.dropna(axis=0, how='all', subset=['known_genre'])

        filename_dgt = file_path + '/doc2vec_files/' + Main.original_file + '_groundtruth_dense.csv'
        dense_groundtruth.to_csv(filename_dgt, sep=';', encoding="utf-8")

        # return dense_groundtruth


def main():
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

    # read the local path to the Euopena directory
    dir = os.path.dirname(__file__)
    filename = os.path.join(dir, 'mypath.txt')

    with open(filename, 'r', encoding="UTF-8") as mypath:
        file_path = mypath.readline()

        ######################## do Stuff
        ### prepare file: reduce columns, clinsing, ...
        #Main.prepare_Document(file_path)

        ### apply hardcoded rules
        #filename = file_path+Main.original_file+'_clean.csv'
        #clean_file = pd.read_csv(filename, sep=";", encoding="utf-8", index_col='id')
        #Main.apply_hardcoded_Rules(clean_file, file_path)

        #Main.make_groundtruth_dense(file_path)


        doc2vec_file_path = file_path+'doc2vec_files'
        cluster = Doc2vec_clustering()

        # cluster.build_Model(doc2vec_file_path) - old tutorial version
        cluster.do_clustering_v2(doc2vec_file_path)


### entrypoint
main()
