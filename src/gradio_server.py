import gradio as gr  # 导入gradio库用于创建GUI

from config import Config  # 导入配置管理模块
from github_client import GitHubClient  # 导入用于GitHub API操作的客户端
from report_generator import ReportGenerator  # 导入报告生成器模块
from llm import LLM  # 导入可能用于处理语言模型的LLM类
from subscription_manager import SubscriptionManager  # 导入订阅管理器
from logger import LOG  # 导入日志记录器
import re
import markdown2

# 创建各个组件的实例
config = Config()
github_client = GitHubClient(config.github_token)
llm = LLM()
report_generator = ReportGenerator(llm)
subscription_manager = SubscriptionManager(config.subscriptions_file)

def export_progress_by_date_range(repo, days):
    # 定义一个函数，用于导出和生成指定时间范围内项目的进展报告
    raw_file_path = github_client.export_progress_by_date_range(repo, days)  # 导出原始数据文件路径
    report, report_file_path = report_generator.generate_report_by_date_range(raw_file_path, days)  # 生成并获取报告内容及文件路径

    return report, report_file_path  # 返回报告内容和报告文件路径

# def split_markdown_sections(text):
#     """Split markdown text into sections based on h1 headers (#)."""
#     # Split on h1 headers but keep the header with its section
#     sections = re.split(r'(?=^# )', text.strip(), flags=re.MULTILINE)
#     # Remove empty sections
#     return [section.strip() for section in sections if section.strip()]
#
# def render_markdown_sections(markdown_text):
#     """Process markdown text and return rendered sections."""
#     sections = split_markdown_sections(markdown_text)
#     rendered_sections = []
#
#     for section in sections:
#         # Get the section title (first line)
#         title = section.split('\n')[0].lstrip('#').strip()
#         # Get the content (rest of the section)
#         content = '\n'.join(section.split('\n')[1:]).strip()
#         # Convert markdown to HTML
#         html_content = markdown2.markdown(content)
#         rendered_sections.append((title, html_content))
#
#     return rendered_sections

# 创建Gradio界面
# demo = gr.Interface(
#     fn=export_progress_by_date_range,  # 指定界面调用的函数
#     title="GitHubSentinel",  # 设置界面标题
#     inputs=[
#         gr.Dropdown(
#             subscription_manager.list_subscriptions(), label="订阅列表", info="已订阅GitHub项目"
#         ),  # 下拉菜单选择订阅的GitHub项目
#         gr.Slider(value=2, minimum=1, maximum=7, step=1, label="报告周期", info="生成项目过去一段时间进展，单位：天"),
#         # 滑动条选择报告的时间范围
#     ],
#     outputs=[gr.Markdown(), gr.File(label="下载报告")],  # 输出格式：Markdown文本和文件下载
# )

with (gr.Blocks(css="style.css") as demo):
    gr.Markdown("# Github Sentinel")

    with gr.Row():
        dropdown_input = gr.Dropdown(
            subscription_manager.list_subscriptions(), label="订阅列表", info="已订阅GitHub项目"
        )

    with gr.Row():
        slider_input = gr.Slider(value=2, minimum=1, maximum=7, step=1, label="报告周期", info="生成项目过去一段时间进展，单位：天")

    with gr.Row():
        # Process button
        process_button = gr.Button("Submit")

    process_button.click(
        fn=export_progress_by_date_range,
        inputs=[dropdown_input, slider_input],
        outputs=[gr.Markdown(), gr.File(label="下载报告")]
    )

# css = """
# .section-container {
#     margin: 20px 0;
#     padding: 20px;
#     border: 1px solid #ddd;
#     border-radius: 8px;
# }
# .section-title {
#     font-size: 1.5em;
#     margin-bottom: 10px;
#     color: #2c3e50;
# }
# .section-content {
#     line-height: 1.6;
# }
# """



if __name__ == "__main__":
    demo.launch(share=True, server_name="0.0.0.0")  # 启动界面并设置为公共可访问
    # 可选带有用户认证的启动方式
    # demo.launch(share=True, server_name="0.0.0.0", auth=("django", "1234"))