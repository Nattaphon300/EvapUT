
from flask import Flask, render_template, request, redirect, session, jsonify
import pandas as pd
import os

app = Flask(__name__)
app.secret_key = 'evap_secret_key'

data_path = "./data"

thai_months = {
    'January': 'มกราคม', 'February': 'กุมภาพันธ์', 'March': 'มีนาคม',
    'April': 'เมษายน', 'May': 'พฤษภาคม', 'June': 'มิถุนายน',
    'July': 'กรกฎาคม', 'August': 'สิงหาคม', 'September': 'กันยายน',
    'October': 'ตุลาคม', 'November': 'พฤศจิกายน', 'December': 'ธันวาคม'
}

def load_all_csv():
    all_data = []
    for filename in sorted(os.listdir(data_path)):
        file_path = os.path.join(data_path, filename)
        try:
            df = pd.read_csv(file_path)
            df.columns = df.columns.str.strip()
            if 'ประทับเวลา' in df.columns:
                df['วันที่'] = pd.to_datetime(df['ประทับเวลา'], errors='coerce')
                df['เดือน'] = df['วันที่'].dt.strftime('%B').map(thai_months)
            else:
                df['วันที่'] = pd.NaT
                df['เดือน'] = ''
            df['สถานะ'] = df.apply(lambda row: 'ผิดปกติ' if any('ผิดปกติ' in str(val) for val in row.values) else 'ปกติ', axis=1)

            name = filename.replace("(", "").replace(")", "").replace("EVAP", "").replace(".csv", "")
            zone = "PP-BL" if "PP" in name and "BL" in name else "PP-CT" if "PP" in name else "IND-BL" if "IND" in name and "BL" in name else "IND-CT"
            machine = f"เครื่อง {name.split('No.')[-1].split(' ')[0]}" if "No." in name else "ไม่รู้จักเครื่อง"

            df['โซน'] = zone.strip()
            df['เครื่อง'] = machine.strip()
            df['เดือน'] = df['เดือน'].fillna('').str.strip()
            df['สถานะ'] = df['สถานะ'].fillna('').str.strip()

            all_data.append(df[['วันที่', 'เดือน', 'สถานะ', 'โซน', 'เครื่อง']])
        except:
            continue
    return pd.concat(all_data, ignore_index=True) if all_data else pd.DataFrame()

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['username'] == 'UT' and request.form['password'] == '1234':
            session['user'] = request.form['username']
            return redirect('/dashboard')
        return render_template('login.html', error='เข้าสู่ระบบไม่สำเร็จ')
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect('/')
    return render_template('index.html')

@app.route('/api/data')
def api_data():
    if 'user' not in session:
        return jsonify([])
    df = load_all_csv()
    df = df[df['เดือน'].notna()]
    return df.to_dict(orient='records')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
