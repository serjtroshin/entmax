fn=$1
att="$fn"
gen="$fn"
coef=$2
att_alpha=$coef
gen_alpha=$coef
num_steps=100000
model="model_iwslt.de-en.$att."$gen"."$att_alpha"."$gen_alpha"_step_"$num_steps".pt"
bash scripts/train_iwslt.sh de en $att $gen $att_alpha $gen_alpha $num_steps
bash scripts/translate_iwslt.sh de en $model
bash scripts/detokenize_iwslt.sh de en $model
