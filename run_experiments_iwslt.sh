pip install sacrebleu sacremoses subword-nmt
d=0
if [ ! -d de-en ]; then
cd scripts/
bash get_iwslt.sh
bash tokenize_iwslt.sh
cd ..
bash scripts/prepare_iwslt.sh de en
fi
fn="entmax_bisection"
for att in 1.5 2.0
do
CUDA_VISIBLE_DEVICES=$d bash run_experiment.sh $fn $att &
d=$((d + 1))
done
fn="softmax"
att=1
CUDA_VISIBLE_DEVICES=$d bash run_experiment.sh $fn $att &
