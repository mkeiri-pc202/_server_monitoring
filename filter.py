from app import app

@app.template_filter('datetime_format')
def datetime_format(dt): # 
    return dt.strftime('%Y/%m/%d %H:%M:%S')

@app.template_filter('number_format')
def int(number): # 
    return "{:.1f}".format(number)