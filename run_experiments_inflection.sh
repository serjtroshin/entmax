gpu_id0=${1: 0}
gpu_id1=${2: 0}

if [ ! -d data ]; then
    mkdir data
fi

for task in "high" "low" "medium"
do
    if [ ! -f data/$task.train.src ] || [! -f data/$task.train.tgt]; then
        bash scripts/prepare_inflection_data.sh $task
    fi
done

for task in "high" "low" "medium"
do
    echo $task
    bash scripts/inflection_experiment_pipe.sh $task $task.1.5.1.5 1.5 1.5 $gpu_id0 &
    bash scripts/inflection_experiment_pipe.sh $task $task.2.0.2.0 2.0 2.0 $gpu_id1 &&
    bash scripts/inflection_experiment_pipe.sh $task $task.softmax 0 0 $gpu_id0
done

for task in "high" "low" "medium"
do
    for exp_type in "1.5.1.5" "2.0.2.0" "softmax"
    do
        echo "$exp_type"
        cat $task.$exp_type/result.txt | tail -n 2
        printf "\n"
    done
done
