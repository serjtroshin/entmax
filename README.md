# entmax
Implementation of the paper [Sparse Sequence-to-Sequence Models](https://arxiv.org/pdf/1905.05702v2.pdf) 
### Install
```
conda create --name entmax36 python=3.6
conda activate entmax36
cd OpenNMT-py
python setup.py install
```

# MORPH
### Preprocess
```
git submodule update --init --recursive
bash scripts/prepare_data.sh [high | low | medium]
```
this will create `data` folder

### Experiments
Run all inflection experiments (with preprocessing and softmax as baseline)
`bash run_experiments_inflection.sh`

# IWSLT
### Preprocess
```
cd scripts
bash get_iwslt.sh
bash tokenize_iwslt.sh
```

this will create `de-en` folder

### Experiments
Run all iwlst experiments (with preprocessing and softmax as baseline)
`bash run_experiments_iwlst.sh`
