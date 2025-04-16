import time
import json
from typing import List, Dict
from emailService import EmailService
from DBService import DBService
from LLMHelper import EmailAnalysisAssistant
from utils.logger_config import setup_logger

class EmailMonitoringSystem:
    def __init__(self):
        self.logger = setup_logger('EmailMonitoringSystem')
        self.logger.info("初始化邮件监控系统...")
        
        self.email_service = EmailService()
        self.db_service = DBService()
        self.llm_assistant = EmailAnalysisAssistant()
        self.previous_emails = set()  # 存储上一次检查时的邮件ID
        
    def get_folder_emails(self, folder_name: str) -> Dict[str, dict]:
        """获取指定文件夹中的所有邮件信息"""
        self.logger.info(f"开始获取{folder_name}文件夹邮件...")
        
        email_ids = self.email_service.get_messages_from_folder(folder_name)
        self.logger.debug(f"在{folder_name}文件夹获取到 {len(email_ids)} 封邮件")
        
        emails_dict = {}
        for email_id in email_ids:
            try:
                email_info = self.email_service.get_email_info(email_id, folder_name)
                if email_info and email_info.get('message_id'):
                    emails_dict[email_info['message_id']] = {
                        'email_id': email_id,
                        'info': email_info,
                        'source_folder': folder_name
                    }
                    self.logger.debug(f"成功获取邮件信息: {email_info['message_id']}, 来源文件夹: {folder_name}")
            except Exception as e:
                self.logger.error(f"获取邮件信息失败: {str(e)}")
                
        self.logger.info(f"在{folder_name}文件夹成功处理 {len(emails_dict)} 封邮件")
        return emails_dict

    def get_all_monitored_emails(self) -> Dict[str, dict]:
        """获取所有需要监控的文件夹中的邮件"""
        self.logger.info("开始获取所有监控文件夹的邮件...")
        
        # 获取working和error文件夹的邮件
        working_emails = self.get_folder_emails("working")
        error_emails = self.get_folder_emails("error")
        
        # 合并两个文件夹的邮件
        all_emails = {**working_emails, **error_emails}
        self.logger.info(f"总共获取到 {len(all_emails)} 封邮件")
        
        return all_emails

    def process_failed_emails(self, failed_emails: List[str], emails_dict_folder: Dict[str, dict]):
        """处理失败的邮件"""
        self.logger.info(f"开始处理 {len(failed_emails)} 个失败的邮件")
        
        for message_id in failed_emails:
            self.logger.info(f"处理邮件: {message_id}")
            
            try:
                email_detail_db = self.db_service.get_email_detail(message_id)
                if not email_detail_db:
                    self.logger.warning(f"无法获取邮件详情: {message_id}")
                    continue
                
                self.logger.debug(f"邮件详情: {json.dumps(email_detail_db, ensure_ascii=False)}")
                
                # 使用LLM分析并获取决策建议
                analysis_result = self.llm_assistant.analyze_failed_email(email_detail_db)
                self.logger.info(f"分析结果: {json.dumps(analysis_result, ensure_ascii=False)}")
                # 执行决策
                self.execute_decisions(message_id, analysis_result, emails_dict_folder)
                
            except Exception as e:
                self.logger.error(f"处理邮件 {message_id} 时发生错误: {str(e)}")
            
    def execute_decisions(self, message_id: str, decisions: List[Dict], emails_dict: Dict[str, dict]):
        """执行决策结果"""
        self.logger.info(f"执行决策: {message_id}")
        
        if message_id not in emails_dict:
            self.logger.warning(f"在emails_dict中找不到邮件: {message_id}")
            return
            
        email_data = emails_dict[message_id]
        email_id = email_data['email_id']
        source_folder = email_data['source_folder']
        
        for decision in decisions:
            self.logger.debug(f"决策内容: {json.dumps(decision, ensure_ascii=False)}")
            
            try:
                if decision['type'] == 'automation':
                    target_folder = decision['action']
                    self.logger.info(f"将邮件从 {source_folder} 移动到 {target_folder}")
                    self.email_service.move_message_to_folder(
                        email_id, source_folder, target_folder
                    )
                elif decision['type'] == 'dev':
                    self.logger.info("发送通知邮件给开发人员")
                    self.email_service.send_email(
                        to_addr="zqiang_zhu@163.com",
                        subject="有一封邮件消费失败--" + email_data['info']['subject'] + "--" + message_id,
                        body=decision['rootcause']
                    )
            except Exception as e:
                self.logger.error(f"执行决策时发生错误: {str(e)}")
            
    def monitor_loop(self):
        """监控循环"""
        self.logger.info("启动监控循环...")
        
        try:
            while True:
                print()
                self.logger.info("***************开始新一轮检查********************")
                
                # 获取当前所有监控文件夹中的邮件
                current_emails = self.get_all_monitored_emails()
                current_message_ids = set(current_emails.keys())
                
                if self.previous_emails:
                    # 找出仍然存在的邮件（即处理失败的邮件）
                    failed_message_ids = self.previous_emails.intersection(current_message_ids)
                    
                    if failed_message_ids:
                        self.logger.info(f"发现 {len(failed_message_ids)} 个处理失败的邮件")
                        self.process_failed_emails(failed_message_ids, current_emails)
                    else:
                        self.logger.info("没有发现处理失败的邮件")
                
                # 更新上一次检查的邮件列表
                self.previous_emails = current_message_ids
                
                # 等待间隔
                self.logger.debug("等待5秒后进行下一轮检查...")
                time.sleep(5)
                
        except KeyboardInterrupt:
            self.logger.info("监控系统停止")
        except Exception as e:
            self.logger.error(f"监控循环发生错误: {str(e)}")
        finally:
            self.email_service.close()
            self.logger.info("监控系统关闭")

def test_monitoring_system():
    """测试监控系统"""
    logger = setup_logger('test_monitoring_system')
    logger.info("开始测试监控系统...")
    
    system = EmailMonitoringSystem()
    
    # 模拟一些测试数据
    test_email = {
        "id": 1,
        "emailId": "test123",
        "subject": "Test Subject",
        "processed": "F",
        "processed_state": "F",
        "error_message": "Connection timeout when processing email",
        "create_ticket": "N",
        "ticket_id": None
    }
    
    # 测试LLM分析
    logger.info("测试LLM分析...")
    result = system.llm_assistant.analyze_failed_email(test_email)
    logger.info(f"分析结果: {json.dumps(result, ensure_ascii=False, indent=2)}")
    logger.info("测试完成")

if __name__ == "__main__":
    # 运行测试
    # test_monitoring_system()
    
    # 运行实际监控系统
    system = EmailMonitoringSystem()
    system.monitor_loop()
