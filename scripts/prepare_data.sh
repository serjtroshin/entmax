inflection_dir="conll2018/task1/all/"
target_dir="data/"
python scripts/prepare_inflection.py --data $inflection_dir --save_to $target_dir
cd OpenNMT-py
task_type="high"
dir="../"
onmt_preprocess -train_src $dir/data/$task_type.train.src -train_tgt $dir/data/$task_type.train.tgt \
-valid_src $dir/data/$task_type.dev.src -valid_tgt $dir/data/$task_type.dev.tgt -overwrite -save_data $dir/data/demo ${@:1}
