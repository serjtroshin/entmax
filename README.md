# \alpha-entmax

## Install
conda create --name entmax36 python=3.6
conda activate entmax36
cd OpenNMT-py
python setup.py install

git submodule init

## Preprocess
bash scripts/prepare_data.sh
