
import argparse
import tensorflow
import sys
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

    arg_lists = [[int(x)] for x in sys.argv[1:]]
    zipped = zip(feature_col_list, arg_lists)
    predict_dict = {key: val for (key, val) in zipped}

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
