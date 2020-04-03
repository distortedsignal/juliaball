import sys

import pandas
import tensorflow

with open('/tmp/predictor_logs.log', 'a') as log:

    log.write('starting scoring script')

    argument_dict = {
        'model_checkpoint_directory': '/bd-fs-mnt/tom_repo/models/lineup_to_runs_model'
    }

    log.write('argument_dict: ' + str(argument_dict))


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
        print("Setting up data structures")
        log.write('starting eval')

        feature_col_list = ['batter_' + str(i+1) + '_' + y
                            for i in range(9)
                            for y in ['pa', 'outs', 'singles', 'doubles', 'triples', 'hrs']]

        eval_dataset = {}

        items_processed = 0

        log.write('getting data from POST')
        for item in sys.argv[1:]:
            eval_dataset[feature_col_list[items_processed]] = int(item)
            items_processed += 1

        log.write('got data from post: ' + str(eval_dataset))

        predicting_dataframe = pandas.DataFrame(data=eval_dataset)

        feature_columns = [tensorflow.feature_column.numeric_column(key=name, shape=(1,))
                           for name in feature_col_list]

        log.write('creating regressor')

        regressor = tensorflow.estimator.DNNRegressor(feature_columns=feature_columns,
            hidden_units=[2048, 1024, 512, 256, 128],
            warm_start_from=argument_dict['model_checkpoint_directory'])

        log.write('regressor created')

        print(str(regressor.predict(predicting_dataframe)))

        log.write('done')



    if __name__ == '__main__':
        tensorflow.logging.set_verbosity(tensorflow.logging.WARN)
        tensorflow.app.run(main)
