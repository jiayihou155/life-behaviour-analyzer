import json
import os
import hashlib
import logging
from datetime import datetime
import pandas as pd

# 1. 数据与日志目录隔离设置
DATA_DIR = "data"
DATA_FILE = os.path.join(DATA_DIR, "data.json")
LOG_FILE = os.path.join(DATA_DIR, "tracker.log")

# 创建专用的数据文件夹
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

# 配置日志记录
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    encoding="utf-8"
)

def hash_password(password):
    return hashlib.sha256(password.encode("utf-8")).hexdigest()

def init_data():
    if not os.path.exists(DATA_FILE):
        init = {"users": {}}
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(init, f, ensure_ascii=False, indent=2)

def load_data():
    if not os.path.exists(DATA_FILE):
        init_data()
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# --- 工具函数：输入校验 ---
def input_date(prompt):
    while True:
        date_str = input(prompt).strip()
        try:
            # 校验日期格式是否为 YYYY-MM-DD
            datetime.strptime(date_str, "%Y-%m-%d")
            return date_str
        except ValueError:
            print("❌ 日期格式错误，请输入正确的格式（如 2026-08-30）！")

def input_text(prompt, max_len=100):
    text = input(prompt).strip()
    if len(text) > max_len:
        print(f"⚠️ 文本过长，已自动截断前 {max_len} 个字符。")
        return text[:max_len]
    return text

# --- 用户认证模块 ---
def register_user(username, password):
    data = load_data()
    if username in data["users"]:
        return False, "❌ 用户名已存在"
    
    data["users"][username] = {
        "pwd": hash_password(password),
        "study": [],
        "sleep": [],
        "mood": [],
        "consume": []
    }
    save_data(data)
    logging.info(f"User registered successfully: {username}")
    return True, "✅ 注册成功"

def login_user(username, password):
    data = load_data()
    u = data["users"].get(username)
    if not u or u["pwd"] != hash_password(password):
        logging.warning(f"Failed login attempt for username: {username}")
        return False, "❌ 账号或密码错误"
    logging.info(f"User logged in: {username}")
    return True, "✅ 登录成功"

# --- 功能模块 ---
# 1. 学习记录
def add_study_record(username):
    date_str = input_date("输入日期(YYYY-MM-DD): ")
    tag = input_text("科目标签(如雅思、编程): ", max_len=20)
    try:
        duration = float(input("学习时长(小时): "))
    except ValueError:
        print("❌ 输入错误：学习时长必须为数字！")
        return
    note = input_text("备注: ", max_len=100)
    
    rec = {"date": date_str, "tag": tag, "duration": duration, "note": note}
    data = load_data()
    data["users"][username]["study"].append(rec)
    save_data(data)
    logging.info(f"[{username}] Added study record: {rec}")
    print("✅ 学习记录已保存")

# 2. 睡眠记录
def add_sleep_record(username):
    date_str = input_date("日期(YYYY-MM-DD): ")
    bed = input_text("上床时间(HH:MM): ", max_len=5)
    wake = input_text("起床时间(HH:MM): ", max_len=5)
    try:
        quality = int(input("睡眠质量1-5(5最好): "))
        if not (1 <= quality <= 5):
            print("❌ 输入错误：评分范围必须在 1 到 5 之间！")
            return
    except ValueError:
        print("❌ 输入错误：质量评分必须为整数！")
        return
        
    rec = {"date": date_str, "bed": bed, "wake": wake, "quality": quality}
    data = load_data()
    data["users"][username]["sleep"].append(rec)
    save_data(data)
    logging.info(f"[{username}] Added sleep record: {rec}")
    print("✅ 睡眠记录已保存")

# 3. 情绪记录
def add_mood_record(username):
    date_str = input_date("日期(YYYY-MM-DD): ")
    try:
        score = int(input("情绪分数1-5(5最好): "))
        if not (1 <= score <= 5):
            print("❌ 输入错误：分数范围必须在 1 到 5 之间！")
            return
    except ValueError:
        print("❌ 输入错误：情绪分数必须为整数！")
        return
    note = input_text("情绪备注: ", max_len=100)
    
    rec = {"date": date_str, "score": score, "note": note}
    data = load_data()
    data["users"][username]["mood"].append(rec)
    save_data(data)
    logging.info(f"[{username}] Added mood record: {rec}")
    print("✅ 情绪记录已保存")

