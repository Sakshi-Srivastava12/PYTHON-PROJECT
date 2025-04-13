import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
#Loading dataset
data=pd.read_excel("retail_sales_dataset.xlsx")
print(data)
#Exploring Dataset
print("Information of DataSet:  \n",data.info())
print("Description of DataSet1:  \n",data.describe())
#Handling Missing Values
print("Missing values: ",data.isnull().sum())
data['Quantity']=data['Quantity'].fillna(12)
data['Price per Unit']=data['Price per Unit'].fillna(200)
data['Total Amount']=data['Total Amount'].fillna(20000)
data['Product Category']=data['Product Category'].fillna("Furniture")
data['Gender']=data['Gender'].fillna("Trans Gender")
data['Age']=data['Age'].fillna(data['Age'].mode()[0])
data['Customer ID']=data['Customer ID'].fillna("UNKNOWN")
data['Month']=data['Month'].fillna("June")
print(data)
#print("Drop Missing Values If any:  \n",data.dropna())
#Basic operation performed
print("1st 10 reows of DataSet:  \n",data.head(10))
print("1st 10 reows of DataSet:  \n",data.tail(10))
print("Shape of DataSet:  \n",data.shape)
print("Columns of DataSet:  \n",data.columns)
print("Datatype of DataSet: \n ",data.dtypes)
data.to_csv("cleaned_dataset.csv", index=False)
print("Saved succesfully")
#Total price Generated for each product
total_quantity=data.groupby('Product Category')['Quantity'].sum()
print("Total Quantity of each product:  \n ",total_quantity)
total=data.groupby('Product Category')['Total Amount'].sum()
print("Total price: \n",total)
plot_df = pd.DataFrame({
    'Product Category': total.index,
    'Total Amount': total.values
})
plt.figure(figsize=(10,6))
#sns.barplot(data=plot_df ,x=total_quantity.index,y=total.values,palette='viridis')
sns.barplot(data=plot_df, x='Product Category', y='Total Amount',  hue='Product Category',palette='viridis')
plt.xlabel("Product Category")
plt.ylabel("Total Amount")
plt.title("Revenue Per Category") 
plt.show()
#Average price of each product category
avg=data.groupby('Product Category')['Total Amount'].mean()
print("Average price: ",round(avg,2))
#best selling product
best=data.groupby('Product Category')['Quantity'].sum().sort_values(ascending=False)
print("Best Sellling product: \n ",best)
plt.figure(figsize=(12,6))
plt.bar(best.index,best.values,color="orange")
plt.title(" Most Popular Products by Sales")
plt.xlabel("Product Category")
plt.ylabel("Total Quantity")
plt.show()
#Total revenue generatd
total_sales=data['Total Amount'].sum()
print("Total Revenue: ",total_sales)
#Count no of male and female customers
count=data.groupby('Gender')['Customer ID'].count()
print(count)
revenue=data.groupby('Gender')['Total Amount'].sum()
print("Revenue generated by male and female separetly: \n ",revenue)
fig, axes = plt.subplots(1, 2, figsize=(14, 6))
c = ["cyan", "pink","m"] 
# Pie chart for customer count
axes[0].pie(count, labels=count.index, colors=c, autopct='%1.1f%%', startangle=90, shadow=True)
axes[0].set_title("Customer Count by Gender")

# Pie chart for revenue
axes[1].pie(revenue, labels=revenue.index, colors=c, autopct='%1.1f%%', startangle=90, shadow=True)
axes[1].set_title("Revenue by Gender")

