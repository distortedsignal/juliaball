from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


import tensorflow
import argparse
import time


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


def main(argv):
    main_start_time = time.time()
    print("Setting up data structures")

    feature_col_list = ['batter_' + str(i+1) + '_' + y
                        for i in range(9)
                        for y in ['pa', 'outs', 'singles', 'doubles', 'triples', 'hrs']]

    args = parser.parse_args(argv[1:])

    feature_columns = [tensorflow.feature_column.numeric_column(key=name, shape=(1,))
                       for name in feature_col_list]

    regressor = tensorflow.estimator.DNNRegressor(feature_columns=feature_columns,
        hidden_units=[2048, 1024, 512, 256, 128],
        model_dir=args.model_checkpoint_directory,
        warm_start_from=args.model_checkpoint_directory)

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

    print("--- %s seconds ---" % (time.time() - main_start_time))


start_time = time.time()
if __name__ == '__main__':
    tensorflow.logging.set_verbosity(tensorflow.logging.WARN)
    tensorflow.app.run(main)
print("--- %s seconds ---" % (time.time() - start_time))
