task_type=${1:-"high"}
exp_dir=${2-"exp"}
model=`ls -Art $exp_dir/models/ | tail -n 1`
model_step=55000
cd OpenNMT-py
dir="../"
onmt_translate -model $dir/$exp_dir/models/$model -src $dir/data/$task_type.dev.src -output $dir/$exp_dir/pred.txt -replace_unk
