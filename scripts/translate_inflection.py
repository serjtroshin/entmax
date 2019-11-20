task_type="high"
cd OpenNMT-py
dir="../"
onmt_translate -model $dir/demo-model_step_5000.pt -src $dir/data/high.dev.src -output $dir/data/pred.txt -replace_unk -verbose