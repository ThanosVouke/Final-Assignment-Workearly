import pandas as pd
import matplotlib.pyplot as plt 
import numpy as np 
import matplotlib.cm as cm

df = pd.read_csv('finance_liquor_sales.csv')
df.dropna(inplace=True)
df['Date'] = pd.to_datetime(df.date)
df.set_index('Date', inplace=True)
del df['date']
df = df[(df.index.year>=2016)&(df.index.year<=2019)]

# Part 1: Bottles sold per zip code:
    
popular_zip = df.groupby('zip_code')['bottles_sold'].sum()

#plot
colors = cm.rainbow(np.linspace(0, 1, len(popular_zip)))

fig = plt.figure(dpi=300)


plt.scatter(popular_zip.index,popular_zip,color=colors,s=50)
    
    
plt.ylim(-50,2000)
plt.ylabel('Bottles Sold',fontsize=15)
plt.xlabel('Zip Code',fontsize=15)
plt.title('Bottles Sold')
plt.tight_layout()
plt.show()

popular_zip = df.groupby(['zip_code','item_description'])['bottles_sold'].sum()
popular_zip.sort_values( ascending=False, inplace=True)
print(f"The most popular item per zipcode is: \n {popular_zip}")

#%% Part 2: Percentage of sales per store (showing the top 10):
    
sales = df.groupby('store_name')['sale_dollars'].sum()
perce_sales = (sales/sum(sales))*100

perce_sales.sort_values( ascending=True, inplace=True)



fig = plt.figure( dpi = 300)

colors = cm.rainbow(np.linspace(0, 1, len(perce_sales[-10:])))

plt.barh(perce_sales[-10:].index,perce_sales[-10:],color=colors)
    
    
plt.ylabel('Store name',fontsize=15)
plt.xlabel('Percentage of sales (%)',fontsize=15)
plt.title('Percentage of sales per store in the period between 2016-2019')
plt.tight_layout()
plt.show()

#%% Part 3: Maps of bottles sold per store's name: 
    
    
import folium

lat = []
lon = [] 
for i in df.store_location:
    j = i.split()
    lat.append(float(j[1][1:]))
    lon.append(float(j[2][0:-1]))

df['lat'] = lon
df['lon'] = lat


n = folium.Map(location=[45,-90], tiles="OpenStreetMap", zoom_start=6)

for i in range(0,len(df)):
   folium.CircleMarker(
      location=[df.iloc[i]['lat'], df.iloc[i]['lon']],
      popup=df.iloc[i]['store_name'],
      radius=float(df.iloc[i]['bottles_sold']/25),
      draggable = False,
      color='black',                                         
      fill=True,
      fill_color='yellow'
   ).add_to(n)
   
n.save('Scatter.html')    
   
from folium import plugins

m = folium.Map([40,-90], zoom_start=5,width="%100",height="%100")
locations = list(zip(df.lat, df.lon))
cluster = plugins.MarkerCluster(locations=locations,                     
               popups=df['bottles_sold'].tolist())  
m.add_child(cluster)
m.save('Cluster.html')   
    
    