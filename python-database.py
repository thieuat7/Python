import pymysql
import pymysql.cursors
import requests
from bs4 import BeautifulSoup
import datetime

def my_join():
    # Kết nối đến cơ sở dữ liệu MySQL
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='',
        database='crawl-vang',
        cursorclass=pymysql.cursors.DictCursor
    )
    
    try:
        with connection:
            with connection.cursor() as cursor:
                # URL trang để lấy dữ liệu giá vàng
                url = 'https://www.pnj.com.vn/blog/gia-vang/?r=1726709709840'
                response = requests.get(url)
                
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')
                    table = soup.find('tbody', id='content-price')
                    rows = table.find_all('tr')
                    
                    # Lấy ngày hiện tại và định dạng thành ddmmyyyy
                    today = datetime.date.today()
                    date_str = today.strftime("%d%m%Y")  # Định dạng ddmmyyyy
                    
                    # Chuyển đổi date_str thành số nguyên
                    date_number = int(date_str)
                    
                    # Khởi tạo số thứ tự cho ngày hiện tại
                    stt = 1
                    
                    for row in rows:
                        columns = row.find_all('td')
                        name = columns[0].text.strip()
                        purchaseprice = columns[1].text.strip()
                        sellingprice = columns[2].text.strip()
                        
                        # Chuyển đổi giá mua và bán từ chuỗi thành số
                        purchaseprice = float(purchaseprice.replace(',', '').strip())
                        sellingprice = float(sellingprice.replace(',', '').strip())
                        
                        # Tạo ID bằng cách nhân số thứ tự với 1000000 và cộng với ngày
                        id_custom = stt * 10000000 + date_number
                        
                        print(id_custom, name, purchaseprice, sellingprice)
                        
                        # Thêm dữ liệu bao gồm ID tùy chỉnh và cột ngày
                        sql = """
                        INSERT INTO `giá vàng`(`ID`, `Loai_Vang`, `Gia_mua`, `Gia_ban`, `Day`)
                        VALUES (%s, %s, %s, %s, %s)
                        """
                        cursor.execute(sql, (id_custom, name, purchaseprice, sellingprice, today))
                        
                        # Tăng số thứ tự cho lần lặp tiếp theo
                        stt += 1
                    
                    connection.commit()
                    print("Chèn dữ liệu thành công!")
    finally:
        # Kiểm tra xem kết nối còn mở không trước khi đóng
        if connection.open:
            connection.close()

my_join()
