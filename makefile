Tarea1: Bimodal GShared PShared Tournament
Bimodal:
		python3 ./branch_predictor.py --bp 0 -s 8

GShared:
		python3 ./branch_predictor.py --bp 1 -s 12 --gh 6

PShared:
		python3 ./branch_predictor.py --bp 2 -s 8 --lh 12
Tournament:
        python3 ./branch_predictor.py --bp 3 -s 12 --gh 6 --lh 12    

