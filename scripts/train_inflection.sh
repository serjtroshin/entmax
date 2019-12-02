task_type="high"
cd OpenNMT-py
dir="../"
onmt_train -data $dir/data/demo \
--gpu_ranks 0 \
--world_size 1 \
--enc_rnn_size 300 \
--dec_rnn_size 300 \
--src_word_vec_size 300 \
--tgt_word_vec_size 300 \
--learning_rate 0.001 \
--optim adam \
--train_steps 130000 \
--batch_size 64 \
--valid_steps 10000 \
--global_attention_function entmax_bisect \
--entmax_alpha 1.5 \
--entmax_bisect_iters 20 \
--encoder_type brnn \
--save_model $dir/models/model ${@:1}
