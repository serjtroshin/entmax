task_type=${1:-"high"}
target_dir=${2:-"data/"}
inflection_dir="conll2018/task1/all/"
dir="../"
python3.6 scripts/prepare_inflection.py --data $inflection_dir --save_to $target_dir --mode $task_type
cd OpenNMT-py

onmt_preprocess -train_src $dir/data/$task_type.train.src -train_tgt $dir/data/$task_type.train.tgt \
-valid_src $dir/data/$task_type.dev.src -valid_tgt $dir/data/$task_type.dev.tgt -overwrite -save_data $dir/data/demo
