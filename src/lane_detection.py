import cv2
import numpy as np
import matplotlib.pyplot as plt
import time

def convert_to_gray(image):
  
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

def apply_blur(image, kernel_size=(5, 5)):
   
    return cv2.GaussianBlur(image, kernel_size, 0)

def detect_edges(image, low_threshold=50, high_threshold=150):
   
    return cv2.Canny(image, low_threshold, high_threshold)

def region_of_interest(image):
    
    height = image.shape[0]
    width = image.shape[1]
    
    # Dinamik olarak bir üçgen/yamuk bölge tanımlama
    # Sol alt, Sağ alt ve orta-üst nokta
    polygons = np.array([
        [(0, height), (width, height), (width // 2, height // 2)]
    ])
    
    # Görüntü boyutunda siyah bir maske oluşturduk
    mask = np.zeros_like(image)
    
    # Tanımladığımız bölgeyi beyaza boyadık (255)
    cv2.fillPoly(mask, polygons, 255)
    
    # Orijinal kenar görüntüsü ile maskeyi "VE" işlemine sokma
    masked_image = cv2.bitwise_and(image, mask)
    return masked_image, mask # Maskeyi de görselleştirmek için döndürüyoruz

def detect_lines(image):
    """
    Maskelenmiş kenar görüntüsünden çizgileri bulur.
    """

    lines = cv2.HoughLinesP(
        image, 
        rho=2, 
        theta=np.pi/180, 
        threshold=100, 
        minLineLength=40, 
        maxLineGap=5
    )
    return lines

def average_slope_intercept(image, lines):
    """
    Bulunan çizgileri eğimlerine göre sol ve sağ olarak ayırır ve tek bir çizgiye indirger.
    """
    left_fit = []
    right_fit = []
    
    if lines is None:
        return None

    for line in lines:
        for x1, y1, x2, y2 in line:
            
            parameters = np.polyfit((x1, x2), (y1, y2), 1)
            slope = parameters[0]
            intercept = parameters[1]
            
        
            if slope < 0:
                left_fit.append((slope, intercept))
            else:
                right_fit.append((slope, intercept))
                
    # Sol ve sağ çizgilerin ortalamasını alma
    left_fit_average = np.average(left_fit, axis=0) if left_fit else None
    right_fit_average = np.average(right_fit, axis=0) if right_fit else None
    
    return np.array([left_fit_average, right_fit_average], dtype=object)

def make_coordinates(image, line_parameters):
    """Eğim ve kaymadan tam sayı koordinat üretir."""
    if line_parameters is None: return None
    
    slope, intercept = line_parameters
    y1 = image.shape[0] # Alt sınır
    y2 = int(y1 * (3/5)) # Üst sınır (Görüntünün %60'ı)
    
    # Koordinatları hesaplama ve  int() ile tamsayıya çevirme
    x1 = int((y1 - intercept) / slope)
    x2 = int((y2 - intercept) / slope)
    
    return np.array([x1, y1, x2, y2])

def display_lines(image, lines_params):
    """Çizgileri boş bir siyah ekrana çizer."""
    line_image = np.zeros_like(image)
    if lines_params is not None:
        # Sol Şerit: Mavi , Sağ Şerit: Kırmızı 
        colors = [(255, 0, 0), (0, 0, 255)] 
        for i, line_p in enumerate(lines_params):
            coords = make_coordinates(image, line_p)
            if coords is not None:
                x1, y1, x2, y2 = coords
                cv2.line(line_image, (x1, y1), (x2, y2), colors[i], 10)
    return line_image

def process_frame(image):
    """
    Tüm aşamaları birleştirir: Tek bir kareyi alır, işler ve sonucu döndürür.
    """
    # 1. Ön İşleme
    gray = convert_to_gray(image)
    blurred = apply_blur(gray)
    edges = detect_edges(blurred)
    
    # 2. Maskeleme
    masked_edges, _ = region_of_interest(edges)
    
    # 3. Çizgi Tespiti
    lines = detect_lines(masked_edges)
    averaged_lines = average_slope_intercept(image, lines)
    
    # 4. Görselleştirme
    line_image = display_lines(image, averaged_lines)
    combo_image = cv2.addWeighted(image, 0.8, line_image, 1, 1)
    
    return combo_image

def process_video(video_path):
    cap = cv2.VideoCapture(video_path)
    prev_time = 0

    fps_display = 0
    frame_count = 0 
    
    if not cap.isOpened():
        print("Hata: Video dosyası açılamadı!")
        return

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret: break
            
        # STABİL FPS HESAPLAMA
        current_time = time.time()
        frame_count += 1
        
        # Her 10 karede bir FPS değerini güncelle (Gözün takip edebileceği hız)
        if frame_count % 10 == 0:
            if prev_time != 0:
                fps_display = 10 / (current_time - prev_time)
            prev_time = current_time
            
        try:
            processed_frame = process_frame(frame)
            
            cv2.putText(processed_frame, f"FPS: {int(fps_display)}", (30, 60), 
                        cv2.FONT_HERSHEY_DUPLEX, 1.2, (0, 255, 100), 2)
            
            cv2.imshow('Serit Tespiti - Kaptan', processed_frame)
        except Exception as e:
            print(f"Hata: {e}")
            continue 
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
            
    cap.release()
    cv2.destroyAllWindows()

def average_slope_intercept(image, lines):
    left_fit = []
    right_fit = []
    if lines is None: return None

    for line in lines:
        for x1, y1, x2, y2 in line:
            parameters = np.polyfit((x1, x2), (y1, y2), 1)
            slope = parameters[0]
            intercept = parameters[1]
            
            # FİLTRELEME 
            if abs(slope) < 0.5: 
                continue
                
            if slope < 0: 
                left_fit.append((slope, intercept))
            else: 
                right_fit.append((slope, intercept))
    
    # Ortalamaları alırken hata almamak için kontrol
    left_fit_average = np.average(left_fit, axis=0) if len(left_fit) > 0 else None
    right_fit_average = np.average(right_fit, axis=0) if len(right_fit) > 0 else None
    
    return [left_fit_average, right_fit_average]

# TEST ETME VE GÖRSELLEŞTİRME
image_path = 'test_images/test_yol.webp' 
image = cv2.imread(image_path)

if image is None:
    print("Hata: Resim bulunamadı!")
else:
    print("Önce analiz görseli açılıyor... (Kapatınca video başlayacak)")
   
    gray = convert_to_gray(image)
    blurred = apply_blur(gray)
    edges = detect_edges(blurred)
    masked_edges, _ = region_of_interest(edges)
    lines = detect_lines(masked_edges)
    averaged_lines = average_slope_intercept(image, lines)
    line_image = display_lines(image, averaged_lines)
    final_image = cv2.addWeighted(image, 0.8, line_image, 1, 1)

    # Resmi göster
    plt.figure(figsize=(10, 6))
    plt.imshow(cv2.cvtColor(final_image, cv2.COLOR_BGR2RGB))
    plt.title("Analiz Tamam! Bu pencereyi kapatın, video baslayacak...")
    plt.axis('off')
    plt.show() 

# VİDEO TETİKLEYİCİ
print("Video başlatılıyor...")
video_input = 'test_images/surus_videosu2.mp4' 
process_video(video_input)