import os
import re
import shutil
import requests
from pathlib import Path
import pdfplumber
from docx import Document
import pandas as pd

class DocumentClassifier:
    def __init__(self, api_key):
        self.api_key = api_key
        self.api_url = "https://api.deepseek.com/v1"  # 替换为实际API地址

    def call_api(self, endpoint, data):
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        response = requests.post(
            f"{self.api_url}/{endpoint}",
            json=data,
            headers=headers
        )
        return response.json()

    def extract_text(self, file_path):
        if file_path.endswith('.txt'):
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        
        elif file_path.endswith('.pdf'):
            with pdfplumber.open(file_path) as pdf:
                return "\n".join(page.extract_text() for page in pdf.pages)
        
        elif file_path.endswith('.docx'):
            doc = Document(file_path)
            return "\n".join(p.text for p in doc.paragraphs)
        
        elif file_path.endswith(('.xlsx', '.xls')):
            df = pd.read_excel(file_path)
            return df.to_string()
        
        else:
            raise ValueError(f"Unsupported file type: {file_path}")

    def classify_document(self, text):
        response = self.call_api("classify", {
            "text": text,
            "language": "zh"
        })
        return response['category']

    def generate_filename(self, text):
        response = self.call_api("summarize", {
            "text": text,
            "language": "zh",
            "max_length": 20
        })
        return response['summary']

    def process_folder(self, folder_path):
        for file_name in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file_name)
            if os.path.isfile(file_path):
                try:
                    print(f"Processing: {file_name}")
                    
                    # 提取文本内容
                    text = self.extract_text(file_path)
                    
                    # 获取分类
                    category = self.classify_document(text)
                    
                    # 生成新文件名
                    new_name = self.generate_filename(text)
                    ext = os.path.splitext(file_name)[1]
                    new_name = f"{new_name}{ext}"
                    
                    # 创建分类文件夹
                    category_folder = os.path.join(folder_path, category)
                    os.makedirs(category_folder, exist_ok=True)
                    
                    # 移动并重命名文件
                    new_path = os.path.join(category_folder, new_name)
                    shutil.move(file_path, new_path)
                    
                    print(f"Processed: {file_name} -> {new_path}")
                    
                except Exception as e:
                    print(f"Error processing {file_name}: {str(e)}")

if __name__ == "__main__":
    api_key = input("请输入Deepseek API Key: ")
    folder_path = input("请输入要处理的文件夹路径: ")
    
    classifier = DocumentClassifier(api_key)
    classifier.process_folder(folder_path)
