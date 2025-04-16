from DBService import DBService

db_service = DBService()

# 获取邮件详情
email_id = "<6e07133a.9d41.195a8b58e7b.Coremail.zqiang_zhu@163.com>"
email_detail = db_service.get_email_detail(email_id)
print(email_detail)

# 保存邮件
email_data = {
    "emailId": "new_email_id",
    "subject": "Test Email",
    "content": "This is a test email."
}
save_result = db_service.save_email(email_data)
print(save_result)

# 更新邮件
updated_email_data = {
  "emailId": "new_email_id",
  "processed": "true",
  "processedState": "SUCCESS",
  "errorMessage": "null",
  "createTicket": "true",
  "ticketId": "12345"
}

update_result = db_service.update_email(updated_email_data)
print(update_result)

# 搜索日志
log_path = "/path/to/logfile.log"
keyword = "error"
search_result = db_service.search_logs(log_path, keyword)
print(search_result)