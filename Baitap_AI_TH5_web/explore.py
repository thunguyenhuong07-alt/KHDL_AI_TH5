import pandas as pd
df = pd.read_csv('Financial Statement Anomaly Dataset.csv')
print('Shape:', df.shape)
print('\nColumns:')
print(df.columns.tolist())
print('\nDtypes:')
print(df.dtypes)
print('\nFirst 5 rows:')
print(df.head().to_string())
print('\nDescribe:')
print(df.describe().to_string())
print('\nNull counts:')
print(df.isnull().sum())
print('\nUnique value counts for low-cardinality columns:')
for col in df.columns:
    u = df[col].nunique()
    if u < 20:
        print(f'\n{col}: {u} unique values')
        print(df[col].value_counts())