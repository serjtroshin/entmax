task_type="high"
cd OpenNMT-py
dir="../"
onmt_train -data $dir/data/demo -save_model $dir/demo-model ${@:1}