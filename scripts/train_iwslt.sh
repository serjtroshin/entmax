cd OpenNMT-py
dir="../"
src=$1
tgt=$2
pair="$1-$2"
attention_fn=$3
generator_fn=$4
att_alpha=$5
gen_alpha=$6
num_iterations=$7
echo "$src $tgt $attention_fn $generator_fn $att_alpha $gen_alpha $num_iterations"

python train.py -data $dir/data/iwlst.$pair \
--gpu_ranks 0 \
--world_size 1 \
--enc_rnn_size 500 \
--dec_rnn_size 500 \
--src_word_vec_size 500 \
--tgt_word_vec_size 500 \
--learning_rate 0.001 \
--optim adam \
--train_steps $num_iterations \
--batch_size 64 \
--valid_steps 10000 \
--global_attention_function $attention_fn \
--generator_function $generator_fn \
--entmax_alpha $att_alpha \
--generator_entmax_alpha $gen_alpha \
--encoder_type brnn \
--save_model $dir/models/model_iwslt.$src-$tgt.$attention_fn.$generator_fn.$att_alpha.$gen_alpha
