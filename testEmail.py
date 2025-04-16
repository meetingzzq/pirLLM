from emailService import EmailService

# 创建EmailService实例
email_service = EmailService()

try:


    email_service.send_email(
        to_addr="zqiang_zhu@163.com",
        subject="测试邮件",
        body="这是邮件正文",
        attachments=["C:/Users/Jay/Documents/cursor/Service/LLM/attachments/blue.jpg"]
    )

    # # 获取邮件信息
    # email_ids = email_service.get_messages_from_folder("error")
    # for email_id in email_ids:
    #     email_info = email_service.get_email_info(email_id, "error")
    #     print(email_info)

    # # 移动邮件
    #     email_service.move_message_to_folder(email_id, "error", "ignore")

finally:
    # 关闭连接
    email_service.close()
