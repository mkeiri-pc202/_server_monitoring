import os

class Config(object):
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    INSTANCE_DIR = "instance"
    
    if not os.path.exists(INSTANCE_DIR):
        os.makedirs(INSTANCE_DIR)
    
    # os.getcwd()はVSCodeでフォルダを開くときに指定したPathが入る（ターミナルの中のPathを変えると動かない）
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(os.getcwd(), 'instance', 'server_status.sqlite') 
