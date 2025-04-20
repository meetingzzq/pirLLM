import os
import json
from typing import Dict, Any, List
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain.agents import initialize_agent, Tool
from utils.logger_config import setup_logger
from tools import LogAnalyzer, DatabaseQuery

class EmailMonitorAgent:
    def __init__(self):
        # 设置日志
        self.logger = setup_logger('EmailMonitorAgent')
        self.logger.info("初始化 EmailMonitorAgent...")

        # 配置API
        os.environ['OPENAI_API_BASE'] = 'https://api.siliconflow.cn/v1'
        os.environ['OPENAI_API_KEY'] = 'sk-elgvqsyxgfpusvhxtypjdtxkppttswuefuieaijgemkmrtld'

        # 初始化LLM
        self.model = 'deepseek-ai/DeepSeek-V2.5'
        self.llm = ChatOpenAI(model=self.model, temperature=0.1)

        # 初始化工具
        self.log_analyzer = LogAnalyzer()
        self.db_query = DatabaseQuery()

        # 读取actionGuidance.txt内容
        try:
            with open('actionGuidance.txt', 'r', encoding='utf-8') as f:
                self.action_guidance = f.read()
        except Exception as e:
            self.logger.error(f"读取actionGuidance.txt失败: {str(e)}")
            self.action_guidance = ""

        # 定义工具
        tools = [
            Tool(
                name="Query Email",
                func=self.db_query.query_email,
                description="查询指定邮件ID的邮件信息"
            ),
            Tool(
                name="Analyze Logs",
                func=self.log_analyzer.analyze,
                description="分析指定邮件ID的系统日志"
            ),
            Tool(
                name="Query Ticket",
                func=self.db_query.query_ticket,
                description="查询指定工单ID的工单信息"
            )
        ]

       # 创建分析提示词
        # 创建分析提示词
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", f"""You are an intelligent assistant for an email monitoring system. Your task is to analyze the reasons for email processing failures.
            Decision guidance:
            {self.action_guidance}
            Please output the analysis result in the following valid JSON format (as a Python list containing JSON elements, without code blocks or other markers):
            [
                {{
                    "type": "****",
                    "rootcause": "*************",
                    "action": "****",
                    "impact": "*****"
                }}
            ]
            """),
            ("human", "{input}")
        ])

        # 初始化agent
        self.agent = initialize_agent(tools, self.llm, agent="chat-zero-shot-react-description", verbose=True)

    def analyze_email(self, email_id: str) -> Dict[str, Any]:
        """分析指定邮件ID的问题"""
        self.logger.info(f"开始分析邮件: {email_id}")


        # 生成完整的提示信息
        input_text = f"请分析邮件ID为 {email_id} 的邮件处理失败的原因，并按照指定格式输出分析结果。"

        self.prompt = """You are an intelligent assistant for an email monitoring system. Your task is to analyze the reasons for email processing failures.
            Decision guidance:
            {self.action_guidance}
            Please output the analysis result in the following valid JSON format (as a Python list containing JSON elements, without code blocks or other markers):
            [
                {{
                    "type": "****",
                    "rootcause": "*************",
                    "action": "****",
                    "impact": "*****"
                }}
            ]
            {input_text}
            """

        result = self.agent.run(self.prompt)

        print(result)





        self.logger.info(f"分析完成: {json.dumps(result, ensure_ascii=False, indent=2)}")
        return result


if __name__ == "__main__":
    # 测试代码
    agent = EmailMonitorAgent()
    test_email_id = "test123"
    result = agent.analyze_email(test_email_id)
    print(result)