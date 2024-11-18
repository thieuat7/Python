import pymysql
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd  # Nhập khẩu Pandas để xử lý chuỗi thời gian

def get_gold_prices():
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='',  # Thay đổi password nếu có
        database='crawl-vang',
        cursorclass=pymysql.cursors.DictCursor
    )
    
    data = {}
    
    try:
        with connection:
            with connection.cursor() as cursor:
                sql = "SELECT Day, Loai_Vang, Gia_mua, Gia_ban FROM `giá vàng` ORDER BY Day ASC"
                cursor.execute(sql)
                results = cursor.fetchall()
                
                # Tổ chức dữ liệu theo loại vàng
                for row in results:
                    if row['Loai_Vang'] not in data:
                        data[row['Loai_Vang']] = {'dates': [], 'purchase_prices': [], 'selling_prices': []}
                    
                    data[row['Loai_Vang']]['dates'].append(pd.to_datetime(row['Day']))  # Chuyển đổi thành datetime
                    data[row['Loai_Vang']]['purchase_prices'].append(float(row['Gia_mua']))
                    data[row['Loai_Vang']]['selling_prices'].append(float(row['Gia_ban']))
    finally:
        if connection.open:
            connection.close()
    
    return data

def plot_gold_prices():
    data = get_gold_prices()
    
    plt.figure(figsize=(15, 8))

    colors = plt.cm.Dark2(np.linspace(0, 1, len(data)))

    for (loai_vang, values), color in zip(data.items(), colors):
        # Vẽ đường kẻ liền cho giá mua
        plt.plot(values['dates'], values['purchase_prices'], label=f'Giá Mua - {loai_vang}', linestyle='-', color=color)
        # Vẽ đường nét đứt cho giá bán
        plt.plot(values['dates'], values['selling_prices'], label=f'Giá Bán - {loai_vang}', linestyle='--', color=color)

    plt.title('Biểu Đồ Giá Vàng Theo Ngày (Chuỗi Thời Gian)')
    plt.xlabel('Ngày')
    plt.ylabel('Giá (VND)')
    plt.xticks(rotation=45)
    
    # Thêm ghi chú bên ngoài khu vực biểu đồ
    plt.legend(loc='upper left', fontsize='small', frameon=False, bbox_to_anchor=(1, 1))

    plt.tight_layout()
    plt.show()

# Gọi hàm vẽ biểu đồ
plot_gold_prices()
