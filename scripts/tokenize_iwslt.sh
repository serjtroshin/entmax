DATA_DIR="de-en/"

set -e 
python parse_xml.py

BPE_MERGES=32000

for lang in en de
do
cat $DATA_DIR/train.tags.de-en.$lang | \
    grep -v '<doc' | \
    grep -v '<doc\>' | \
    grep -v '<reviewer' | \
    grep -v '<translator' | \
    grep -v '<speaker>' | \
    grep -v '<url>' | \
    grep -v '<talkid>' | \
    grep -v '<keywords>' | \
    sed -e 's/<title>//g' | \
    sed -e 's/<\/title>//g' | \
    sed -e 's/<description>//g' | \
    sed -e 's/<\/description>//g' > $DATA_DIR/train.de-en.$lang
done

for lang in en de
do
cat $DATA_DIR/IWSLT17.TED.tst2012*.$lang.parsed \
    $DATA_DIR/IWSLT17.TED.tst2013*.$lang.parsed \
    $DATA_DIR/IWSLT17.TED.tst2014*.$lang.parsed > $DATA_DIR/dev.de-en.$lang
done

for lang in en de
do
cat $DATA_DIR/IWSLT17.TED.tst2015*.$lang.parsed \
    $DATA_DIR/IWSLT17.TED.tst2016*.$lang.parsed \
    $DATA_DIR/IWSLT17.TED.tst2017*.$lang.parsed > $DATA_DIR/test.de-en.$lang
done

for data in train test dev
do
for lang in en de
do
sacremoses tokenize -j 8 -l $lang < $DATA_DIR/$data.de-en.$lang > $DATA_DIR/$data.de-en.$lang.tok
done
done

for lang in en de
do
sacremoses train-truecase -m "$DATA_DIR/true_case.model.$lang" -j 8 < $DATA_DIR/train.de-en.$lang.tok
done

for data in train test dev
do
for lang in en de
do
sacremoses truecase -m "$DATA_DIR/true_case.model.$lang" -j 8 < $DATA_DIR/$data.de-en.$lang.tok > $DATA_DIR/$data.de-en.$lang.tok.truecased
done
done

cat $DATA_DIR/$data.de-en.en.tok.truecased $DATA_DIR/$data.de-en.de.tok.truecased | \
subword-nmt learn-bpe -s $BPE_MERGES -o $DATA_DIR/bpe_codes

for data in train test dev
do
for lang in en de
do
subword-nmt apply-bpe -c $DATA_DIR/bpe_codes < $DATA_DIR/$data.de-en.$lang.tok.truecased > $DATA_DIR/$data.de-en.$lang.tok.truecased.bpe
done
done

rm $DATA_DIR/*.parsed
rm $DATA_DIR/*.xml
mv $DATA_DIR ../$DATA_DIR