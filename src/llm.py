# src/llm.py

import os
from openai import OpenAI
from logger import LOG
from config import Config

config = Config()

class LLM:
    def __init__(self):
        self.client = OpenAI(api_key=config.deepseek_api_key, base_url=config.deepseek_base_url)
        LOG.add("daily_progress/llm_logs.log", rotation="1 MB", level="DEBUG")

    def generate_daily_report(self, markdown_content, dry_run=False):
        prompt = f"以下是项目的最新进展，根据功能合并同类项，形成一份简报，至少包含：1）新增功能；2）主要改进；3）修复问题；:\n\n{markdown_content}"
        system_prompt = f"你是一个github专家,负责监控开发团队使用github的开发效率"
        
        if dry_run:
            LOG.info("Dry run mode enabled. Saving prompt to file.")
            with open("daily_progress/prompt.txt", "w+") as f:
                f.write(prompt)
            LOG.debug("Prompt saved to daily_progress/prompt.txt")
            return "DRY RUN"

        LOG.info("Starting report generation using GPT model.")
        
        try:
            response = self.client.chat.completions.create(
                model="deepseek-chat",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ]
            )
            LOG.debug("GPT response: {}", response)
            return response.choices[0].message.content
        except Exception as e:
            LOG.error("An error occurred while generating the report: {}", e)
            raise

