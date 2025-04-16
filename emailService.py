import imaplib
import email
import smtplib
from email.header import decode_header, make_header
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import os
from typing import List, Dict, Optional, Union
from queue import Queue
import threading
import time

# 邮箱配置
EMAIL_HOST = "imap.qq.com"
EMAIL_PORT = 993
SMTP_HOST = "smtp.qq.com"
SMTP_PORT = 587
EMAIL_USERNAME = "jfkfd@qq.com"
EMAIL_PASSWORD = "ckmuumrnoylybbge"

class SMTPConnection:
    def __init__(self, host, port, username, password):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.connection = None
        self.last_used = 0
        self.lock = threading.Lock()

    def connect(self):
        """建立SMTP连接"""
        if self.connection is None:
            self.connection = smtplib.SMTP(self.host, self.port)
            self.connection.starttls()
            self.connection.login(self.username, self.password)
        return self.connection

    def disconnect(self):
        """断开SMTP连接"""
        if self.connection:
            try:
                self.connection.quit()
            except:
                pass
            finally:
                self.connection = None

    def get_connection(self):
        """获取连接，如果连接太久没用过就重新建立"""
        with self.lock:
            current_time = time.time()
            # 如果连接超过30秒没使用，重新建立连接
            if current_time - self.last_used > 30:
                self.disconnect()
            
            try:
                conn = self.connect()
                self.last_used = current_time
                return conn
            except Exception as e:
                self.disconnect()
                raise e

class SMTPConnectionPool:
    def __init__(self, host, port, username, password, pool_size=3):
        self.pool = Queue(maxsize=pool_size)
        for _ in range(pool_size):
            self.pool.put(SMTPConnection(host, port, username, password))

    def get_connection(self):
        """从池中获取一个连接"""
        return self.pool.get()

    def return_connection(self, conn):
        """将连接返回池中"""
        self.pool.put(conn)

