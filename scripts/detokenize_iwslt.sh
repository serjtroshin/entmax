cd OpenNMT-py
dir="../"
src=$1
tgt=$2
pair="$1-$2"
model=$3
pred=$model.predict
DATA_DIR="../de-en/"

cat $dir/data/$pred | sed -e "s/@@ //g" > $dir/data/$pred.debpe

sacremoses detruecase -j 8 < $dir/data/$pred.debpe > $dir/data/$pred.debpe.detrue

sacremoses detokenize -j 8 -l $tgt < $dir/data/$pred.debpe.detrue > $dir/data/$pred.debpe.detrue.detok

cat $dir/data/$pred.debpe.detrue.detok | sacrebleu $DATA_DIR/test.$pair.$tgt
