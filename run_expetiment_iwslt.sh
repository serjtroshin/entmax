pip install sacrebleu sacremoses subword-nmt
att="entmax_bisection"
gen="entmax_bisection"
att=$1
att_alpha=$att
gen_alpha=$att
num_steps=100000
model="model_iwslt.de-en.$att."$gen"."$att_alpha"."$gen_alpha"_step_"$num_steps".pt"
if [ ! -d de-en ]; then
bash scripts/get_data.sh
bash scripts/tokenize_iwslt.sh
bash scripts/prepare_iwslt.sh de en
fi
bash scripts/train_iwslt.sh de en $att $gen $att_alpha $gen_alpha $num_steps
bash scripts/translate_iwslt.sh de en $model
bash scripts/detokenize_iwslt.sh de en $model
