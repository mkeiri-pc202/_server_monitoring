import win32com.client


outlook = win32com.client.Dispatch('Outlook.Application')
mail = outlook.CreateItem(0)

mail.to = 'matsumotokeiri_hirasawa@outlook.jp'
mail.subject = 'エラー発生メール'
mail.bodyFormat = 1
mail.body = '''
これはPythonから送信されたメールです。
'''


if __name__ == '__main__':
    try:
        mail.Send()
        print('メールを送信しました。')
    except Exception as e:
        print(f"エラー: メールの送信に失敗しました。 - {e}")
