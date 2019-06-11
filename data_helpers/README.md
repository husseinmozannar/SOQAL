## View The Arabic Machine Comprehension Dataset

To view the full the ARCD dataset just run (-v 1 is to view all the data, -v 0 for a summary):

```shell
python view_data.py -d ../data/arcd.json -v 1
```

To view the full the Arabic SQuAD dataset just run:

```shell
python view_data.py -d ../data/Arabic-SQuAD.json -v 1
```

## Split datasets for train-dev-test

We have provided helper scripts in data_split.py to split your data into training, developement and testing.

The two functions: train_dev_test_split, train_test_split help you do so, just call them and provide the dataset path and percentages. Each creates new files for the splits.

