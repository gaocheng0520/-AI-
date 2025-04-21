import pandas as pd
from openai import OpenAI

# Step 1: DeepSeek API 配置
client = OpenAI(
    api_key="sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxx",  # 请替换为你的 DeepSeek API Key
    base_url="https://api.deepseek.com"
)

# Step 2: 数据读取与处理
df = pd.read_csv("train.csv", low_memory=False)
df["Date"] = pd.to_datetime(df["Date"])
df = df[df["Open"] == 1]
recent_df = df[df["Date"] >= df["Date"].max() - pd.DateOffset(months=3)].copy()
recent_df["Month"] = recent_df["Date"].dt.to_period("M")

# Step 3: 计算归因指标
agg = recent_df.groupby("Month").agg({
    "Sales": "sum",
    "Customers": "sum",
    "Promo": "mean",
    "SchoolHoliday": "mean",
    "StateHoliday": lambda x: (x != '0').mean()
}).reset_index()
agg["客单价"] = agg["Sales"] / agg["Customers"]

# Step 4: 计算环比增幅
agg_sorted = agg.sort_values("Month")
growth_df = agg_sorted[["Sales", "Customers", "客单价", "Promo", "SchoolHoliday", "StateHoliday"]].pct_change().iloc[1:].copy()
month_labels = agg_sorted["Month"].astype(str).tolist()
month_pairs = [f"{month_labels[i]} vs {month_labels[i-1]}" for i in range(1, len(month_labels))]
growth_df["月份对"] = month_pairs

# Step 5: 构造 Prompt
def build_prompt(agg: pd.DataFrame, growth: pd.DataFrame) -> str:
    rows = agg.to_dict(orient="records")
    prompt = "请根据下列三个月销售数据，分析营业额的环比增长/下降的主要原因，并判断哪些因素（顾客数、促销、学校假期、州假期、客单价）影响最大。输出详细的中文分析报告，最后请给出提升营业额的建议。\n\n"
    for row in rows:
        month = str(row['Month'])
        prompt += f"""
【{month}】
- 营业额: {row['Sales']:.0f}
- 顾客数: {row['Customers']:.0f}
- 客单价: {row['客单价']:.2f}
- 促销占比: {row['Promo']*100:.1f}%
- 学校假期占比: {row['SchoolHoliday']*100:.1f}%
- 州假期占比: {row['StateHoliday']*100:.2f}%
"""
    prompt += "\n请详细总结每个月之间营业额变化的原因，列出主要影响因子及贡献判断。"
    return prompt

prompt = build_prompt(agg, growth_df)

# Step 6: 调用 DeepSeek API
def call_deepseek(prompt: str) -> str:
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "你是一位数据分析专家,分析近三个月商店的销售数据，分析营业额的环比增长/下降的主要原因，并判断哪些因素（顾客数、促销、学校假期、州假期、客单价）影响最大"},
            {"role": "user", "content": prompt}
        ],
        stream=False
    )
    return response.choices[0].message.content

# Step 7: 调用并保存报告
analysis = call_deepseek(prompt)

with open("deepseek_sales_attribution_report.md", "w", encoding="utf-8") as f:
    f.write("# \U0001F4CA 营业额归因分析报告（由 DeepSeek 大模型生成）\n\n")
    f.write("## 一、分析背景与目的\n")
    f.write("本报告旨在对最近三个月营业额的环比变化进行归因分析，找出造成营业额上升或下降的关键因素，并计算其大致贡献度。借助 DeepSeek 大模型的自然语言理解能力，结合业务数据，生成解释性强的可视化报告。\n\n")
    f.write("## \U0001F9E0 二、分析框架\n")
    f.write("\n| 模块 | 内容 |\n|------|------|\n| 数据来源 | train.csv（营业门店数据） |\n| 分析范围 | 最近三个月的开门门店数据 |\n| 分析指标 | 营业额、顾客数量、客单价、促销比、学校假期、州假期 |\n| 分析方法 | 数据处理 + 归因因子构建 + 大模型自动分析 |\n| 输出形式 | Markdown 报告 + LLM 分析总结 |\n")
    f.write("\n## \U0001F4CC 三、输入数据摘要\n")
    f.write(prompt)
    f.write("\n\n---\n\n## \U0001F50D 四、DeepSeek 分析结果\n")
    f.write(analysis)
    
    # 添加环比变化表格
    f.write("\n\n---\n\n## \U0001F4C8 五、中间数据与环比增幅\n")
    f.write("指标 | " + " | ".join(growth_df["月份对"]) + "\n")
    f.write(":--|" + "|".join([":--:" for _ in growth_df["月份对"]]) + "\n")
    for col in ["Sales", "Customers", "客单价", "Promo", "SchoolHoliday", "StateHoliday"]:
        row = "{} | {}".format(
            col,
            " | ".join([f"{v * 100:+.2f}%" for v in growth_df[col]])
        )
        f.write(row + "\n")

import pandas as pd
from openai import OpenAI

