import smtplib
from email.mime.text import MIMEText

def mail_send():
# メール情報
    sender = 'matsumotokeiri_hirasawa@outlook.jp'
    receiver = '@outlook.jp'
    subject = 'テストメール'
    body = 'これはPythonから送信されたメールです。'
# メール作成
    msg = MIMEText(body, 'plain', 'utf-8')
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = receiver

# SMTPサーバへ接続
    smtp_server = 'smtp-mail.outlook.com'
    smtp_port = 587
    password = 'ここにアプリパスワードを入力'  # 「アプリパスワード」を使用

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender, password)
            server.send_message(msg)
        print("メールを送信しました。")

    except Exception as e:
        print(f"エラー: メールの送信に失敗しました。 - {e}")


if __name__ == '__main__':
    mail_send()
