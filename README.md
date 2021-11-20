# COMP 4060/7570 Group 2 Project
---
#### Members
- Judah Zammit
- Jordan Kashton
- Abram Kremer

---

#### Step 1 Results
- Results can be read in [step_1_report.txt](https://github.com/jeeerdin/COMP7570-Group-Project/blob/main/Step1/step_1_report.txt)

---

#### Step 2 Results
- Results can be read in [step_2_report.txt](https://github.com/jeeerdin/COMP7570-Group-Project/blob/main/Step2/step_2_report.txt)

---

#### Expected Repository Structure

* data (This is where all the data goes, this file is included in the .gitignore so you will have to download the files yourself)

    - edges (This is where all the edges data from step 1 goes, these can be downloaded from [here](https://chartalist.org/BitcoinData.html)
		- edges20XX (the files for a specific year goes here)
    - grams (This is where all the files related to the grams dataset goes)
        - raw This is where the raw csv's goes,[here](https://umanitoba-my.sharepoint.com/:u:/r/personal/zammitj3_myumanitoba_ca/Documents/grams.zip?csf=1&web=1&e=Dmgd93), You will have to rename it to 'raw')
		- parsed (This is where the processed grams data goes, you can either run 'read_grams.py', or download it from [here](https://umanitoba-my.sharepoint.com/:u:/g/personal/zammitj3_myumanitoba_ca/EVhGCF1bgKxHqTw-hQUpxrEB1VglALycHKPk4LUWQVi-_Q?e=mACX1p)
		- linked (This is where the grams data that has been linked to a transaction id will go when we get 'link_grams.py' working)

    - daily_graphs (This where the sparse matrices for each day goes)
		- dd_mm_tx_to_addr.npz (This is the sparse matrix for day dd and month mm transaction outputs)
		- dd_mm_addr_to_tx.npz (This is the sparse matrix for day dd and month mm transaction inputs)
		- months_1_to_12_btc_transactions_tx_to_addr.npz (This is the sparse matrix for the full year transaction outputs)
		- months_1_to_12_btc_transactions_addr_to_tx.npz (This is the sparse matrix for the full year transaction inputs)
        - You will either have to download these files from [here](https://umanitoba-my.sharepoint.com/:u:/r/personal/zammitj3_myumanitoba_ca/Documents/daily_graphs.zip?csf=1&web=1&e=zgvn2X ) or run 'Step1/run.sh'

* Step1 (All the files for step 1)
* Step2 (All the files for step 2)
* Step3 (All the files for step 2)

---

