pip install sacrebleu sacremoses subword-nmt
att="entmax_bisection"
gen="entmax_bisection"
d=0
if [ ! -d de-en ]; then
cd scripts/
bash get_iwslt.sh
bash tokenize_iwslt.sh
cd ..
bash scripts/prepare_iwslt.sh de en
fi
for att in 1.5 2.0
do
CUDA_VISIBLE_DEVICES=$d bash run_experiment.sh $att &
d=$((d + 1))
done
