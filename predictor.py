
import tensorflow
import sys
import time


def main(argv):
    main_start_time = time.time()
    print("Setting up data structures")

    feature_col_list = ['batter_' + str(i+1) + '_' + y
                        for i in range(9)
                        for y in ['pa', 'outs', 'singles', 'doubles', 'triples', 'hrs']]

    feature_columns = [tensorflow.feature_column.numeric_column(key=name, shape=(1,))
                       for name in feature_col_list]

    regressor = tensorflow.estimator.DNNRegressor(feature_columns=feature_columns,
        hidden_units=[2048, 1024, 512, 256, 128],
        model_dir='model_checks',
        warm_start_from='model_checks')

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
    tensorflow.logging.set_verbosity(tensorflow.logging.ERROR)
    tensorflow.app.run(main)
print("--- %s seconds ---" % (time.time() - start_time))