class EmailService:
    def __init__(self):
        self.imap_conn = None
        self.smtp_conn = None

    def connect_to_imap(self):
        """连接到IMAP服务器"""
        if not self.imap_conn:
            self.imap_conn = imaplib.IMAP4_SSL(EMAIL_HOST, EMAIL_PORT)
            self.imap_conn.login(EMAIL_USERNAME, EMAIL_PASSWORD)
        return self.imap_conn

    def connect_to_smtp(self):
        """连接到SMTP服务器"""
        if not self.smtp_conn:
            self.smtp_conn = smtplib.SMTP(SMTP_HOST, SMTP_PORT)
            self.smtp_conn.starttls()
            self.smtp_conn.login(EMAIL_USERNAME, EMAIL_PASSWORD)
        return self.smtp_conn

    def get_messages_from_folder(self, folder_name: str) -> List[bytes]:
        """获取指定文件夹中的邮件ID列表"""
        mail = self.connect_to_imap()
        mail.select(folder_name)
        status, messages = mail.search(None, "ALL")
        return messages[0].split()

    def move_message_to_folder(self, email_id: bytes, source_folder: str, target_folder: str) -> bool:
        """移动指定邮件到目标文件夹"""
        mail = self.connect_to_imap()
        mail.select(source_folder)
        result = mail.copy(email_id, target_folder)
        if result[0] == 'OK':
            mail.store(email_id, '+FLAGS', '\\Deleted')
            mail.expunge()
            return True
        return False

    def get_email_info(self, email_id: bytes, folder_name: str) -> Dict[str, Union[str, List[str]]]:
        """获取指定邮件的详细信息"""
        mail = self.connect_to_imap()
        mail.select(folder_name)
        status, msg_data = mail.fetch(email_id, "(RFC822)")
        email_body = msg_data[0][1]
        msg = email.message_from_bytes(email_body)

        # 解码邮件主题
        subject = str(make_header(decode_header(msg.get("Subject", ""))))
        
        # 获取发件人和收件人
        from_addr = str(make_header(decode_header(msg.get("From", ""))))
        to_addr = str(make_header(decode_header(msg.get("To", ""))))
        
        # 获取Message-ID
        message_id = msg.get("Message-ID", "")

        # 获取正文内容
        body = ""
        attachments = []
        
        for part in msg.walk():
            if part.get_content_maintype() == "text" and not part.get_filename():
                # 获取文本内容
                charset = part.get_content_charset() or 'utf-8'
                body += part.get_payload(decode=True).decode(charset, errors='ignore')
            
            elif part.get_filename():
                # 获取附件信息
                filename = str(make_header(decode_header(part.get_filename())))
                attachment_info = {
                    "filename": filename,
                    "content_type": part.get_content_type(),
                    "size": len(part.get_payload(decode=True))
                }
                attachments.append(attachment_info)

        return {
            "message_id": message_id,
            "subject": subject,
            "from": from_addr,
            "to": to_addr,
            "body": body,
            "attachments": attachments
        }

    def extract_attachments(self, email_id: bytes, folder_name: str, save_path: str = "attachments") -> List[str]:
        """提取邮件附件并保存到指定目录"""
        if not os.path.exists(save_path):
            os.makedirs(save_path)

        mail = self.connect_to_imap()
        mail.select(folder_name)
        status, msg_data = mail.fetch(email_id, "(RFC822)")
        msg = email.message_from_bytes(msg_data[0][1])
        saved_files = []

        for part in msg.walk():
            if part.get_content_maintype() == 'multipart':
                continue
            if part.get('Content-Disposition') is None:
                continue

            filename = part.get_filename()
            if filename:
                filename = str(make_header(decode_header(filename)))
                filepath = os.path.join(save_path, filename)
                with open(filepath, "wb") as f:
                    f.write(part.get_payload(decode=True))
                saved_files.append(filepath)
        return saved_files

    def send_email(self, 
                   to_addr: Union[str, List[str]], 
                   subject: str, 
                   body: str, 
                   attachments: Optional[List[str]] = None) -> bool:
        """发送邮件，支持多个收件人和附件"""
        try:
            msg = MIMEMultipart()
            msg['From'] = EMAIL_USERNAME
            msg['To'] = to_addr if isinstance(to_addr, str) else ", ".join(to_addr)
            msg['Subject'] = subject

            # 添加邮件正文
            msg.attach(MIMEText(body, 'plain', 'utf-8'))

            # 添加附件
            if attachments:
                for attachment_path in attachments:
                    if os.path.exists(attachment_path):
                        with open(attachment_path, 'rb') as f:
                            attachment = MIMEApplication(f.read())
                            attachment.add_header(
                                'Content-Disposition', 
                                'attachment', 
                                filename=os.path.basename(attachment_path)
                            )
                            msg.attach(attachment)

            # 发送邮件
            smtp = self.connect_to_smtp()
            smtp.send_message(msg)
            self.closeSmtp()
            return True
        except Exception as e:
            print(f"发送邮件失败: {str(e)}")
            return False
    
    def closeSmtp(self):
        if self.smtp_conn:
            self.smtp_conn.quit()
            self.smtp_conn = None

    def close(self):
        """关闭所有连接"""
        if self.imap_conn:
            self.imap_conn.logout()
            self.imap_conn = None
        if self.smtp_conn:
            self.smtp_conn.quit()
            self.smtp_conn = None

def main():
    email_service = EmailService()
    try:
        # 示例用法
        folder_name = "INBOX"
        email_ids = email_service.get_messages_from_folder(folder_name)
        
        for email_id in email_ids:
            # 获取邮件信息
            email_info = email_service.get_email_info(email_id, folder_name)
            print(f"邮件主题: {email_info['subject']}")
            
            # 提取附件
            attachments = email_service.extract_attachments(email_id, folder_name)
            if attachments:
                print(f"已保存的附件: {attachments}")
    finally:
        email_service.close()

if __name__ == "__main__":
    main()