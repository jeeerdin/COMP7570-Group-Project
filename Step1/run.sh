# Clear intermediate files
rm ./*.npy
rm ../data/edges/edges2015/*tx.txt
rm ../data/edges/edges2015/*eff.txt
rm ./*output.txt

# Run script
python make_addr_dir.py > make_addr_dir_output.txt
python change_address.py > change_address_output.txt
python change_tx.py > change_tx_output.txt
python txt_to_graph.py > txt_to_graph_output.txt
python make_daily_graphs.py > make_daily_graphs_output.txt
