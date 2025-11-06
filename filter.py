from app import app

# --------------------------
# ✅ Flaskのfilter条件(小数点以下の表示の調整）
# --------------------------

@app.template_filter('datetime_format')
def datetime_format(dt): 
    return dt.strftime('%Y/%m/%d %H:%M:%S')

@app.template_filter('number_format')
def number_format(number): 
    return "{:.1f}".format(number)
