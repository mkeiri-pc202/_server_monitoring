import requests
import time
import psutil
import socket
# import send_e_mail

# POST先は仮でlocalhost→受信側のIPアドレスに変更が必要
POST_URL = 'http://localhost:5000/api/status'
hostname = socket.gethostname()

def get_status():
    """
    CPU使用率、メモリ使用率、ディスク空き容量を取得して数値で返す
    取得時に問題が発生した場合は、エラーメッセージを返す

    Returns:
        tuple: 以下の3つの値を含むタプル
            - cpu (float): CPU使用率(%)
            - memory (float): メモリ使用率(%)
            - disk (float): ディスクの空き容量(GB)
    """
    try:
        cpu = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory().percent
        disk = psutil.disk_usage('C:\\').free / (1024 ** 3)
        return cpu, memory, disk
    except Exception as e:
        error_msg = f'ステータス取得エラー: {type(e).__name__} - {e}'
        print(error_msg)
        return None, None, None


def send_status():
    """
    取得したステータスをJSON形式で指定先のサーバにPOST送信する
    
    送信データには、サーバID、CPU使用率、メモリ使用率、ディスク空き容量が含まれる
    サーバの応答が正常でなければ、問題に応じてエラーメッセージを返す 
    """
    cpu, memory, disk = get_status()
    if None in (cpu, memory, disk):
        print("取得失敗のため送信をスキップ")
        return
    data = {
        'server_id': hostname,
        'cpu': cpu,
        'memory': memory,
        'disk_free_gb': disk
    }

    try:
        r = requests.post(POST_URL, json=data, timeout=5)
        r.raise_for_status()
        print(f"[送信] CPU: {cpu}%, MEM: {memory}%, DISK: {disk}GB → {r.status_code}")
    except requests.exceptions.Timeout as e:
        msg = f"タイムアウト: {e}"
        print(msg)
    except requests.exceptions.ConnectionError as e:
        msg = f"接続エラー: {e}"
        print(msg)
    except requests.exceptions.HTTPError as e:
        msg = f"HTTPエラー: {e}"
        print(msg)
        # send_e_mail.mail_send(msg)
    except requests.exceptions.RequestException as e:
        msg = f"その他の通信エラー: {e}"
        print(msg)


if __name__ == '__main__':
    """
    10秒ごとにステータスを取得・送信を行う監視ループを開始する

    ループの停止はCtrl+Cを押下
    """
    try:
        while True:
            send_status()
            time.sleep(10)
    except KeyboardInterrupt:
        print('End')