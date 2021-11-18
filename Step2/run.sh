rm *output.txt
rm ../data/grams/parsed/*.npy
rm ../data/grams/linked/*.npy

python read_grams.py > read_grams_output.txt
python link_grams.py > link_grams_output.txt
