import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

st.set_page_config(page_title="EVAP KPI Summary Dashboard", layout="wide")

# ระบบล็อกอิน

def login():
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False

    if not st.session_state['logged_in']:
        st.title("EVAP KPI Dashboard")
        password = st.text_input("กรุณาใส่รหัสผ่าน", type="password")
        login_button = st.button("เข้าสู่ระบบ")

        if login_button and password == "1234":
            st.session_state['logged_in'] = True
            st.success("เข้าสู่ระบบสำเร็จ กำลังโหลด Dashboard...")
            st.rerun()
        elif login_button:
            st.error("รหัสผ่านไม่ถูกต้อง")
            st.stop()

login()

if st.session_state['logged_in']:

    @st.cache_data(ttl=600)
    def load_csv(url):
        return pd.read_csv(url)

    csv_urls = [
        "https://docs.google.com/spreadsheets/d/1JH0EPswBM7lNBhmsVhnwMMOmYVfwlSiATDmOz0jCnX4/export?format=csv",
        "https://docs.google.com/spreadsheets/d/1DkMr_9kGuF3KfbDU-rfJZWGn_oUX2C7d-dA9oTGtL5E/export?format=csv",
        "https://docs.google.com/spreadsheets/d/1Lay7VNiSlzunevei2fYR3H06dORhXXto3omDerY23nw/export?format=csv",
        "https://docs.google.com/spreadsheets/d/191J-NG-I6q2At2ONBYn8pdQTAftw4bHYpc4XFqNMtS8/export?format=csv",
        "https://docs.google.com/spreadsheets/d/1IaAIlRN0MYFLhsXLJmu8O2ml7TGkhSCyoshj7P240D4/export?format=csv",
        "https://docs.google.com/spreadsheets/d/1udvbSTVB1HvAqMzSl3wtgmZ_ZIxCzwCWR3lf-MU_cCQ/export?format=csv",
        "https://docs.google.com/spreadsheets/d/1nu2bG5zEmDWjzy6ar0j8WkIt56186nElbjUg2a7weK4/export?format=csv",
        "https://docs.google.com/spreadsheets/d/1wsDHOKBY_Tfa59fRIdIzgrz6nXA_WOaINR7Cjjjb3t4/export?format=csv",
        "https://docs.google.com/spreadsheets/d/1I5KxcifJkI7jMgGyAsnJ6dYqTNHoqICv7VUWmmjj34A/export?format=csv",
        "https://docs.google.com/spreadsheets/d/1mH7Yw-CmG6A3pS3fTSzJyquTFnd170nu55jpjnQIioA/export?format=csv",
        "https://docs.google.com/spreadsheets/d/18UZNJcwVzUne_TFBEtW4JRJjJ6bWBE7L3fVXcKm5rQ8/export?format=csv",
        "https://docs.google.com/spreadsheets/d/1NAr6psLk1LOch-n9L2Ik8wcmGeVbKunygIFQ9eq7p9o/export?format=csv",
        "https://docs.google.com/spreadsheets/d/1yedPJ_XdE_ILRIIlz091uaI1YPrbYSIypWJhThxYQ3w/export?format=csv",
        "https://docs.google.com/spreadsheets/d/1epYB4NT8eJ6mGZNZO9InAZyz9Fj-FN8TPouuTQYkh0A/export?format=csv",
        "https://docs.google.com/spreadsheets/d/1p6gb4D-TzbIBJIaRI7mBrWYvXx3DreP0dpVpfoBuEh8/export?format=csv",
        "https://docs.google.com/spreadsheets/d/1nZ0VHDqwuLquxEf8HCSxZze5E3PcVCVKfs9rgr7F-mg/export?format=csv",
        "https://docs.google.com/spreadsheets/d/14V20TFT-yx4EqbyP8ravb_DjbH1eAbcL_VZLT00naKA/export?format=csv",
        "https://docs.google.com/spreadsheets/d/1MZVCsAOwSjYp6BJxDZvR1UbrP5UFFOZpn_ZZjSI_nVw/export?format=csv",
        "https://docs.google.com/spreadsheets/d/1KEHfxVhIVq7NOaTN46KNz7HVrYddiI6_WBB-JARX7UE/export?format=csv",
        "https://docs.google.com/spreadsheets/d/1QOft1va-2b_-EVnX-VyOjjvXmDFtfalmXKRriXcLQYc/export?format=csv",
        "https://docs.google.com/spreadsheets/d/1QZ8tKQUZ-pzFQR5Eul-hwmfYucpNgJAYxw0GB8pB-B4/export?format=csv",
        "https://docs.google.com/spreadsheets/d/1hRlVqhagzaD3mIbsZan9_3yKV3LtumZ-oFS2W6mWzuk/export?format=csv"
    ]

    zone_mapping = ['BL-PP']*3 + ['CT-PP']*9 + ['IND-BL']*4 + ['IND-CT']*6
    machine_mapping = ['No.1', 'No.2', 'No.3'] + ['No.1', 'No.2', 'No.3', 'No.4', 'No.5', 'No.6', 'No.7', 'No.8', 'No.9'] + ['No.1', 'No.2', 'No.3', 'No.4'] + ['No.1', 'No.2', 'No.3', 'No.4', 'No.5', 'No.6']

    all_data = []
    for idx, url in enumerate(csv_urls):
        try:
            df = load_csv(url)
            df['Zone'] = zone_mapping[idx]
            df['Machine'] = machine_mapping[idx]
            all_data.append(df)
        except Exception as e:
            st.error(f"โหลดไม่ได้: {url}\n{e}")

    if all_data:
        df_all = pd.concat(all_data, ignore_index=True)
    else:
        st.stop()

    if 'ประทับเวลา' in df_all.columns:
        df_all['Date'] = pd.to_datetime(df_all['ประทับเวลา'], errors='coerce')
        df_all['Month'] = df_all['Date'].dt.to_period('M').astype(str)
        df_all['Day'] = df_all['Date'].dt.date

    check_cols = [col for col in df_all.columns if 'ตรวจเช็ค' in col]
    if not check_cols:
        st.warning("ไม่พบข้อมูลการตรวจเช็ค")
        st.stop()

    melted = df_all.melt(id_vars=['Zone', 'Machine', 'Month', 'Day'], value_vars=check_cols, var_name='Check Item', value_name='Status')
    melted = melted[melted['Status'].isin(['ปกติ', 'ผิดปกติ'])]

    st.title("วิเคราะห์ KPI รายเดือนแยกตามโซน")
    zones = sorted(melted['Zone'].unique().tolist())
    selected_zone = st.selectbox("เลือกโซน", zones)
    months = sorted(melted['Month'].dropna().unique().tolist())
    selected_month = st.selectbox("เลือกเดือน", months)

    zone_df = melted[(melted['Zone'] == selected_zone) & (melted['Month'] == selected_month)]
    if zone_df.empty:
        st.warning("ไม่มีข้อมูลสำหรับโซนและเดือนที่เลือก")
        st.stop()

    # KPI รวมของเครื่องในโซน
    kpi_by_machine = zone_df.groupby(['Machine', 'Status']).size().reset_index(name='Count')
    total_machine = kpi_by_machine.groupby('Machine')['Count'].transform('sum')
    kpi_by_machine['Percent'] = (kpi_by_machine['Count'] / total_machine * 100).round(2)

    st.subheader(f"KPI เครื่องทั้งหมดในโซน {selected_zone} ประจำเดือน {selected_month}")
    fig_bar = px.bar(
        kpi_by_machine,
        x='Machine',
        y='Percent',
        color='Status',
        color_discrete_map={'ปกติ': 'blue', 'ผิดปกติ': 'red'},
        barmode='group',
        text='Percent',
        title="กราฟแท่งแสดงเปอร์เซ็นต์สถานะของแต่ละเครื่อง"
    )
    fig_bar.update_traces(texttemplate='%{text}%', textposition='outside')
    fig_bar.add_shape(
        type='line',
        x0=-0.5, x1=len(kpi_by_machine['Machine'].unique()) - 0.5,
        y0=80, y1=80,
        line=dict(color='black', width=2, dash='dash'),
        xref='x', yref='y'
    )
    st.plotly_chart(fig_bar, use_container_width=True)

    # รวมข้อมูล Pie
    pie_summary = zone_df.groupby(['Status']).size().reset_index(name='Count')
    pie_total = pie_summary['Count'].sum()
    pie_summary['Percent'] = (pie_summary['Count'] / pie_total * 100).round(2)

    st.subheader("สรุปสถานะทั้งหมดในโซนเป็นเปอร์เซ็นต์")
    fig_pie = px.pie(pie_summary, names='Status', values='Percent', color='Status',
                    color_discrete_map={'ปกติ': 'blue', 'ผิดปกติ': 'red'},
                    title="สัดส่วนปกติ/ผิดปกติ ทั้งหมดในโซน")
    st.plotly_chart(fig_pie, use_container_width=True)

    # กราฟ Time Series รายวันในเดือน
    st.subheader("แนวโน้มสถานะรายวัน")
    ts_df = zone_df.groupby(['Day', 'Status']).size().reset_index(name='Count')
    fig_line = px.line(ts_df, x='Day', y='Count', color='Status', markers=True,
                       color_discrete_map={'ปกติ': 'blue', 'ผิดปกติ': 'red'},
                       title="จำนวนรายการปกติ/ผิดปกติ ตามวัน")
    st.plotly_chart(fig_line, use_container_width=True)
