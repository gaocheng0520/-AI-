本项目基于Rossmann Store Sales商店最近三个月的商店销售数据，借助 DeepSeek 大模型对营业额的环比增减进行归因分析，识别顾客数、客单价、促销、学校假期、州假期等关键影响因素，并自动生成结构化分析报告。

📁 项目结构
├── train.csv # 商店的历史销售数据（包含日期、营业额、促销、节假日等）
├── run.py  # 主分析脚本，生成分析报告
├── deepseek_sales_attribution_report.md  # 自动生成的 Markdown 分析报告
└── README.md  # 项目说明文档
🔧 环境依赖
Python 3.7+

依赖库：
pip install pandas openai
🔑 配置说明
请在脚本中配置你的 DeepSeek API Key：
client = OpenAI(
    api_key="sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxx",  # 替换为你的 DeepSeek API Key
    base_url="https://api.deepseek.com"
)
