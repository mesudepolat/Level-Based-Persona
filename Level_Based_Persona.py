import numpy as np
import pandas as pd
users = pd.read_csv("datasets/users.csv")
purchases = pd.read_csv("datasets/purchases.csv")
df = purchases.merge(users, how="inner", on="uid")
agg_df = df.groupby(["country", "device", "gender", "age"]).agg({"price": "sum"})
agg_df = df.groupby(["country", "device", "gender", "age"]).agg({"price": "sum"}).sort_values("price", ascending=False)
agg_df.reset_index(inplace=True)
agg_df["age_cat"] = pd.cut(agg_df["age"],
                           bins=[0, 19, 24, 31, 41, agg_df["age"].max()],
                           labels=["0_19", "19_23", "24_30", "31_40", "41_" + str(agg_df["age"].max())])
level_based_customers = [row[0] + "_" + row[1].upper() + "_" + row[2] + "_" + row[5] for row in agg_df.values]
agg_df["level_based_customer"] = level_based_customers
agg_df.drop(["country", "device", "gender", "age", "age_cat"], axis=1, inplace=True)
agg_df = agg_df[["level_based_customer", "price"]]
agg_df["level_based_customer"].count()
agg_df = agg_df.groupby("level_based_customer").agg({"price": "mean"})
agg_df = agg_df.reset_index()
agg_df["level_based_customer"].count()
agg_df["segment"] = pd.qcut(agg_df["price"], 4, labels=["D", "C", "B", "A"])
agg_df.groupby("segment").agg({"price": "mean"})
new_user = "TUR_IOS_F_41_75"
agg_df[agg_df["level_based_customer"] == new_user]
