# برنامه ای که از سایت تکنولایف گوشی ها را بگیره و پس
# از اون با توجه به برند و رم و... قیمت گوشی را بهمون بگه

import numpy as np
import  requests
from bs4 import BeautifulSoup
import pandas as pd
# import numpy as np

# تابعی که دریافت میکنه اطلاعات را و به تعداد
# صفحه ای که میخوایم میگرده . پیشفرض ۲صفحه است ولی میشه پایین عوضش کرد
def get_data_site(url,pages=2):
    # ایجاد یک session برای افزایش سرعت و بهبود کارایی وب‌سایت
    session = requests.Session()
    counter = 0
    perfect_list=[]
    for page in range(1,pages):
        MyRequest=requests.get(url+str(page))
        soup=BeautifulSoup(MyRequest.text,'html.parser')
        model_ram_hard = soup.select('a.ProductComp_product_title__bOrf5')
        price=soup.select('div.ProductComp_main_price__XgWce')

        hard_size_camera_battery=soup.select('ul.pr_icon')
        whole_list=[]
        for char in hard_size_camera_battery:
            # print(char.text)
            # 41.77
            # 800
            # 41.8800
            # 50646.65000
            # 326.585000
            mylist=[]
            for b in char:
                # print(b.text)
                # 5000
                # 128
                # 6.43
                # 50
                mylist.append(b.text)
            whole_list.append(mylist)
            # print(mylist) #['64', '6.4', '64', '6000']
            counter+=1
            from more_itertools import collapse
            for m_r_h, pr, ra_si_cam_bat in zip(model_ram_hard, price, whole_list):
                # mrh=m_r_h.text.split(' ') #'گوشی', 'موبایل', 'اپل', 'مدل', 'iPhone', '13', 'Pro', 'Max', 'ZA/A', 'Not', 'Active'
                my=(m_r_h.text,pr.text, ra_si_cam_bat)
                # print(my) #('گوشی موبايل سامسونگ Galaxy A23 ظرفیت 128 گیگابایت رم 6 گیگابایت - ویتنام', '9,399,000تومان', ['128', '6.6', '50', '5000'])
                perfect_list.append(my)
                # perfect_list.append(list(map(collapse,my)))
    second_new = []
    for item in perfect_list:
        # جدا کردن عناصر درون رشته‌ی اول
        product, price, *specs = item
        # جایگزینی کاراکترهای خاص با کاما یا با چیزی که میخوایم
        # میشد از رجکس استفاده کرد
        product2 = product.replace(' - ', ',').replace('mAh','').replace('MP','').replace('in','').replace('VGA','0.3').replace('GB','').replace('4 مگابایت',',4,').replace('ظرفیت ', ',').replace('رم', '').replace('گیگابایت', '').replace('گوشی موبایل', 'گوشی موبایل,').replace('گوشی موبايل ', 'گوشی موبايل,').replace(',,', ',').replace('شیائومی ', 'شیائومی,').replace(' دو سیم کارت', '').replace('سامسونگ', 'سامسونگ,').replace('گلکسی','').replace('مدل', '').replace('نوکيا  ', 'نوکيا,').replace('اپل  ', 'اپل,').replace('هواوی  ', 'هواوی,').replace('نوکیا 150 ', 'نوکيا,').replace(' دو سیم‌ کارت', '')
        product3 = product2.strip().split(',')
        price = price.replace('تومان', '').strip() # چون قیمت جدا بود تومان را جدا اوردیم
        mylist = [product3, *specs, [price.strip()]]
        second_new.append(mylist)
    return (second_new)
    session.close()
# سایتشو که تکنو لایف است را میگیریم
mysite='https://www.technolife.ir/product/list/69_800_801/%D8%AA%D9%85%D8%A7%D9%85%DB%8C-%DA%AF%D9%88%D8%B4%DB%8C%E2%80%8C%D9%87%D8%A7?code=69_800_801&plp=%D8%AA%D9%85%D8%A7%D9%85%DB%8C-%DA%AF%D9%88%D8%B4%DB%8C%E2%80%8C%D9%87%D8%A7&page=1'
# فراخوانی و کاربرد تابع
data=(get_data_site(mysite,4))
# print(data)


# درست کردن داده ها برای بردن در پانداس
price=[]
for money in data:
    # print(money[2])
    # ['920,000']
    # ['9,399,000']
    # ['15,399,000']
    for i in money[2]:
        i=str(i.replace(',', '')) # جایگزینی میکنیم تا مثه ادم درست کار کنه
        price.append(i)
# print(price)
# print(len(price))


