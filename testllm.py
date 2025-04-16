from LLMHelper import EmailAnalysisAssistant
from utils.logger_config import setup_logger
import json

logger = setup_logger('test_llm')

def generate_test_cases():
    return [
        {
            "case_id": 1,
            "emailId": "test001",
            "subject": "数据库字段溢出",
            "processed": "F",
            "processed_state": "F",
            "error_message": "Data truncation: Data too long for column 'note' at row 1",
            "create_ticket": "N",
            "ticket_id": ""
        },
        # {
        #     "case_id": 2,
        #     "emailId": "test002",
        #     "subject": "附件过大",
        #     "processed": "F",
        #     "processed_state": "F",
        #     "error_message": "Attachment size exceeds limit (25MB)",
        #     "create_ticket": "N",
        #     "ticket_id": ""
        # },
        # {
        #     "case_id": 3,
        #     "emailId": "test003",
        #     "subject": "网络连接问题",
        #     "processed": "F",
        #     "processed_state": "F",
        #     "error_message": "Connection timeout when connecting to database",
        #     "create_ticket": "N",
        #     "ticket_id": ""
        # },
        {
            "case_id": 4,
            "emailId": "test004",
            "subject": "创建成功案例",
            "processed": "Y",
            "processed_state": "Y",
            "error_message": "attachment size exceeds limit (25MB)",
            "create_ticket": "Y",
            "ticket_id": "XM202403201234"
        },
        # {
        #     "case_id": 5,
        #     "emailId": "test005",
        #     "subject": "更新成功案例",
        #     "processed": "Y",
        #     "processed_state": "Y",
        #     "error_message": "",
        #     "create_ticket": "N",
        #     "ticket_id": "XM202403201235 update!"
        # },
        # {
        #     "case_id": 6,
        #     "emailId": "test006",
        #     "subject": "忽略处理案例",
        #     "processed": "F",
        #     "processed_state": "I",
        #     "error_message": "",
        #     "create_ticket": "",
        #     "ticket_id": ""
        # },
        # {
        #     "case_id": 7,
        #     "emailId": "test007",
        #     "subject": "特殊字符问题",
        #     "processed": "F",
        #     "processed_state": "F",
        #     "error_message": "Invalid characters in email content",
        #     "create_ticket": "N",
        #     "ticket_id": ""
        # },
        # {
        #     "case_id": 8,
        #     "emailId": "test008",
        #     "subject": "邮箱服务异常",
        #     "processed": "F",
        #     "processed_state": "F",
        #     "error_message": "Exchange service temporarily unavailable",
        #     "create_ticket": "",
        #     "ticket_id": ""
        # },
        # {
        #     "case_id": 9,
        #     "emailId": "test009",
        #     "subject": "API调用失败",
        #     "processed": "F",
        #     "processed_state": "F",
        #     "error_message": "API request failed with status 500",
        #     "create_ticket": "N",
        #     "ticket_id": ""
        # },
        # {
        #     "case_id": 10,
        #     "emailId": "test010",
        #     "subject": "数据库连接池满",
        #     "processed": "F",
        #     "processed_state": "F",
        #     "error_message": "Maximum pool size has been reached",
        #     "create_ticket": "",
        #     "ticket_id": ""
        # },
        # {
        #     "case_id": 11,
        #     "emailId": "test011",
        #     "subject": "附件格式错误",
        #     "processed": "F",
        #     "processed_state": "F",
        #     "error_message": "Unsupported attachment format",
        #     "create_ticket": "N",
        #     "ticket_id": ""
        # },
        # {
        #     "case_id": 12,
        #     "emailId": "test012",
        #     "subject": "邮件内容为空",
        #     "processed": "F",
        #     "processed_state": "F",
        #     "error_message": "Email body is empty",
        #     "create_ticket": "N",
        #     "ticket_id": ""
        # },
        # {
        #     "case_id": 13,
        #     "emailId": "test013",
        #     "subject": "重复处理",
        #     "processed": "F",
        #     "processed_state": "F",
        #     "error_message": "Duplicate ticket ID detected",
        #     "create_ticket": "N",
        #     "ticket_id": ""
        # },
        # {
        #     "case_id": 14,
        #     "emailId": "test014",
        #     "subject": "权限验证失败",
        #     "processed": "F",
        #     "processed_state": "F",
        #     "error_message": "Authentication failed for API access",
        #     "create_ticket": "",
        #     "ticket_id": ""
        # },
        {
            "case_id": 15,
            "emailId": "test015",
            "subject": "系统资源不足",
            "processed": "F",
            "processed_state": "F",
            "error_message": "System resources exhausted",
            "create_ticket": "",
            "ticket_id": ""
        }
    ]

def run_tests():
    logger.info("开始执行测试...")
    assistant = EmailAnalysisAssistant()
    test_cases = generate_test_cases()
    test_results = []
    
    for case in test_cases:
        logger.info(f"测试用例 {case['case_id']}: {case['subject']}")
        try:
            result = assistant.analyze_failed_email(case)
            test_results.append({
                "case_id": case["case_id"],
                "email_info": case,
                "llm_result": result
            })
        except Exception as e:
            logger.error(f"测试用例 {case['case_id']} 执行失败: {str(e)}")
            test_results.append({
                "case_id": case["case_id"],
                "email_info": case,
                "llm_result": str(e)
            })
    
    return test_results

if __name__ == "__main__":
    results = run_tests()
    print(f"测试完成，共执行 {len(results)} 个测试用例")
