pip install sacrebleu sacremoses subword-nmt
att="softmax"
gen="softmax"
model="model_iwslt.de-en.$att."$gen"_step_100000.pt"
bash scripts/prepare_iwslt.sh de en
bash scripts/train_iwslt.sh de en $att $gen
bash scripts/translate_iwslt.sh de en $model
bash scripts/detokenize_iwslt.sh de en $model