# Step 1: DeepSeek API 配置
client = OpenAI(
    api_key="sk-d2fc486c317b45fb8cf7fa5966746a49",  # 请替换为你的 DeepSeek API Key
    base_url="https://api.deepseek.com"
)

# Step 2: 数据读取与处理
df = pd.read_csv("train.csv", low_memory=False)
df["Date"] = pd.to_datetime(df["Date"])
df = df[df["Open"] == 1]
recent_df = df[df["Date"] >= df["Date"].max() - pd.DateOffset(months=3)].copy()
recent_df["Month"] = recent_df["Date"].dt.to_period("M")

# Step 3: 计算归因指标
agg = recent_df.groupby("Month").agg({
    "Sales": "sum",
    "Customers": "sum",
    "Promo": "mean",
    "SchoolHoliday": "mean",
    "StateHoliday": lambda x: (x != '0').mean()
}).reset_index()
agg["客单价"] = agg["Sales"] / agg["Customers"]

# Step 4: 计算环比增幅
agg_sorted = agg.sort_values("Month")
growth_df = agg_sorted[["Sales", "Customers", "客单价", "Promo", "SchoolHoliday", "StateHoliday"]].pct_change().iloc[1:].copy()
month_labels = agg_sorted["Month"].astype(str).tolist()
month_pairs = [f"{month_labels[i]} vs {month_labels[i-1]}" for i in range(1, len(month_labels))]
growth_df["月份对"] = month_pairs

# Step 5: 构造 Prompt
def build_prompt(agg: pd.DataFrame, growth: pd.DataFrame) -> str:
    rows = agg.to_dict(orient="records")
    prompt = "请根据下列三个月销售数据，分析营业额的环比增长/下降的主要原因，并判断哪些因素（顾客数、促销、学校假期、州假期、客单价）影响最大。输出详细的中文分析报告，最后请给出提升营业额的建议。\n\n"
    for row in rows:
        month = str(row['Month'])
        prompt += f"""
【{month}】
- 营业额: {row['Sales']:.0f}
- 顾客数: {row['Customers']:.0f}
- 客单价: {row['客单价']:.2f}
- 促销占比: {row['Promo']*100:.1f}%
- 学校假期占比: {row['SchoolHoliday']*100:.1f}%
- 州假期占比: {row['StateHoliday']*100:.2f}%
"""
    prompt += "\n请详细总结每个月之间营业额变化的原因，列出主要影响因子及贡献判断。"
    return prompt

prompt = build_prompt(agg, growth_df)

# Step 6: 调用 DeepSeek API
def call_deepseek(prompt: str) -> str:
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "你是一位数据分析专家,分析近三个月商店的销售数据，分析营业额的环比增长/下降的主要原因，并判断哪些因素（顾客数、促销、学校假期、州假期、客单价）影响最大"},
            {"role": "user", "content": prompt}
        ],
        stream=False
    )
    return response.choices[0].message.content

# Step 7: 调用并保存报告
analysis = call_deepseek(prompt)

with open("deepseek_sales_attribution_report.md", "w", encoding="utf-8") as f:
    f.write("# \U0001F4CA 营业额归因分析报告（由 DeepSeek 大模型生成）\n\n")
    f.write("## 一、分析背景与目的\n")
    f.write("本报告旨在对最近三个月营业额的环比变化进行归因分析，找出造成营业额上升或下降的关键因素，并计算其大致贡献度。借助 DeepSeek 大模型的自然语言理解能力，结合业务数据，生成解释性强的可视化报告。\n\n")
    f.write("## \U0001F9E0 二、分析框架\n")
    f.write("\n| 模块 | 内容 |\n|------|------|\n| 数据来源 | train.csv（营业门店数据） |\n| 分析范围 | 最近三个月的开门门店数据 |\n| 分析指标 | 营业额、顾客数量、客单价、促销比、学校假期、州假期 |\n| 分析方法 | 数据处理 + 归因因子构建 + 大模型自动分析 |\n| 输出形式 | Markdown 报告 + LLM 分析总结 |\n")
    f.write("\n## \U0001F4CC 三、输入数据摘要\n")
    f.write(prompt)
    # 添加环比变化表格
    f.write("\n\n---\n\n## \U0001F4C8 四、中间数据与环比增幅\n")
    f.write("指标 | " + " | ".join(growth_df["月份对"]) + "\n")
    f.write(":--|" + "|".join([":--:" for _ in growth_df["月份对"]]) + "\n")
    for col in ["Sales", "Customers", "客单价", "Promo", "SchoolHoliday", "StateHoliday"]:
        row = "{} | {}".format(
            col,
            " | ".join([f"{v * 100:+.2f}%" for v in growth_df[col]])
        )
        f.write(row + "\n")

    f.write("\n\n---\n\n## \U0001F50D 五、DeepSeek 分析结果\n")
    f.write(analysis)

    f.write("以上分析基础上，已生成营业额提升建议，详见分析结尾部分。\n如需进一步操作建议、数据支持与图表可视化，请结合业务实际开展多维度细化分析。\n")

