task_type="high"
cd OpenNMT-py
dir="../"
onmt_translate -model $dir/models/model_step_130000.pt -src $dir/data/high.dev.src -output $dir/data/pred.txt -replace_unk ${@:1}
