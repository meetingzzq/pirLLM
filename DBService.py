import requests
from requests.exceptions import RequestException

class DBService:
    def __init__(self, base_url="http://localhost:8080/api/"):
        self.base_url = base_url

    def get_email_detail(self, email_id):
        """
        获取邮件详情
        :param email_id: 邮件ID
        :return: 邮件详情或None（未找到）
        """
        try:
            response = requests.get(f"{self.base_url}{email_id}")
            response.raise_for_status()  # 检查请求是否成功
            return response.json()
        except RequestException as e:
            print(f"请求失败：{e}")
            return None

    def save_email(self, email):
        """
        保存邮件
        :param email: Email对象（字典格式）
        :return: 成功消息或错误消息
        """
        try:
            response = requests.post(f"{self.base_url}save", json=email)
            response.raise_for_status()
            return response.text
        except RequestException as e:
            print(f"请求失败：{e}")
            return f"保存失败：{e}"

    def update_email(self, email):
        """
        更新邮件
        :param email: Email对象（字典格式）
        :return: 成功消息或错误消息
        """
        try:
            response = requests.put(f"{self.base_url}update", json=email)
            response.raise_for_status()
            return response.text
        except RequestException as e:
            print(f"请求失败：{e}")
            return f"更新失败：{e}"

    def search_logs(self, log_path, keyword):
        """
        搜索日志
        :param log_path: 日志文件路径
        :param keyword: 关键字
        :return: 匹配的日志内容或错误消息
        """
        try:
            params = {"logPath": log_path, "keyword": keyword}
            response = requests.get(f"{self.base_url}searchLogs", params=params)
            response.raise_for_status()
            return response.text
        except RequestException as e:
            print(f"请求失败：{e}")
            return f"搜索失败：{e}"