import win32com.client

def send_mail(msg):
    """Outlook を使用してエラーメッセージをメール送信する。

    エラーに応じて指定されたメッセージを本文に含めて、固定の宛先にメールを送信
    Outlookをwindowsにインストールして、
    win32com.clientライブラリをインストール、COMオブジェクトが利用可能にする必要がある

    Args:
        msg (str): 送信するエラーメッセージでメール本文に挿入
    Raises:
        Exception: メール送信に失敗した場合、例外情報をプロンプトに表示
    """
    outlook = win32com.client.Dispatch("Outlook.Application")
    mail = outlook.CreateItem(0)

    mail.to = "matsumotokeiri_hirasawa@outlook.jp"
    mail.subject = "エラー発生メール"
    mail.bodyFormat = 1
    mail.body = "エラー発生" \
                f"{msg}"

    try:
        mail.Send()
        print(f"メールを送信しました: {msg}")
    except Exception as e:
        print(f"送信エラー: メールの送信に失敗しました。 - {e}")