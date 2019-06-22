
## Training and Evaluating BERT on Arabic-SQuAD or ARCD

We have provided a Google Colab notebook to train, evaluate and demo BERT on our datasets availabe here: [Colab](https://colab.research.google.com/drive/19a_jIKpjhQez0KTa_Qwh2BW2nryGXzhb)


To train locally, the training and code follows exactly that of the [Official BERT repo](https://github.com/google-research/bert).

First download the multilingual model: [Cased recommended](https://storage.googleapis.com/bert_models/2018_11_23/multi_cased_L-12_H-768_A-12.zip), [Uncased not recommended](https://storage.googleapis.com/bert_models/2018_11_03/multilingual_L-12_H-768_A-12.zip).

Then just run, if you're using the cased model change do_lower_case to False:

**You need more than 6GB of GPU memory, recommend training on cloud**

```shell
python run_squad.py  ^
  --vocab_file=multilingual_L-12_H-768_A-12/vocab.txt  ^
  --bert_config_file=multilingual_L-12_H-768_A-12/bert_config.json  ^
  --init_checkpoint=multilingual_L-12_H-768_A-12/bert_model.ckpt  ^
  --do_train=True ^
  --train_file=../data/arabic-squad.json  ^
  --do_predict=False  ^
  --predict_file=../data/arcd.json  ^
  --train_batch_size=1  ^
  --learning_rate=3e-5  ^
  --num_train_epochs=2  ^
  --max_seq_length=250  ^
  --doc_stride=128  ^
  --do_lower_case=True ^
  --output_dir=./runs
```
If you have memory overflows try reducing (1) train_batch_size and (2) max_seq_length.

Then to evaluate on ARCD run the following two scripts:
```shell
python run_squad.py  ^
  --vocab_file=multilingual_L-12_H-768_A-12/vocab.txt  ^
  --bert_config_file=multilingual_L-12_H-768_A-12/bert_config.json  ^
  --init_checkpoint=multilingual_L-12_H-768_A-12/bert_model.ckpt  ^
  --do_train=False ^
  --train_file=../data/arabic-squad.json  ^
  --do_predict=True  ^
  --predict_file=../data/arcd.json  ^
  --train_batch_size=1  ^
  --learning_rate=3e-5  ^
  --num_train_epochs=2  ^
  --max_seq_length=250  ^
  --doc_stride=128  ^
  --do_lower_case=True ^
  --output_dir=./runs
```

```shell
python evaluate.py ../data/arcd.json  ./runs/predictions.json
```

## Local Demo of BERT

We have provided a trained model of BERT and an html demo, simply run:

```shell
python demo.py ^
-c multilingual_L-12_H-768_A-12/bert_config.json ^
-v multilingual_L-12_H-768_A-12/vocab.txt ^
-o runs/
```
and go to http://localhost:8000/
