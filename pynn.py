from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


import pandas
import tensorflow
import sqlite3
import argparse
import time

# import pdb


parser = argparse.ArgumentParser()
parser.add_argument('--file_name', default='juliaball.db', type=str,
                    help='sqlite db file name')
parser.add_argument('--batch_size', default=100, type=int, help='batch size')
parser.add_argument('--train_steps', default=1000, type=int,
                    help='number of training steps')
parser.add_argument('--game_table', default='results', type=str,
                    help='table name for game logs')
parser.add_argument('--player_table', default='players', type=str,
                    help='table name for player profiles')
parser.add_argument('--model_checkpoint_directory', default='model_checks',
                    type=str, help='the directory where model checkpoints should be stored')


def train_fn(features, labels, batch_size):
    dataset = tensorflow.data.Dataset.from_tensor_slices((dict(features), labels))
    dataset = dataset.shuffle(1000).repeat().batch(batch_size)
    return dataset


def add_row_to_dataset(player_tuple, dataset, player_idx):
    (_, pa, outs, singles, doubles, triples, hrs) = player_tuple
    dataset['batter_' + str(player_idx + 1) + '_pa'].append(pa)
    dataset['batter_' + str(player_idx + 1) + '_outs'].append(outs)
    dataset['batter_' + str(player_idx + 1) + '_singles'].append(singles)
    dataset['batter_' + str(player_idx + 1) + '_doubles'].append(doubles)
    dataset['batter_' + str(player_idx + 1) + '_triples'].append(triples)
    dataset['batter_' + str(player_idx + 1) + '_hrs'].append(hrs)
    return dataset


def main(argv):
    main_start_time = time.time()
    print("Setting up data structures")

    feature_col_list = ['batter_' + str(i+1) + '_' + y
                        for i in range(9)
                        for y in ['pa', 'outs', 'singles', 'doubles', 'triples', 'hrs']]
    test_set_size = 0
    training_dataset = {}
    testing_dataset = {}
    for title in feature_col_list:
        training_dataset[title] = []
        testing_dataset[title] = []
    training_result = []
    testing_result = []
    training_error = float('inf')
    trained_times = 0

    args = parser.parse_args(argv[1:])

    conn = sqlite3.connect(args.file_name)
    c = conn.cursor()
    c2 = conn.cursor()
    player_select_string = 'SELECT * FROM ' + args.player_table + ' WHERE idx=?'

    for (roster, avg_rpg) in c.execute('SELECT * FROM ' + args.game_table):
        roster = roster.strip(' []')
        player_id_list = roster.split()
        for (player_idx, player_id) in enumerate(player_id_list):

            c2.execute(player_select_string, (player_id,))
            player_tuple = (player_id, pa, outs, singles, doubles, triples, hrs) = c2.fetchone()

            if test_set_size < 250:
                testing_dataset = add_row_to_dataset(player_tuple, testing_dataset, player_idx)
            else:
                training_dataset = add_row_to_dataset(player_tuple, training_dataset, player_idx)

        if test_set_size < 250:
            testing_result.append(avg_rpg)
            test_set_size += 1
        else:
            training_result.append(avg_rpg)
            test_set_size += 1

    training_dataframe = pandas.DataFrame(data=training_dataset)
    testing_dataframe = pandas.DataFrame(data=testing_dataset)

    training_result_series = pandas.Series(training_result)
    testing_result_series = pandas.Series(testing_result)

    feature_columns = [tensorflow.feature_column.numeric_column(key=name, shape=(1,))
                       for name in feature_col_list]

    regressor = tensorflow.estimator.DNNRegressor(feature_columns=feature_columns,
        hidden_units=[2048, 1024, 512, 256, 128],
        model_dir=args.model_checkpoint_directory,
        warm_start_from=args.model_checkpoint_directory)

    while True:
        print("Have trained " + str(trained_times) + " times")
        trained = False
        print("Training...")
        while not trained:
            try:
                regressor.train(input_fn=lambda: train_fn(training_dataframe,
                                                          training_result_series, args.batch_size),
                                steps=args.train_steps)
                trained = True
            except tensorflow.train.NanLossDuringTrainingError:
                print("NAN'd during training.")

        print("Evaluating...")

        eval_result = regressor.evaluate(input_fn=lambda: train_fn(testing_dataframe,
                                                                   testing_result_series,
                                                                   args.batch_size),
                                         steps=10)

        print("----------------------------------")
        print("Test set eval result: " + str(eval_result))
        print("----------------------------------")

        training_error = eval_result['average_loss']
        trained_times += 1

        if trained_times == 1:
            break

    # pdb.set_trace()

    predict_dict = {
        'batter_1_pa': [559], 'batter_1_outs': [444], 'batter_1_singles': [84], 'batter_1_doubles': [23],
        'batter_1_triples': [4], 'batter_1_hrs': [4],

        'batter_2_pa': [602], 'batter_2_outs': [397], 'batter_2_singles': [133], 'batter_2_doubles': [51],
        'batter_2_triples': [10], 'batter_2_hrs': [11],

        'batter_3_pa': [467], 'batter_3_outs': [322], 'batter_3_singles': [94], 'batter_3_doubles': [25],
        'batter_3_triples': [9], 'batter_3_hrs': [17],

        'batter_4_pa': [608], 'batter_4_outs': [480], 'batter_4_singles': [70], 'batter_4_doubles': [31],
        'batter_4_triples': [7], 'batter_4_hrs': [20],

        'batter_5_pa': [674], 'batter_5_outs': [463], 'batter_5_singles': [108], 'batter_5_doubles': [66],
        'batter_5_triples': [11], 'batter_5_hrs': [26],

        'batter_6_pa': [300], 'batter_6_outs': [238], 'batter_6_singles': [45], 'batter_6_doubles': [10],
        'batter_6_triples': [2], 'batter_6_hrs': [5],

        'batter_7_pa': [700], 'batter_7_outs': [485], 'batter_7_singles': [114], 'batter_7_doubles': [58],
        'batter_7_triples': [20], 'batter_7_hrs': [23],

        'batter_8_pa': [345], 'batter_8_outs': [255], 'batter_8_singles': [66], 'batter_8_doubles': [16],
        'batter_8_triples': [4], 'batter_8_hrs': [4],

        'batter_9_pa': [491], 'batter_9_outs': [334], 'batter_9_singles': [107], 'batter_9_doubles': [35],
        'batter_9_triples': [6], 'batter_9_hrs': [9]
    }

    def test_input_fn():
        dataset = tensorflow.data.Dataset.from_tensors(predict_dict)
        return dataset

    pred_results = regressor.predict(input_fn=test_input_fn)

    for pred in enumerate(pred_results):
        print(pred)

    print("Final training error: " + str(training_error))
    print("--- %s seconds ---" % (time.time() - main_start_time))


start_time = time.time()
if __name__ == '__main__':
    tensorflow.logging.set_verbosity(tensorflow.logging.WARN)
    tensorflow.app.run(main)
print("--- %s seconds ---" % (time.time() - start_time))
