import pandas as pd
names=['dinga','dingi','manga','mangi']
eng=[100,70,50,60]
hin=[60,40,70,20]
tamil=[80,90,70,50]
# print(eng,hin,tamil)
df=pd.DataFrame({'student_name':names,'sub1':eng,'sub2':hin,'sub3':tamil})
print(df)