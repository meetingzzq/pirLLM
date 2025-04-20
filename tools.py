from typing import Dict, Any
import random
from datetime import datetime, timedelta
import mysql.connector
import os
import re

class LogAnalyzer:
    def __init__(self):
        # 模拟的日志数据
        self.log_patterns = {
            "database_error": [
                "Error updating database: Data truncation",
                "Database connection failed",
                "SQL syntax error",
                "Deadlock found when trying to get lock"
            ],
            "attachment_error": [
                "Attachment too large",
                "Failed to process attachment",
                "Invalid attachment format"
            ],
            "exchange_error": [
                "Exchange service not available",
                "Failed to connect to exchange server",
                "Exchange authentication failed"
            ],
            "api_error": [
                "API call failed",
                "Invalid API response",
                "API rate limit exceeded"
            ]
        }
        
    def analyze(self, email_id: str) -> Dict[str, Any]:
        """分析日志，返回与邮件ID相关的错误信息"""
        # 模拟日志分析结果
        error_type = random.choice(list(self.log_patterns.keys()))
        error_message = random.choice(self.log_patterns[error_type])
        
        result = {
            "email_id": email_id,
            "error_type": error_type,
            "error_message": error_message,
            "timestamp": datetime.now().isoformat(),
            "log_level": "ERROR",
            "analysis": {
                "severity": "high" if error_type in ["database_error", "exchange_error"] else "medium",
                "impact": "系统功能受影响" if error_type in ["database_error", "exchange_error"] else "部分功能受影响",
                "suggestion": self._get_suggestion(error_type)
            }
        }
        
        return {
            "status": "success",
            "data": result,
            "message": "日志分析完成"
        }
    
    def _get_suggestion(self, error_type: str) -> str:
        """根据错误类型返回建议"""
        suggestions = {
            "database_error": "检查数据库连接和SQL语句",
            "attachment_error": "检查附件大小和格式限制",
            "exchange_error": "检查Exchange服务器状态和认证信息",
            "api_error": "检查API调用参数和限流设置"
        }
        return suggestions.get(error_type, "请检查相关配置")

class DatabaseQuery:
    def __init__(self):
        # 模拟的数据库数据
        self.email_data = {
            "test123": {
                "id": 1,
                "emailId": "test123",
                "subject": "Test Subject",
                "sender": "test@example.com",
                "receiver": "support@example.com",
                "processed": "F",
                "processed_state": "F",
                "error_message": "Database connection failed",
                "create_ticket": "N",
                "ticket_id": "XM202503171535",
                "receiveTime": (datetime.now() - timedelta(hours=1)).isoformat(),
                "analysis": {
                    "status": "failed",
                    "reason": "数据库连接失败",
                    "suggestion": "检查数据库连接配置"
                }
            }
        }
        
        self.ticket_data = {
            "XM202503171535": {
                "ticket_id": "XM202503171535",
                "status": "open",
                "priority": "high",
                "created_at": (datetime.now() - timedelta(days=1)).isoformat(),
                "updated_at": datetime.now().isoformat(),
                "analysis": {
                    "current_state": "等待处理",
                    "next_action": "需要人工介入",
                    "suggestion": "联系技术支持团队"
                }
            }
        }
    
    def query_email(self, email_id: str) -> Dict[str, Any]:
        """查询邮件信息"""
        if email_id in self.email_data:
            return {
                "status": "success",
                "data": self.email_data[email_id],
                "message": "邮件信息查询成功"
            }
        return {
            "status": "error",
            "error": "Email not found",
            "suggestion": "检查邮件ID是否正确",
            "message": "邮件信息查询失败"
        }
    
    def query_ticket(self, ticket_id: str) -> Dict[str, Any]:
        """查询工单信息"""
        if ticket_id in self.ticket_data:
            return {
                "status": "success",
                "data": self.ticket_data[ticket_id],
                "message": "工单信息查询成功"
            }
        return {
            "status": "error",
            "error": "Ticket not found",
            "suggestion": "检查工单ID是否正确",
            "message": "工单信息查询失败"
        }

class SQLQuery:
    def __init__(self):
        self.config = {
            'host': 'localhost',
            'user': 'root',
            'password': 'zznewQQ031578',
            'database': 'pir',
            'port': 3306
        }
    
    def execute_query(self, sql: str) -> Dict[str, Any]:
        """执行SQL查询并返回结果"""
        try:
            conn = mysql.connector.connect(**self.config)
            cursor = conn.cursor(dictionary=True)
            cursor.execute(sql)
            result = cursor.fetchall()
            cursor.close()
            conn.close()
            return {
                "status": "success",
                "data": result,
                "message": "SQL查询执行成功"
            }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "message": "SQL查询执行失败"
            }

class EmailSQLBuilder:
    def build_query(self, email_id: str) -> str:
        """构建查询email表的SQL语句"""
        return f"""
        SELECT * FROM email 
        WHERE emailId = '{email_id}'
        """

class TicketSQLBuilder:
    def build_query(self, ticket_id: str) -> str:
        """构建查询ticket表的SQL语句"""
        return f"""
        SELECT * FROM ticket 
        WHERE ticket_id = '{ticket_id}'
        """

class LogQuery:
    def __init__(self):
        self.log_path = r"C:\Users\Jay\Desktop\PIR\Service\LLM-backup\logs"
    
    def search_log(self, log_name: str, keyword: str) -> Dict[str, Any]:
        """搜索日志文件中的关键词"""
        try:
            log_file = os.path.join(self.log_path, log_name)
            if not os.path.exists(log_file):
                return {
                    "status": "error",
                    "error": "Log file not found",
                    "message": "日志文件不存在"
                }
            
            results = []
            with open(log_file, 'r', encoding='utf-8') as f:
                for line in f:
                    if keyword in line:
                        results.append(line.strip())
            
            return {
                "status": "success",
                "data": results,
                "message": "日志查询成功"
            }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "message": "日志查询失败"
            } 