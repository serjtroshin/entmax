task_type=${1:-high}
exp_name=${2:-"exp"}
activation_alpha=${3:-1.5}
generator_alpha=${4:-1.5}
gpu_id=${5:-0}
epochs=${6:-8}

if [ ! -d $exp_name ]; then
    mkdir $exp_name
fi

if [[ "$exp_name" == *"softmax"* ]]; then
    bash scripts/train_inflection_softmax.sh $task_type $epochs $exp_name $gpu_id
else
    bash scripts/train_inflection_entmax_bisect.sh $task_type $epochs $activation_alpha $generator_alpha $exp_name $gpu_id
fi

bash scripts/translate_inflection.sh $task_type $exp_name
python scripts/eval_accuracy_inflection.py --data_true $task_type.dev.tgt --data_pred ../$exp_name/pred.txt > $exp_name/result.txt
cat $exp_name/result.txt | tail -n 2