# 4. 消费记录
def add_consume_record(username):
    date_str = input_date("日期(YYYY-MM-DD): ")
    category = input_text("消费分类（餐饮/网购/文具等）: ", max_len=20)
    try:
        money = float(input("消费金额: "))
    except ValueError:
        print("❌ 输入错误：金额必须为数字！")
        return
    note = input_text("备注: ", max_len=100)
    
    rec = {"date": date_str, "category": category, "money": money, "note": note}
    data = load_data()
    data["users"][username]["consume"].append(rec)
    save_data(data)
    logging.info(f"[{username}] Added consume record: {rec}")
    print("✅ 消费记录已保存")

# 5. 生成复盘报告
def generate_analysis_report(username):
    data = load_data()
    udata = data["users"][username]
    study_df = pd.DataFrame(udata["study"])
    sleep_df = pd.DataFrame(udata["sleep"])
    mood_df = pd.DataFrame(udata["mood"])
    consume_df = pd.DataFrame(udata["consume"])

    md_lines = ["# 个人多维生活复盘报告\n"]

    md_lines.append("## 📚 学习统计")
    if not study_df.empty:
        total_h = study_df["duration"].sum()
        tag_group = study_df.groupby("tag")["duration"].sum()
        md_lines.append(f"- 总学习时长：{total_h:.2f} 小时")
        md_lines.append("### 各科目时长")
        for k, v in tag_group.items():
            md_lines.append(f"- {k}: {v:.2f} h")
    else:
        md_lines.append("- 暂无学习数据")

    md_lines.append("\n## 😴 睡眠统计")
    if not sleep_df.empty:
        avg_q = sleep_df["quality"].mean()
        md_lines.append(f"- 平均睡眠质量：{avg_q:.2f} / 5")
    else:
        md_lines.append("- 暂无睡眠数据")

    md_lines.append("\n## 💛 情绪统计")
    if not mood_df.empty:
        avg_mood = mood_df["score"].mean()
        md_lines.append(f"- 平均情绪得分：{avg_mood:.2f} / 5")
    else:
        md_lines.append("- 暂无情绪数据")

    md_lines.append("\n## 💰 消费统计")
    if not consume_df.empty:
        total_money = consume_df["money"].sum()
        cat_group = consume_df.groupby("category")["money"].sum()
        md_lines.append(f"- 总消费：{total_money:.2f} 元")
        md_lines.append("### 分类消费")
        for k, v in cat_group.items():
            md_lines.append(f"- {k}: {v:.2f} 元")
    else:
        md_lines.append("- 暂无消费数据")

    md_lines.append("\n> 积累更多数据后，可进一步扩展分析晚睡、情绪与消费之间的关联。")
    
    report_text = "\n".join(md_lines)
    report_path = os.path.join(DATA_DIR, "report.md")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report_text)
        
    print("\n===== 复盘报告 =====")
    print(report_text)
    print(f"\n📄 报告已成功保存至 {report_path}")
    logging.info(f"[{username}] Generated analysis report")

# 6. 查询全部记录
def query_records(username):
    data = load_data()
    u = data["users"][username]
    print("\n--- 学习记录 ---")
    for s in u["study"]: print(s)
    print("\n--- 睡眠记录 ---")
    for s in u["sleep"]: print(s)
    print("\n--- 情绪记录 ---")
    for s in u["mood"]: print(s)
    print("\n--- 消费记录 ---")
    for s in u["consume"]: print(s)

def main():
    init_data()
    print("==== 个人多维生活行为复盘系统 v1.2 ====")
    while True:
        print("\n1 注册  2 登录  0 退出")
        op = input("请选择: ").strip()
        if op == "0":
            print("感谢使用，再见！")
            break
        elif op == "1":
            un = input("用户名: ").strip()
            pw = input("密码: ").strip()
            if un and pw:
                ok, msg = register_user(un, pw)
                print(msg)
            else:
                print("❌ 用户名和密码不能为空！")
        elif op == "2":
            un = input("用户名: ").strip()
            pw = input("密码: ").strip()
            ok, msg = login_user(un, pw)
            print(msg)
            if ok:
                while True:
                    print(f"\n【用户菜单 - {un}】")
                    print("1 添加学习记录 ｜ 2 添加睡眠记录 ｜ 3 添加情绪记录 ｜ 4 添加消费记录")
                    print("5 查询全部记录 ｜ 6 生成复盘报告 ｜ 9 返回登录页")
                    sub = input("选择: ").strip()
                    if sub == "1": add_study_record(un)
                    elif sub == "2": add_sleep_record(un)
                    elif sub == "3": add_mood_record(un)
                    elif sub == "4": add_consume_record(un)
                    elif sub == "5": query_records(un)
                    elif sub == "6": generate_analysis_report(un)
                    elif sub == "9": break
                    else: print("❌ 无效选择，请重新输入")
        else:
            print("❌ 输入错误，请输入 1、2 或 0")

if __name__ == "__main__":
    main()