# رم و دوربین و.. را میگیره
ram=[]
size=[]
camera=[]
battery=[]
for char in data:
    # for the_ram in char[1][0]:
    if 'GB' in (char[1][0]):
        char[1][0] = ''.join([i for i in char[1][0] if  i.isdigit()]) # بررسی میکنه اونایی که gb داشتند را جایگزین میکنه با عدد خالی
    ram.append(char[1][0])
    if 'in' in char[1][1]:
        char[1][1]=''.join([i for i in char[1][1] if i.isdigit()]) # در بعضی هاشون اندازه را با in یعنی اینچ اوردن که درستشون میکنیم
    size.append(char[1][1])
    if 'VGA' in char[1][2]:
        char[1][2]=(char[1][2]).replace('VGA','0.3') #از اونجایی که vga هم ارز ۰.۳ دوربین است جایگزین میکنیم
    if 'MP' in char[1][2]:
        char[1][2]=''.join([i for i in char[1][2] if i.isdigit()])
    camera.append(char[1][2])

    if 'mAh' in char[1][-1]:
        char[1][-1]=''.join([i for i in char[1][-1] if i.isdigit()])
    battery.append(char[1][-1]) # خطا میده چون برای یکی سه تایی هستش و یکی چهارتایی واسه همین منفی یک را گرفتم

# print(ram)
# print(len(ram))
# #
# print(size)
# print(len(size))
# #
# print(camera)
# print(len(camera))
#
# print(battery)
# print(len(battery))


# مشخصات استرینگی موبایل ها مثل مدل گوشی و برند و...
product=[]
Brand=[]
Model=[]
for title in data:
    # اینجا برای اینکه مشکل تایپی باعث نشه که گوشی های موبایل که متفاوت نوشته شده اند
    # را برای برچسب زدن ماشین متفاوت تشخیص بده با یک چیز جایگزین کردم
    title[0][0]=title[0][0].replace(title[0][0],'گوشی موبایل') # میشه یع متغیر را جایگزین کنیم با یه رشته
    product.append(title[0][0])
    Brand.append(title[0][1])
    Model.append(title[0][2])

# print((product))
# print(len(product))
#
# print((Brand))
# print(len(Brand))
#
# print((Model))
# print(len(Model))


# تا اینجا داده ها را درآوردیم
# حالا به پانداس تبدیلشون میکنیم تا بتونیم به دیتا بیس ببریم
# 1-pandas
# درست کردن سرستون ها و لیست ها که به جدول پانداس تبدیل میکنیم
df=pd.DataFrame(np.column_stack([ram,size,camera,product,Brand,Model,battery,price]),columns=['ram','size','camera','product','Brand','Model','battery','price'])
# print(df)

# تبدیل پانداس به دیتابیس
# ساخت  دیتابیس فارسی


from mysql.connector import connect
import pymysql
import mysql
# اینجا دیتابیس را میسازیم
db=mysql.connector.connect(
    user='root',
    host='localhost',
    password='mamad951219644002',
)
# اینجا دیتابیس را میسازیم . که اگر وجود نداشت بسازش اگر داشت که بجاش بزار
cursor = db.cursor()
cursor.execute('CREATE DATABASE IF NOT EXISTS a_mobile')
# CREATE DATABASE IF NOT EXISTS DBname



# # ساخت موتور تبدیل پانداس به دیتابیس
import sqlalchemy
read_engine=sqlalchemy.create_engine('mysql+pymysql://root:mamad951219644002@localhost/a_mobile')
conn = read_engine.connect()

# تبدیل جدول پانداس به دیتابیس
df.to_sql(con=conn , name='r_mobile1',if_exists='replace',index=False)

# ///////////
# تا اینجا داده ها را ریختم توی دیتابیس . از این به بعد داده هارا فراخوانی میکنم
# ////////
# تبدیل دیتا بیس به جدول پانداس
# از همون موتور که ساختیم استفاده میکنیم
df_new=pd.read_sql_table('r_mobile1' ,con= conn )

# سرستونهامون اینها هستند
# 'ram','size','camera','product','Brand','Model','battery','price'


# تبدیل اعضا به اینتیجر
df_new['price']=df_new['price'].astype(int)  #درست شد
# print(df_new['price'])
df_new['ram']=df_new['ram'].astype(int) #درست شد
# print(df_new['ram'])
df_new['battery']=df_new['battery'].astype(int) #درست شد
# print(df_new['battery'])

df_new['size']=df_new['size'].astype(float) # درست شد
# print(df_new['size'])

