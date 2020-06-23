# mutual_fund_generator_aa
Generated AA compliant deposit - JSON by taking CSV of the bank statement from SBI
https://specifications.rebit.org.in/api_schema/account_aggregator/documentation/mutual_funds.html

Visit the webiste https://new.camsonline.com/Investors/Statements/Transaction-Details-Statement
Fill in your email id, the time range for Mutual Funds transactions history that you want to analyse.
You will receive an e-mail with a download link. 
Download the zip file and unzip it using the password that you mentioned on the CAMS website.
You will have received two xls files in the unzip folder.
1. Starts with CurrentValuation - It is the consolidated statement of your MF investments
2. Starts with an alphanumeric character - This contains the transaction details of your MF investments

#### Clone repo and check for conda -
```
git clone https://github.com/abraj09/mutual_funds_generator_aa.git
cd deposit_generator_aa
conda --version
```
#### If error, then install conda using the following steps -

- for MacOS
```
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-MacOSX-x86_64.sh
sh Miniconda3-latest-MacOSX-x86_64.sh
```
- for Linux
```
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
sh Miniconda3-latest-Linux-x86_64.sh
```

#### After conda installation is complete, restart terminal-
```
conda create -n temp_env_gen python=3.7
conda activate temp_env_gen
pip install -r requirements.txt
python
```
#### Within python shell
```
from generator import mutual_fund_generator
consolidated_statement_path = "path/to/csv/bank/statement"
transaction_statement_path
mutual_fund_generator(transaction_statement_path, consolidated_statement_path)
```

PS. This is currently supported for mutual funds services by CAMS only 