# Display
plt.tight_layout()
plt.show()
"""plt.figure(figsize=(12,6))
c = ["cyan", "pink","m"]  # Use a list of colors
plt.pie(count, labels=count.index, colors=c, autopct='%1.1f%%') 
plt.title("Customer Count vs. Revenue: Gender-wise Analysis")
plt.xlabel("no of female and male")
plt.ylabel("revenue geerated by each gender")
plt.grid(True, ls="--", color="grey", zorder=1)
plt.show()"""
#Sales trend over time
data["Date"]=pd.to_datetime(data["Date"])
sales=data.groupby("Date")["Total Amount"].sum()
plt.figure(figsize=(12,8))
plt.plot(sales.index,sales.values,marker="*",ls="dashed", color="b")
plt.title("SALES TREND OVER TIME")
plt.xlabel("date")
plt.ylabel("Total AmountT")
plt.show()
#Monthly sales trend
mon=data.groupby("Month")["Total Amount"].sum()
month_order = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
]
mon.index=pd.Categorical(mon.index,categories=month_order,ordered=True)
mon=mon.sort_index()
plt.figure(figsize=(10,6))
plt.barh(mon.index,mon.values,color="cyan")
plt.xlabel("Month")
plt.ylabel("Quantity Sold")
plt.title(" Best-Selling Product Category Each Month")
#plt.legend()
plt.grid(axis="y", linestyle="--", alpha=0.7)
plt.show()
print("Total Sales per Month: \n",mon)
print("Verify month index: \n",mon.index)
#analyse monthly sale trend by product category
data["Month"]=pd.Categorical(data["Month"],categories=month_order,ordered=True)
monthly_sale=data.groupby(["Month", "Product Category"],observed=False)["Quantity"].sum().unstack()
plt.figure(figsize=(12, 6))
for category in monthly_sale.columns:
    plt.plot(monthly_sale.index, monthly_sale[category], marker="o", linestyle="-", label=category)
plt.title("Monthly Sales Trend by Product Category")
plt.xlabel("Month")
plt.ylabel("Total Quantity Sold")
plt.xticks(rotation=45)
plt.legend(title="Product Category")
plt.grid(axis="y", linestyle="--", alpha=0.7)
plt.show()
print("Sample data for verification: \n",data[["Month", "Product Category", "Quantity"]].head())  
print("Check aggregated sales data by product category: \n",monthly_sale.head())  
print("Ensure product categories are correct: \n",monthly_sale.columns)  
print("Verify months are sorted correctly: \n",monthly_sale.index)   
# price vs quantity
plt.figure(figsize=(12,6))
jitter = np.random.uniform(-0.1, 0.1, size=len(data))

sns.scatterplot(x=data["Price per Unit"],y=data["Quantity"] + jitter,color="blue",alpha=0.7,s=100)
sns.regplot(x=data["Price per Unit"], y=data["Quantity"], scatter=False, color="red", line_kws={"linewidth": 2})

plt.title("The Price Puzzle")
plt.ylabel("Quantity")
plt.xlabel("Price Per Unit")
plt.grid(True,linestyle="--")
plt.show()
# Calculate correlation
correlation = data["Price per Unit"].corr(data["Quantity"])
print(f"Correlation between Price per Unit and Quantity Sold: {correlation:.2f}")
#boxplot to analyze
plt.figure(figsize=(12,6))
sns.boxplot(x="Product Category", y="Price per Unit", hue="Product Category",data=data, palette="Set2",legend=False)
sns.stripplot(x="Product Category", y="Price per Unit", data=data, color="black", alpha=0.6, jitter=True)

plt.title("Price Distribution Across Product Categories")
plt.xlabel("Product Category")
plt.ylabel("Price per Unit")
plt.xticks(rotation=45)  
plt.grid(True, linestyle="--", alpha=0.5)
plt.show()
print(data.groupby("Product Category")["Price per Unit"].describe())



# Standardize column names
data.columns = data.columns.str.strip()

# Create Age Groups for better readability
bins = [18, 25, 35, 45, 55, 65]  # Define age ranges
labels = ["18-25", "26-35", "36-45", "46-55", "56-65"]
data["Age Group"] = pd.cut(data["Age"], bins=bins, labels=labels, include_lowest=True)

# Create Pivot Table: Sales by Age Group & Product Category
age_category_sales = data.pivot_table(
    index="Age Group", 
    columns="Product Category", 
    values="Total Amount", 
    aggfunc="sum", 
    fill_value=0,

    
    observed=False
)

# Plot heatmap with improved readability
plt.figure(figsize=(10, 5))  # Adjust figure size
sns.heatmap(
    age_category_sales, 
    cmap="Blues", 
    annot=True, 
    fmt=".0f", 
    linewidths=0.5, 
    cbar_kws={'shrink': 0.8},  # Shrink color bar
    annot_kws={"size": 10}
   # Adjust annotation font size
)

# Improve Labels
plt.xticks(rotation=45, ha="right", fontsize=12)  # Rotate x-axis labels
plt.yticks(fontsize=12)  # Increase y-axis font size
plt.title("Sales Distribution Across Age Groups & Product Categories", fontsize=14, fontweight="bold")
plt.xlabel("Product Category", fontsize=12)
plt.ylabel("Age Group", fontsize=12)

# Show the improved heatmap
plt.show()
