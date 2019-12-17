task_type=${1:-"high"}
steps=${2:-80000}
val_steps=${3:-10000}
cd OpenNMT-py
dir="../"
python3.6 setup.py install

onmt_train -data $dir/data/demo \
--gpu_ranks 0 \
--world_size 1 \
--enc_rnn_size 300 \
--dec_rnn_size 300 \
--src_word_vec_size 300 \
--tgt_word_vec_size 300 \
--learning_rate 0.001 \
--optim adam \
--train_steps $steps \
--batch_size 64 \
--valid_steps $val_steps \
--global_attention_function entmax15 \
--generator_function entmax15 \
--encoder_type brnn \
--save_model $dir/models/model
