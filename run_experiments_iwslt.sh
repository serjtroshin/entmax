pip install sacrebleu sacremoses subword-nmt
att="softmax"
gen="softmax"
model="model_iwslt.de-en.$att."$gen"_step_100000.pt"
if [ ! -d de-en ]; then
bash scripts/get_data.sh
bash scripts/tokenize_iwslt.sh
bash scripts/prepare_iwslt.sh de en
fi
bash scripts/train_iwslt.sh de en $att $gen
bash scripts/translate_iwslt.sh de en $model
bash scripts/detokenize_iwslt.sh de en $model