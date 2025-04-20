from tools import SQLQuery, EmailSQLBuilder, TicketSQLBuilder, LogQuery

def test_tools():
    # 初始化工具实例
    sql_query = SQLQuery()
    email_builder = EmailSQLBuilder()
    ticket_builder = TicketSQLBuilder()
    log_query = LogQuery()
    
    # 测试email查询
    email_id = "A732EA9F64CC8AEAFDB4368F53B907593108"
    email_sql = email_builder.build_query(email_id)
    email_result = sql_query.execute_query(email_sql)
    print(f"Email查询结果: {email_result}")
    
    # 测试ticket查询
    ticket_id = "XM202503181059"
    ticket_sql = ticket_builder.build_query(ticket_id)
    ticket_result = sql_query.execute_query(ticket_sql)
    print(f"Ticket查询结果: {ticket_result}")
    
    # 测试日志查询
    log_name = "EmailAnalysisAssistant_20250419.log"
    keyword = "error"
    log_result = log_query.search_log(log_name, keyword)
    print(f"日志查询结果: {log_result}")

if __name__ == "__main__":
    test_tools() 