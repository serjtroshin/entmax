task_type=${1:-"high"}
epochs=${2:-10}
activation_alpha=${3:-1.5}
generator_alpha=${4:-1.5}
exp_dir=${5:-"exp"}
gpu_id=${6:-0}

mkdir $exp_dir/models

dir=".."
data_size=`wc -l data/$task_type.train.src | awk '{print $1}'`
batch_size=64
let epoch_steps=$data_size/$batch_size
let train_steps=$epochs*$epoch_steps
val_steps=$epoch_steps

cd OpenNMT-py
python3.6 setup.py install
echo "Data size $data_size"
echo "Training steps $train_steps"
echo "Val steps $val_steps"

onmt_train -data $dir/data/data.$task_type \
--gpu_ranks $gpu_id \
--world_size 1 \
--enc_rnn_size 300 \
--dec_rnn_size 300 \
--src_word_vec_size 300 \
--tgt_word_vec_size 300 \
--learning_rate 0.001 \
--optim adam \
--train_steps $train_steps \
--valid_steps $val_steps \
--encoder_type brnn \
--batch_size 64 \
--global_attention_function entmax_bisection \
--entmax_alpha $activation_alpha \
--entmax_iters 15 \
--generator_function entmax_bisection \
--generator_entmax_alpha $generator_alpha \
--generator_entmax_iters 15 \
--save_model $dir/$exp_dir/models/model
