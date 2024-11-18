import pandas as pd
import pymysql

# Đường dẫn tới file CSV của bạn
csv_file_path = 'file.csv'  # Đảm bảo file CSV nằm cùng thư mục với file code

# Kết nối tới database MySQL
connection = pymysql.connect(
    host='localhost',
    user='root',
    password='',
    database='crawl-vang',
    cursorclass=pymysql.cursors.DictCursor
)

try:
    # Đọc dữ liệu từ file CSV
    with open(csv_file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    
    data = []
    record_id_base = 1  # Biến để tạo ID cho mỗi loại vàng
    
    for line in lines:
        line = line.strip()
        if not line:  # Bỏ qua các dòng trống
            continue
        
        # Kiểm tra xem dòng có phải là thời gian hay không
        try:
            # Nếu dòng này có thể chuyển đổi thành datetime, thì đây là thời gian
            day = pd.to_datetime(line).normalize()
            formatted_day = day.strftime('%d%m') + str(day.year)  # Định dạng ngày
            record_id_base = 1  # Reset ID cho mỗi ngày mới
        except ValueError:
            # Nếu không phải là thời gian, nghĩa là đây là thông tin loại vàng
            parts = line.split(', ')
            if len(parts) == 3:  # Kiểm tra có đúng 3 phần không
                loai_vang = parts[0].strip()
                gia_mua = float(parts[1].replace(',', '').strip())
                gia_ban = float(parts[2].replace(',', '').strip())
                
                # Tạo ID bằng cách ghép vị trí và ngày
                record_id = int(f"{record_id_base}{formatted_day}")
                print(record_id)
                data.append((record_id, loai_vang, gia_mua, gia_ban, day))
                record_id_base += 1  # Tăng ID cho loại vàng tiếp theo

    # Chèn dữ liệu vào database
    with connection.cursor() as cursor:
        sql = """
            INSERT INTO `giá vàng`(`ID`, `Loai_Vang`, `Gia_mua`, `Gia_ban`, `Day`)
            VALUES (%s, %s, %s, %s, %s)
            """
        cursor.executemany(sql, data)  # Chèn tất cả dữ liệu cùng một lúc
        print(f"Chèn {cursor.rowcount} dòng dữ liệu thành công!")  # In số dòng đã chèn
    connection.commit()  # Lưu các thay đổi

finally:
    connection.close()  # Đóng kết nối
