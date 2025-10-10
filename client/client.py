import requests
import time
import psutil
import socket
# import send_e_mail

# POST先は仮でlocalhost→受信側のIPアドレスに変更が必要
POST_URL = 'http://localhost:5000/api/status'
hostname = socket.gethostname()

def get_status():
    """CPU使用率、メモリ使用率、ディスク空き容量を取得して数値で返す
    
    Returns:
        tuple: 以下の3つの値を含むタプル
            - cpu (float): CPU使用率(%)
            - memory (float): メモリ使用率(%)
            - disk (float): ディスクの空き容量(GB)
    """
    cpu = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory().percent
    disk = psutil.disk_usage('C:\\').free / (1024 ** 3)
    return cpu, memory, disk


def send_status():
    """
    取得したステータスをJSON形式で指定先のサーバにPOST送信する
    
    送信データには、サーバID、CPU使用率、メモリ使用率、ディスク空き容量が含まれる
    サーバの応答が正常でなければ、エラーメッセージを返す。 
    """
    cpu, memory, disk = get_status()
    data = {
        'server_id': hostname,
        'cpu': cpu,
        'memory': memory,
        'disk_free_gb': disk
    }
    try:
        r = requests.post(POST_URL, json=data)
        if r.status_code != 200:
            print(f'Unexpected response: {r.text}')
        else:
            print(f"[送信] CPU: {cpu}%, MEM: {memory}%, DISK: {disk}GB → {r.status_code}")
    except Exception as e:
        print(f'Error sending status: {e}')
        # send_e_mail.mail_send()


if __name__ == '__main__':
    """
    10秒ごとにステータスを取得・送信を行う監視ループを開始する。

    ループの停止はCtrl+Cを押下。
    """
    try:
        while True:
            send_status()
            time.sleep(10)
    except KeyboardInterrupt:
        print('End')