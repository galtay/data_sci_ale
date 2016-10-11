mkdir -p data

wget -nc -O ./data/State_County_Table_All.zip https://www.cms.gov/Research-Statistics-Data-and-Systems/Statistics-Trends-and-Reports/Medicare-Geographic-Variation/Downloads/State_County_Table_All.zip

unzip ./data/State_County_Table_All.zip -d ./data

wget -nc -O ./data/Medicare_Shared_Savings_Program_Accountable_Care_Organizations_Performance_Year_2014_Results.csv  https://data.cms.gov/api/views/ucce-hhpu/rows.csv

python convert_geo_var_state_county_to_csv.py ./data/County_All_Table.xlsx
