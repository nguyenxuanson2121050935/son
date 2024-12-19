import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix, classification_report, accuracy_score

# Đọc file CSV
df = pd.read_excel('dataFaker.xlsx')
print(df.columns)
df.columns = df.columns.str.strip()
df = pd.get_dummies(df, columns=['tinhtrang'], drop_first=True)
print(df.head())

# Xác định các đặc trưng (features) và nhãn (target)
X = df[['tuoi', 'thunhap(usd)', 'sotienvay(usd)', 'time', 'diemtindung', 'tinhtrang_Unemployed']]  # các đặc trưng
y = df['ketqua']  # nhãn mục tiêu

# Chia dữ liệu thành tập huấn luyện và kiểm tra
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Chuẩn hóa dữ liệu
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Tạo mô hình Logistic Regression
model = LogisticRegression()
model.fit(X_train_scaled, y_train)

# Dự đoán kết quả trên tập kiểm tra
y_pred = model.predict(X_test_scaled)

# Đánh giá mô hình
print("Đánh giá mô hình:")
print("Ma trận nhầm lẫn:")
print(confusion_matrix(y_test, y_pred))
print("\nBáo cáo phân loại:")
print(classification_report(y_test, y_pred))
print(f"Độ chính xác: {accuracy_score(y_test, y_pred)}")
# Dữ liệu mới
# Tạo dữ liệu mới sao cho khớp với các cột đã được xử lý
new_data = pd.DataFrame([[30, 5000, 20000, 24, 600, 0]], columns=['tuoi', 'thunhap(usd)', 'sotienvay(usd)', 'time', 'diemtindung', 'tinhtrang_Unemployed'])  # 0 cho 'Unemployed' (Employed = 1)
new_data_scaled = scaler.transform(new_data)
# Dự đoán kết quả cho dữ liệu mới
prediction = model.predict(new_data_scaled)

# In ra kết quả dự đoán
print(f"Dự đoán cho dữ liệu mới: {'Có thể trả nợ' if prediction[0] == 1 else 'Không thể trả nợ'}")
