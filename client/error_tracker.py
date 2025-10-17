import send_e_mail

class ErrorTracker:
    """エラーの連続発生を監視、指定回数に達した場合にメール通知を行うクラス
    
    Attributes:
        last_error_msg(str or None): 最後に記録されたエラーメッセージ
        error_count(int): 同じエラーが連続して発生した回数
        threshold(int): メール通知を行う連続エラー回数
    """

    def __init__(self, threshold=5):
        """ErrorTrackerを初期化

        Args:
            threshold(int, optional): メール送信を行うまでの連続エラー回数
        """
        self.last_error_msg = None
        self.error_count = 0
        self.threshold = threshold

    def check_error(self, msg):
        """前回と同じエラーが連続して発生しているか判定

        同じエラーメッセージが'threshold'回連続で発生した場合、
        メールを送信する

        Args:
            msg(str): 現在発生したエラーメッセージ
        """
        if msg == self.last_error_msg:
            self.error_count += 1
        else:
            self.last_error_msg = msg
            self.error_count = 1
        
        if self.error_count == self.threshold:
            send_e_mail.send_mail(msg)