# در مورد camera
# یا باید برچسب گذاری کنیم بر اساس استرینگ بودنش
# یا باید اون بقیه را یه جوری پر کنیم
# print(df_new)
df_new['camera']=df_new['camera'].mask(df_new['camera'] == '')
df_new['camera']=df_new['camera'].mask(df_new['camera'] == ' ')
df_new['camera']=df_new['camera'].mask(df_new['camera'] == '  ')
# print(df_new['camera'])
# 1580     50
# 1581    NaN
# حالا تبدیل . اول ببینیم درسته یا نه
# print(df_new.isnull().sum())

# حالا تبدیل null ها با صفر
df_new['camera']=df_new['camera'].fillna(0)
# print(df_new['camera'])
# 1580     50
# 1581      0

# print(df_new.isnull().sum())

# حالا تبدیل به فلوت
df_new['camera']=df_new['camera'].astype(float)
# print(df_new['camera'])



# اماده سازی برای یادگیری ماشین

# اینجا رم و اندازه گوشی و... را میدیم به عنوان ایکس
# 'ram','size','camera','product','Brand','battery'
# از این لیست قیمت را که به ایگریگ میدیم -
# مدل که نمیزاریم چون یه بار امتحان کردم یادیگری ماشین بر اساس الگوریتم هاش فقط پایه را مدل میگیره
X=df_new[['ram','size','camera','product','Brand','battery']].values
# print(X)

# # آوردن ایگیریگ ها
# اینجا قیمت هایی که داره را میاریم به ایگیریگ میدیم
Y=df_new[['price']].values
# print(Y)

from sklearn import preprocessing
product_enc=preprocessing.LabelEncoder()
# اینجا یه متغیر پیشپردازش درست میکنیم
# تا استرینگ ها را برچسب گذاری کنه

# 'ram','size','camera','product','Brand','battery'
# نمونه ما در این جا برند گوشی ها است
# print(X[:,3])  #[' شیائومی' ' شیائومی' 'نوکيا' ' شیائومی' 'نوکيا' 'نوکيا' ' شیائومی'
# اینجا روی تک تک برند گوشی ها فیت میکنیم
product_enc.fit([char for char in X[:,4]])
# اینجا تغیر میدیم به اعداد و میریزیم توی اون برند تا
# از این به بعد با شماره ای که کد گذاری کرده یادش بذاره
X[:,4]=product_enc.transform(X[:,4])
# print(X[:,3]) #[2 2 5 2 5 5 2



# 'ram','size','camera','product','Brand','battery'
# # اکنون روی کالا میزنیم . هرچند فقط یک کالا
# داریم با این حال دو تا تشخیص داده شاید بخاطر تایپش
# # گوشی موبایل
# # گوشی موبايل
# print(X[:,3]) #['گوشی موبایل' 'گوشی موبایل' 'گوشی موبایل' 'گوشی موبایل'
product_enc.fit([ char for char in X[:,3]])
X[:,3]=product_enc.transform(X[:,3])
# print(X[:,3]) #[0 0 0 0 0 0 0 0 0 0 0 0 0 0

# چطور داده های دوربین را درست کنم؟
# بجای اینکه خالی میده یه چیزی بده که بشه باهاش کار کنه
# ایده ۱ - نال بده و چون تعدادشون محدوده اشکالی نداره
# ۲- صفر بده و با بقیه که ۵۰ هستند مقایسه میشه
# ۳-با پانداس ببینم چه کار کرده








# حالا یادگیری ماشین و حدس قیمت یه گوشی فرضی

# print(X,Y)
# بهش  الگو میدیم
from sklearn import tree
dtc=tree.DecisionTreeClassifier()
learn_to_machine=dtc.fit(X,Y)


# بهش یه نمونه میدیم که با توجه به الگو بهمون بگه چی میشه
#  ترتیب از چپ به راست همینه . البته برای product همیشه صفر است چون محصولمون همیشه گوشی است
# 'ram','size','camera','product','Brand','battery'
# اینجا چند نمونه گوشی را با مشخصات عددی بهش میدیم
test=[[512, 128,50, 0 ,3 , 6000],[512, 256,50, 0 ,2 , 5000],[128, 256,50, 0 ,2 , 5000],[128, 512,50, 0 ,1, 6000]]

# مساله ۲- چطور یارو به زبان ادمی زاد بده و ما به زبان کامپیوتر برگردونیمش؟


# حالا قیمتشو بهم بگو
answer=learn_to_machine.predict(test)
print(answer[0]) #18178000
print(answer[1]) #17590000
print(answer[2]) #5819000
print(answer[3]) #7477000

# داده ها برای ۴ صفحه
# 18178000
# 17590000
# 5819000
# 7755000


