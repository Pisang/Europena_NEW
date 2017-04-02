import csv
import logging


class HardcodedRules:
    def applyRules(self, csv_data, csv_groundTruth):
        logging.info('aplying hardcoded rules')
        csv.field_size_limit(500 * 1024 * 1024)

        with open(csv_data, newline='', encoding="UTF-8") as translation:
            with open(csv_groundTruth, 'w', newline='', encoding="UTF-8") as metadata_genre:
                metadataReader = csv.reader(translation, delimiter=';')
                metadataList = list(metadataReader)

                first_row = True;

                for row in metadataList:
                    genre = ''

                    # skip titles
                    if first_row:
                        first_row = False;
                        metadataWriter = csv.writer(metadata_genre, delimiter=';')
                        metadataWriter.writerow(row)
                        continue

                    for column in row:
                        if ('mozart' in column.lower() or 'schubert, franz' in column.lower()):
                            genre = 'classical'

                        if ('testimony' in column.lower() and 'interview' in column.lower()):
                            genre = 'spoken'
                        # A spoken life: [recorded autobiography between 1963 and 1994]
                        if (len(row[17].split(' ')) > 10):
                            if (row[17].split(' ')[4] == 'autobiography'):
                                genre = 'spoken'
                        if (('free discussion' in row[18].lower() or 'interview' == row[18].lower())):
                            genre = 'spoken'

                        if (row[16].lower() == 'instrumental folk music'):
                            genre = 'folklore'
                        if ('latin american folk' in column.lower()):
                            genre = 'folklore'

                        if ('sound effect' in column.lower()):
                            genre = 'invironment'
                            # print(genre)

                        if ('irish traditional' in column.lower()):
                            genre = 'irish'

                        if ('popular music' in column.lower()):
                            genre = 'popular'

                    row.append(genre)
                    metadataWriter = csv.writer(metadata_genre, delimiter=';')
                    metadataWriter.writerow(row)

    def applyRules_pandas(self, clean_csv):
        '''
        didnt build that further due to: i have the thing above and it works :)
        '''
        genres = [None] * (len(clean_csv.index))

        for row in clean_csv.columns.values:
            index = 0
            for item in clean_csv[row]:

                for token in str(item).split():
                    if token == 'mozart': genres[index] = 'classic'
                    if token == 'schubert': genres[index] = 'classic'

                index = index + 1

        clean_csv['known_genre'] = genres

        file_path_clean = 'D:/Dropbox/Dropbox_Uni/Europena_NEW/Test_rules.csv'
        clean_csv.to_csv(file_path_clean, sep=';', encoding='utf-8', index_label='id')

        return clean_csv
