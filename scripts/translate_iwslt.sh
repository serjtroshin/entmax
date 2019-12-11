cd OpenNMT-py
dir="../"
src=$1
tgt=$2
pair="$1-$2"
model=$3
python translate.py -model $dir/models/$model \
-src $dir/de-en/test.$pair.$tgt.tok.truecased.bpe \
-output $dir/data/$model.predict \
-replace_unk
