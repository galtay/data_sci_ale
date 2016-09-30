# Medicare Drug Spending

CMS makes some data available on drug spending.  Lets look at it.
[Data Page](https://www.cms.gov/Research-Statistics-Data-and-Systems/Statistics-Trends-and-Reports/Information-on-Prescription-Drugs/)

Click on the "Download the full underlying data in Excel here." link. This will get you a `Drug_Spending_Data.zip` file.  Create a directory named `data`, copy the zip file there, and then unzip it.  For example,

```shell
mkdir data
mv ~/Downloads/Drug_Spending_Data.zip data/
cd data
unzip Drug_Spending_Data.zip
```

This should get you a file called `Medicare_Drug_Spending_Dashboard_Data_02_17_2016.xlsx`.  Now the notebook in this directory should run.