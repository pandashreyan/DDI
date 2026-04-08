from tdc.multi_pred import DDI
data = DDI(name = 'DrugBank')
df = data.get_data()
print("Columns:", df.columns.tolist())
print(df.head())
