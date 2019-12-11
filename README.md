# \alpha-entmax

## Install

`conda create --name entmax36 python=3.6`

`conda activate entmax36`

`cd OpenNMT-py`

`python setup.py install`

`git submodule update --init --recursive`

## Preprocess MORPH
`bash scripts/prepare_data.sh`

## Preprocess IWSLT

`cd scripts`

`bash get_iwslt.sh`

`bash tokenize_iwslt.sh`

this will create `de-en` folder

## Train
`bash scripts/train_inflection.sh`

## Translate
`bash scripts/translate_inflection.sh`

## Eval Quality
`bash scripts/eval_accuracy_inflection.sh`


