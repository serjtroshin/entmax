task_type="high"
cd OpenNMT-py
python setup.py install
dir="../"
onmt_train -data $dir/data/demo \
--enc_rnn_size 300 \
--dec_rnn_size 300 \
--src_word_vec_size 300 \
--tgt_word_vec_size 300 \
--learning_rate 0.001 \
--optim adam \
--train_steps 130000 \
--encoder_type brnn \
--batch_size 64 \
--valid_steps 10000 \
--global_attention_function entmax_bisection \
--entmax_alpha 1.5 \
--entmax_iters 15 \
--generator_function entmax_bisection \
--generator_entmax_alpha 1.5 \
--generator_entmax_iters 15 \
--save_model $dir/models/model ${@:1}
