import csv
import json
from datetime import datetime
from utils.logger_config import setup_logger
from testllm import run_tests

logger = setup_logger('export_report')

def export_test_results_to_csv():
    logger.info("开始导出测试结果...")
    
    # 生成报告文件名
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"test_results_{timestamp}.csv"
    
    # 获取测试结果
    test_results = run_tests()
    
    # 定义CSV头
    headers = ['Case ID', 'Subject', 'Error Message', 'LLM Analysis Type', 'Root Cause', 'Recommended Action']
    
    try:
        # 使用utf-8-sig编码写入，添加BOM标记
        with open(filename, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            
            for result in test_results:
                email_info = result['email_info']
                llm_results = result['llm_result']
                
                if not isinstance(llm_results, list):
                    llm_results = [{"type": "error", "rootcause": str(llm_results), "action": "unknown"}]
                
                for llm_result in llm_results:
                    row = [
                        email_info['case_id'],
                        email_info['subject'],
                        email_info['error_message'],
                        llm_result.get('type', ''),
                        llm_result.get('rootcause', ''),
                        llm_result.get('action', '')
                    ]
                    # 确保每个字段都是字符串类型
                    row = [str(item) if item is not None else '' for item in row]
                    writer.writerow(row)
        
        logger.info(f"测试报告已导出至: {filename}")
        return filename
    
    except Exception as e:
        logger.error(f"导出报告失败: {str(e)}")
        raise

if __name__ == "__main__":
    try:
        report_file = export_test_results_to_csv()
        print(f"报告生成成功: {report_file}")
    except Exception as e:
        print(f"报告生成失败: {str(e)}")
