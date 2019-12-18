for task in "high" "low" "medium"
do
bash scripts/experiment_pipe.sh $task $task.1.5.1.5 1.5 1.5 2 &
bash scripts/experiment_pipe.sh $task $task.2.0.2.0 2.0 2.0 3 &
done

 
