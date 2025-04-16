import os
import json
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from utils.logger_config import setup_logger

class EmailAnalysisAssistant:
    def __init__(self):
        # 设置日志
        self.logger = setup_logger('EmailAnalysisAssistant')
        self.logger.info("初始化 EmailAnalysisAssistant...")
        
        # 保持原有的API配置
        os.environ['OPENAI_API_BASE'] = 'https://api.siliconflow.cn/v1'
        os.environ['OPENAI_API_KEY'] = 'sk-elgvqsyxgfpusvhxtypjdtxkppttswuefuieaijgemkmrtld'
        
        self.model = 'deepseek-ai/DeepSeek-V2.5'
        self.chat = ChatOpenAI(model=self.model, temperature=0.1)
        
        try:
            # 读取业务逻辑和决策指导文件
            with open('business.txt', 'r', encoding='utf-8') as f:
                self.business_logic = f.read()
                self.logger.debug("成功加载 business.txt")
                
            with open('actionGuidance.txt', 'r', encoding='utf-8') as f:
                self.action_guidance = f.read()
                self.logger.debug("成功加载 actionGuidance.txt")
            
            with open('cases.txt', 'r', encoding='utf-8') as f:
                self.cases = f.read()
                self.logger.debug("成功加载 cases.txt")
        except Exception as e:
            self.logger.error(f"加载配置文件失败: {str(e)}")
            raise

    def analyze_failed_email(self, email_info: dict) -> list:
        """分析失败的邮件并给出决策建议"""
        self.logger.info(f"开始分析邮件: {email_info.get('emailId', 'unknown')}")
        self.logger.debug(f"邮件完整信息: {json.dumps(email_info, ensure_ascii=False)}")

        prompt_template = """
        现在有一个 通过消费邮件信息和业务逻辑 创建或更新ticket的系统，你读取到的输入邮件都是当前卡在working文件夹（理应被及时处理，但是没有处理）
        或者是因为处理失败被移动到error文件夹的邮件，请分析邮件处理失败的原因。

        你通过学习      
        业务逻辑：
        {business_logic}    
        决策指导：
        {action_guidance}
        
        并结合常见案例：
        {cases}
                
        分析当前的问题邮件信息：
        {email_info}
        
        请根据以上信息，严格按照决策指导文件中定义的json格式，给出分析结果和处理建议，
        请按照以下格式输出内容(英文输出)，即外层是python list 内层是json元素[不要包含代码块或其他标记!!!!]。
        例如:
        [
        {{
            "type": "****",
            "rootcause": "*************",
            "action": "****",
            "impact": "*****"
        }}
        ]
        """
        
        self.logger.debug("生成分析提示词")
        prompt = ChatPromptTemplate.from_template(prompt_template)
        chain = prompt | self.chat | StrOutputParser()
        
        try:
            self.logger.info("调用LLM模型进行分析")
            result = chain.invoke({
                "business_logic": self.business_logic,
                "action_guidance": self.action_guidance,
                "cases": self.cases,
                "email_info": json.dumps(email_info, ensure_ascii=False, indent=2)
            })
            
            self.logger.debug(f"LLM原始响应: {result}")
            
            # 将结果字符串转换为Python对象
            parsed_result = json.loads(result)
            self.logger.info(f"分析完成，决策建议: {json.dumps(parsed_result, ensure_ascii=False)}")
            return parsed_result
            
        except json.JSONDecodeError as e:
            self.logger.error(f"LLM响应格式解析失败: {str(e)}")
            return [{
                "type": "dev",
                "rootcause": "模型响应格式错误，需要开发人员检查",
                "action": -1
            }]
        except Exception as e:
            self.logger.error(f"分析过程发生错误: {str(e)}")
            raise

def test_assistant():
    # 测试代码
    logger = setup_logger('test_assistant')
    logger.info("开始测试 EmailAnalysisAssistant...")
    
    assistant = EmailAnalysisAssistant()
    
    # 模拟一个失败的邮件信息
    test_email1 = {
        "id": 1,
        "emailId": "test123",
        "subject": "Test Subject",
        "processed": "F",
        "processed_state": "F",
        "error_message": """
### Error updating database.  Cause: com.mysql.cj.jdbc.exceptions.MysqlDataTruncation: Data truncation: Data too long for column 'note' at row 1
### The error may exist in com/example/email/repository/TicketRepository.java (best guess)
### The error may involve com.example.email.repository.TicketRepository.updateTicket-Inline
### The error occurred while setting parameters
### SQL: UPDATE ticket SET note = ?, update_count = ?, attachments = ? WHERE ticket_id = ?
### Cause: com.mysql.cj.jdbc.exceptions.MysqlDataTruncation: Data truncation: Data too long for column 'note' at row 1
; Data truncation: Data too long for column 'note' at row 1; nested exception is com.mysql.cj.jdbc.exceptions.MysqlDataTruncation: Data truncation: Data too long for column 'note' at row 1
""",
        "create_ticket": "N",
        "ticket_id": ""
    }

    test_email2 = {
        "id": 1,
        "emailId": "test123",
        "subject": "Test Subject",
        "processed": "F",
        "processed_state": "F",
        "error_message":"attachment too large",
        "create_ticket": "",
        "ticket_id": ""
    }
    test_email3 = {
        "id": 1,
        "emailId": "test123",
        "subject": "Test Subject",
        "processed": "F",
        "processed_state": "F",
        "error_message":"数据库连接失败",
        "create_ticket": "",
        "ticket_id": ""
    }  
    test_email4 = {
        "id": 1,
        "emailId": "test123",
        "subject": "Test Subject",
        "processed": "Y",
        "processed_state": "Y",
        "error_message":"",
        "create_ticket": "",
        "ticket_id": "XM5245 update!"
    }  
    test_email5 = {
        "id": 1,
        "emailId": "test123",
        "subject": "Test Subject",
        "processed": "F",
        "processed_state": "I",
        "error_message":"",
        "create_ticket": "",
        "ticket_id": ""
    }   
    test_email6 = {
        "id": 1,
        "emailId": "test123",
        "subject": "Test Subject",
        "processed": "F",
        "processed_state": "F",
        "error_message":"exchange service not available",
        "create_ticket": "",
        "ticket_id": ""
    }   
    test_email7 = {
        "id": 1,
        "emailId": "test123",
        "subject": "Test Subject",
        "processed": "F",
        "processed_state": "F",
        "error_message":"exchange service not available",
        "create_ticket": "N",
        "ticket_id": "XM5245 update!"
    }       
    logger.info("执行测试用例...")
    result = assistant.analyze_failed_email(test_email1)
    logger.info("测试完成")

if __name__ == "__main__":
    test_assistant()