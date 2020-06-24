# mutual_fund_generator_aa
Generated AA compliant mutual_fund dataset in JSON format
https://specifications.rebit.org.in/api_schema/account_aggregator/documentation/mutual_funds.html

You can use your mutual fund portfolio to generate this data set. Below are steps to do that.

1. Visit the webiste https://new.camsonline.com/Investors/Statements/Transaction-Details-Statement
2. Fill in your email id, the time range for Mutual Funds transactions history that you want to use.
3. Select All in the mutual funds drop dowm
4. Create a password, it will be used to unlock your personal document.
5. You will receive an e-mail shortly with a download link.
6. Download the zip file and unzip it using the password that you created in step 4.

You will have two xls files in the unzip folder.
1. Starts with CurrentValuation 
	- Example - CurrentValuationAS104829406.xls
	- It is the consolidated statement of your MF portfolio
2. Starts with a substring of the above name 
	- AS104829406.xls
	- This contains the transaction details of your MF portfolio

#### Clone repo and check for conda -
```
git clone https://github.com/abraj09/mutual_funds_generator_aa.git
cd mutual_funds_generator_aa
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
consolidated_statement_path = "path/to/xls/consolidated/statement"
transaction_statement_path = "path/to/xls/transaction/statement"
mutual_fund_generator(transaction_statement_path, consolidated_statement_path)
```
This will add a new file in your present working directory with the name 'data.txt'. This text file contains the JSON object

PS. This is currently supported for mutual funds that are serviced by CAMS only 
