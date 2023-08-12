import pandas as pd
from prophet import Prophet
import streamlit as st
from datetime import datetime,date,time
import yfinance as yf
import matplotlib.pyplot as plt


liste = ['TRY=X', 'BTC-USD', 'ASELS.IS', 'GOOG','SIRI','GBPUSD=X','AAL','RIVN','T','AMD','PLTR','NVDA','INFY','KVUE','NIO','CCL','SWN']
secim = st.sidebar.selectbox("Birimi Seç", liste)
baslangic = st.sidebar.date_input("Başlangıç Tarihi",min_value=date(2005,1,1),max_value=datetime.now())
bitis = st.sidebar.date_input("Bitiş Tarihi")
getirday= st.sidebar.button("Günlük Değerleri Görüntüle")
getirmonth = st.sidebar.button("Aylık Değerleri Görüntüle")
getiryear = st.sidebar.button("Yıllık Değerleri Görüntüle")

if getirday:
    df = yf.download(secim, baslangic, bitis)
    df.reset_index(inplace=True)  # Dizini sıfırlayalım
    dft = df[['Date', 'Close']]
    dft.rename(columns={'Date': 'ds', 'Close': 'y'}, inplace=True)
    future_day_table=dft
    future_day_table=future_day_table.rename(columns={'ds':'Tarih','y':'Günlük Fiyat'})
    future_day_table['Tarih']=pd.to_datetime(future_day_table['Tarih'])
    future_day_table['Tarih']=future_day_table['Tarih'].dt.strftime('%Y-%m-%d')




    fig, ax = plt.subplots()

    ax.plot(df['Date'], df['Close'], label='Kapanış Fiyatı')

    ax.set_xlabel('Tarih')
    ax.set_ylabel('Kapanış Fiyatı')
    ax.set_title(f"{secim} Birimi Günlük Kapanış Grafiği")
    ax.legend()

    plt.xticks(rotation=90)
    st.pyplot(fig)
    st.write(f"Günlük {secim} Fiyatları")
    st.write(future_day_table)
if getirmonth:
    df = yf.download(secim, baslangic, bitis)
    df.reset_index(inplace=True)  # Dizini sıfırlayalım
    dft = df[['Date', 'Close']]
    dft.rename(columns={'Date': 'ds', 'Close': 'y'}, inplace=True)

    fig, ax = plt.subplots()

    ax.plot(df['Date'], df['Close'], label='Kapanış Fiyatı')

    ax.set_xlabel('Tarih')
    ax.set_ylabel('Kapanış Fiyatı')
    ax.set_title(f"{secim} Birimi Aylık Ortalama Kapanış Grafiği")
    ax.legend()


    dft['Month'] = dft['ds'].dt.to_period('M')  # Tarihleri ay formatına dönüştürelim
    avg_monthly_prices = dft.groupby('Month')['y'].mean()

    x_labels = avg_monthly_prices.index.strftime('%Y-%m-%d')

    fig_monthly, ax_monthly = plt.subplots()
    ax_monthly.plot(avg_monthly_prices.index.strftime('%Y-%m'), avg_monthly_prices.values,
                    label='Aylık Ortalama Kapanış Fiyatı')
    ax_monthly.set_xlabel('Ay')
    ax_monthly.set_ylabel('Ortalama Kapanış Fiyatı')
    ax_monthly.set_title(f"{secim} Birimi Aylık Ortalama Kapanış Grafiği")
    ax_monthly.legend()

    plt.xticks(rotation=90)
    st.pyplot(fig_monthly)

    df_with_monthly_avg = pd.concat(
        [avg_monthly_prices.rename('Aylık Ortalama Fiyatı'), dft.set_index('ds')['y']], axis=1)

    st.write(f"Aylık Ortalama {secim} Fiyatları:")
    st.write(df_with_monthly_avg.drop(columns='y'))
if getiryear:
    df=yf.download(secim,baslangic,bitis)
    df.reset_index(inplace=True)
    dft=df[['Date','Close']]
    dft.rename(columns={'Date':'ds', 'Close':'y'},inplace=True)
    fig,ax=plt.subplots()
    ax.plot(df['Date'],df['Close'],label='Kapanış Fiyatı')
    ax.set_xlabel("Tarih")
    ax.set_ylabel('Kapanış Fiyatı')
    ax.set_title(f"{secim[0]} Birimi Kapanış Fiyatları")
    ax.legend()

    dft['Year'] = dft['ds'].dt.to_period('Y')
    avg_year_prices=dft.groupby('Year')['y'].mean()
    x_labels=avg_year_prices.index.strftime('%Y-%M-%D')
    fig_year,ax_year=plt.subplots()
    ax_year.plot(avg_year_prices.index.strftime('%Y-%M-%D'),avg_year_prices.values,label='Yıllık Ortalama Kapanış Fiyatları')
    ax_year.set_xlabel('Yıl')
    ax_year.set_ylabel('Ortalama Kapanış Fiyatı')
    ax_year.set_title(f"{secim} Birimi Yıllık Ortalama Kapanış Grafiği")
    ax_year.legend()


    plt.xticks(rotation=90)
    st.pyplot(fig_year)
    df_with_year_avg = pd.concat(
        [avg_year_prices.rename('Yıllık Ortalama Fiyatı'), dft.set_index('ds')['y']], axis=1)

    st.write(f"Yıllık Ortalama {secim} Fiyatları ")
    st.write(df_with_year_avg.drop(columns='y'))

