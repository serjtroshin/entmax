task_type="high"
cd OpenNMT-py
dir="../"
onmt_train -data $dir/data/demo \
--enc_rnn_size 300 \
--dec_rnn_size 300 \
--src_word_vec_size 300 \
--tgt_word_vec_size 300 \
--learning_rate 0.001 \
--optim adam \
--valid_steps 658971 \
--save_model $dir/models/model ${@:1}