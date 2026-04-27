# Gerçek Zamanlı Şerit Tespiti Sistemi

Bu proje, otonom araç teknolojileri ve yapay zeka güvenliği alanındaki kişisel Ar-Ge çalışmalarımın ilk yapı taşıdır. Bilgisayarlı görü (Computer Vision) tekniklerini kullanarak, dinamik yol koşullarında şeritlerin stabil ve güvenilir bir şekilde tespit edilmesini hedefler.

#  Kullanılan Teknolojiler
* **Python 3.8+**
* **OpenCV:** Görüntü işleme pipeline'ı için.
* **NumPy:** Matris işlemleri ve koordinat hesaplamaları için.
* **Matplotlib:** Analiz aşamalarını görselleştirmek için.

# Algoritma Aşamaları
1. **Gri Tonlama:** Renk karmaşıklığını azaltarak işlem hızını artırmak için kullanıldı.
2. **Gaussian Blur:** Görüntüdeki gürültüyü (noise) azaltarak kenar tespitinin başarısını artırdı.
3. **Canny Edge Detection:** Yoğunluk değişimlerini yakalayarak yol üzerindeki kenarları çıkardım.
4. **ROI (Region of Interest):** Sadece yolun bulunduğu alt yamuk alana odaklanarak hatalı tespitleri eledim.
5. **Hough Transform:** Piksel noktalarını geometrik çizgilere dönüştürdüm.
6. **Eğim Filtreleme:** Yatay çizgileri eleyerek sadece gerçek şeritleri stabilize ettim.

# Parametre Seçimleri
* **Canny Threshold (50, 150):** Deneme-yanılma sonucunda gün ışığında şeritlerin en belirgin olduğu değerler olarak belirlendi.
* **Hough Threshold (100):** Çizgi sürekliliğini sağlamak için optimize edildi.

# Sistemin Sınırları
Algoritma, şeritlerin silik olduğu eski yollarda veya aşırı güneş parlaması olan durumlarda bazen hassasiyet kaybı yaşamaktadır. Geliştirme aşamasında "Moving Average" eklenerek titremeler daha da azaltılabilir.