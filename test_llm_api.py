import requests
import json
from typing import Dict, Any

def test_analyze_email(email_data: Dict[str, Any]) -> None:
    """
    测试邮件分析API
    """
    url = "http://localhost:8000/analyze_email"
    headers = {"Content-Type": "application/json"}
    
    try:
        response = requests.post(url, json=email_data, headers=headers)
        response.raise_for_status()  # 如果响应状态码不是200，将抛出异常
        
        result = response.json()
        print("\nAPI响应结果:")
        print(json.dumps(result, ensure_ascii=False, indent=2))
        
    except requests.exceptions.RequestException as e:
        print(f"\n请求失败: {str(e)}")
        if hasattr(e.response, 'text'):
            print(f"错误详情: {e.response.text}")

def main():
    # 测试用例1：数据库连接失败
    test_case1 = {
        "emailId": "test123",
        "subject": "Test Subject",
        "processed": "F",
        "processed_state": "F",
        "error_message": "数据库连接失败",
        "create_ticket": "",
        "ticket_id": "",
        "id": 1
    }
    
    # 测试用例2：附件过大
    test_case2 = {
        "emailId": "test456",
        "subject": "Large Attachment",
        "processed": "F",
        "processed_state": "F",
        "error_message": "attachment too large",
        "create_ticket": "",
        "ticket_id": "",
        "id": 2
    }
    
    # 测试用例3：Exchange服务不可用
    test_case3 = {
        "emailId": "test789",
        "subject": "Exchange Error",
        "processed": "F",
        "processed_state": "F",
        "error_message": "exchange service not available",
        "create_ticket": "N",
        "ticket_id": "XM5245 update!",
        "id": 3
    }
    
    print("开始测试LLM分析服务API...")
    
    print("\n测试用例1 - 数据库连接失败:")
    test_analyze_email(test_case1)
    
    print("\n测试用例2 - 附件过大:")
    test_analyze_email(test_case2)
    
    print("\n测试用例3 - Exchange服务不可用:")
    test_analyze_email(test_case3)

if __name__ == "__main__":
    main() 