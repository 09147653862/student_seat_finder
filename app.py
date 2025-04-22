from flask import Flask, request, render_template
import pandas as pd
import os

app = Flask(__name__)

# مسیر ذخیره فایل اکسل
EXCEL_FILE = 'data.xlsx'

# مسیر برای پینگ کردن و جلوگیری از Sleep
@app.route('/ping')
def ping():
    return 'OK'

# صفحه اصلی برای دانشجو
@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    if request.method == 'POST':
        student_id = request.form.get('student_id')
        if student_id:
            try:
                # خواندن فایل اکسل
                df = pd.read_excel(EXCEL_FILE)
                # جستجوی شماره دانشجویی
                student_data = df[df['شماره دانشجويي'] == int(student_id)]
                if not student_data.empty:
                    # تبدیل داده‌ها به دیکشنری
                    result = student_data.to_dict(orient='records')[0]
                else:
                    result = {'error': 'شماره دانشجویی یافت نشد!'}
            except Exception as e:
                result = {'error': f'خطا: {str(e)}'}
    return render_template('index.html', result=result)

# صفحه آپلود فایل برای ادمین
@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        if file and file.filename.endswith('.xlsx'):
            file.save(EXCEL_FILE)
            return 'فایل با موفقیت آپلود شد!'
        else:
            return 'لطفاً فایل اکسل معتبر آپلود کنید!'
    return render_template('upload.html')

if __name__ == '__main__':
    app.run(debug=True)