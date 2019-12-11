wget "https://wit3.fbk.eu/archive/2017-01-trnted//texts/de/en/de-en.tgz"
tar zxvf de-en.tgz
rm de-en.tgz

wget "https://wit3.fbk.eu/archive/2017-01-ted-test//texts/de/en/de-en.tgz"
tar zxvf de-en.tgz
rm de-en.tgz

wget "https://wit3.fbk.eu/archive/2017-01-ted-test//texts/en/de/en-de.tgz"
tar zxvf en-de.tgz
rm en-de.tgz

mv en-de/* de-en
rmdir en-de
