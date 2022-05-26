import pandas as pd

df = pd.read_csv(r'C:\Users\user\Desktop\04 Raw data.csv', index_col=0, header=0, encoding='utf-8-sig')

drop_df = df[df['text'].str.contains("drug|drak web|bitcoin|bust|FBI|marketplace", case=False, regex=True, na=False)
             & (df['text'].str.contains('silk road', case=False, regex=True, na=False))
             & (~df["text"].str.contains('one belt one road|onebeltoneroad|belt and road|beltandroad', case=False, regex=True, na=False))]

df = df[~df.index.isin(drop_df.index)]
print(len(df))
df.reset_index(drop=True, inplace=True)
df.to_csv(r'C:\Users\user\Desktop\result.csv', encoding='utf-8-sig')