winner_hisse=st.sidebar.button("En Çok Kazandıran Hisseler")
if winner_hisse:
    hisse_verileri = {}
    for sembol in liste:
        hisse_verileri[sembol] = yf.download(sembol, start=baslangic, end=bitis)['Close']

    yuzde_degisimler = {}
    for sembol, hisse_fiyatlari in hisse_verileri.items():
        if not hisse_fiyatlari.empty:
            yuzde_degisim = ((hisse_fiyatlari.iloc[-1] - hisse_fiyatlari.iloc[0]) / hisse_fiyatlari.iloc[0]) * 100
            yuzde_degisimler[sembol] = yuzde_degisim

    en_cok_kazandiranlar = sorted(yuzde_degisimler.items(), key=lambda x: x[1], reverse=True)

    # En çok kazandıranları görselleştirmek için çubuk grafik oluşturun
    en_cok_kazandiranlar_df = pd.DataFrame(en_cok_kazandiranlar, columns=['Hisse', 'Yuzde_Degisim'])
    fig, ax = plt.subplots()
    ax.bar(en_cok_kazandiranlar_df['Hisse'], en_cok_kazandiranlar_df['Yuzde_Degisim'])
    ax.set_xlabel('Hisseler')
    ax.set_ylabel('Yüzde Değişim')
    ax.set_title('En Çok Kazandıran Hisseler')
    plt.xticks(rotation=45, ha='right')

    st.pyplot(fig)



secim2 = st.sidebar.selectbox("Tahmin Edilecek Birimi Seç", liste)
baslangic2 = datetime(1995, 1, 1)
bitis2 = datetime.now()
tahminitarih = st.sidebar.date_input("Tahmin Edilecek Tarihi Gir", min_value=datetime.now(),max_value=date(2060,1,1))
getirtahmin = st.sidebar.button("Tahmin et")

if getirtahmin:
    df2 = yf.download(secim2, baslangic2, bitis2)
    dft2 = df2[['Close']]
    df2 = df2.reset_index()
    df2.rename(columns={'Date': 'ds', 'Close': 'y'}, inplace=True)
    model = Prophet()
    model.fit(df2)
    tahminitarih_datetime = datetime.combine(tahminitarih, datetime.min.time())
    periodss = (tahminitarih_datetime - datetime.now()).days + 1

    total_seconds = periodss * 86400
    years, remainder = divmod(total_seconds, 31536000)
    months, remainder = divmod(remainder, 2592000)
    days, remainder = divmod(remainder, 86400)


    future = model.make_future_dataframe(periods=periodss)
    forecast = model.predict(future)

    forecast_table=forecast.rename(columns={'ds':'Tarih','yhat':'Tahmini Fiyat'})
    forecast_table['Tarih'] = pd.to_datetime(forecast_table['Tarih'])


    forecast_table['Tarih'] = forecast_table['Tarih'].dt.strftime('%Y-%m-%d')
    st.write(forecast_table[['Tarih','Tahmini Fiyat']].tail(3),index=False)

    fig1 = model.plot(forecast)
    st.markdown("<p style='text-align: center;'>{0} Tarihinin Tahmin Grafiği</p>".format(tahminitarih),
                unsafe_allow_html=True)
    st.pyplot(fig1)
    st.write(f"Tahmin Tarihine Kalan Süre : {years} yıl, {months} ay, {days} gün")
    st.write(f"Tahmin Tarihine Toplam Kalan Gün : {periodss}")

    try:
        today_price = df2[df2['ds'].dt.date==date.today()]['y'].iloc[0]


        try:
            st.write(f"Seçtiğiniz {secim2} değerinin bugünkü fiyatı : {today_price}")
        except:
            st.write(f"Bugünkü {secim2} değerinin fiyat verisi bulunamadı.")

        try:
            forecast_date=datetime.combine(tahminitarih,time(0,0,0))
            forecast_value=forecast[forecast['ds']==forecast_date]['yhat'].iloc[0]
            forecast_date_v2=forecast_date.date()
        except:
            st.write('Veri Bulunamadı')

        try:
            st.write(f"Seçtiğiniz {secim2} değerinin {forecast_date_v2} Tarihinde Tahmin Edilen Fiyatı : {forecast_value}")
        except:
            st.write(f"Seçtiğinz {secim2} değerinin Tahmini bulunamadı")
    except:
        st.write('Veri bulunamadı')

