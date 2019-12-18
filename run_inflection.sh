set -e

for task_type in "medium"
do

for alpha in 1.5
do

bash scripts/experiment_pipe.sh $task_type exp.$task_type $alpha $alpha 3

done
done
