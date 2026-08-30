import json
import os
import pandas as pd

DATA_FILE = "data.json"

def init_data():
    if not os.path.exists(DATA_FILE):
        init = {"users": {}}
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(init, f, ensure_ascii=False, indent=2)

def load_data():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# 用户注册登录
def register_user(username, password):
    data = load_data()
    if username in data["users"]:
        return False, "用户名已存在"
    data["users"][username] = {
        "pwd": password,
        "study": [],
        "sleep": [],
        "mood": [],
        "consume": []
    }
    save_data(data)
    return True, "注册成功"

def login_user(username, password):
    data = load_data()
    u = data["users"].get(username)
    if not u or u["pwd"] != password:
        return False, "账号或密码错误"
    return True, "登录成功"

# 1.学习记录
def add_study_record(username):
    date_str = input("输入日期(YYYY‑MM‑DD):")
    tag = input("科目标签(如雅思、编程):")
    duration = float(input("学习时长(小时):"))
    note = input("备注:")
    rec = {"date": date_str, "tag": tag, "duration": duration, "note": note}
    data = load_data()
    data["users"][username]["study"].append(rec)
    save_data(data)
    print("✅学习记录已保存")

# 2.睡眠记录
def add_sleep_record(username):
    date_str = input("日期(YYYY‑MM‑DD):")
    bed = input("上床时间(HH:MM):")
    wake = input("起床时间(HH:MM):")
    quality = int(input("睡眠质量1‑5(5最好):"))
    rec = {"date": date_str, "bed": bed, "wake": wake, "quality": quality}
    data = load_data()
    data["users"][username]["sleep"].append(rec)
    save_data(data)
    print("✅睡眠记录已保存")

#3.情绪记录
def add_mood_record(username):
    date_str = input("日期(YYYY‑MM‑DD):")
    score = int(input("情绪分数1‑5(5最好):"))
    note = input("情绪备注:")
    rec = {"date": date_str, "score": score, "note": note}
    data = load_data()
    data["users"][username]["mood"].append(rec)
    save_data(data)
    print("✅情绪记录已保存")

#4.消费记录【新增模块】
def add_consume_record(username):
    date_str = input("日期(YYYY‑MM‑DD):")
    category = input("消费分类（餐饮/网购/文具等）:")
    money = float(input("消费金额："))
    note = input("备注：")
    rec = {"date": date_str, "category": category, "money": money, "note": note}
    data = load_data()
    data["users"][username]["consume"].append(rec)
    save_data(data)
    print("✅消费记录已保存")

#生成复盘报告
def generate_analysis_report(username):
    data = load_data()
    udata = data["users"][username]
    study_df = pd.DataFrame(udata["study"])
    sleep_df = pd.DataFrame(udata["sleep"])
    mood_df = pd.DataFrame(udata["mood"])
    consume_df = pd.DataFrame(udata["consume"])

    md_lines = []
    md_lines.append("# 个人多维生活复盘报告\n")

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
        md_lines.append(f"- 平均睡眠质量：{avg_q:.2f} /5")
    else:
        md_lines.append("- 暂无睡眠数据")

    md_lines.append("\n## 💛 情绪统计")
    if not mood_df.empty:
        avg_mood = mood_df["score"].mean()
        md_lines.append(f"- 平均情绪得分：{avg_mood:.2f} /5")
    else:
        md_lines.append("- 暂无情绪数据")

    md_lines.append("\n## 💰消费统计")
    if not consume_df.empty:
        total_money = consume_df["money"].sum()
        cat_group = consume_df.groupby("category")["money"].sum()
        md_lines.append(f"- 总消费：{total_money:.2f} 元")
        md_lines.append("### 分类消费")
        for k, v in cat_group.items():
            md_lines.append(f"- {k}: {v:.2f} 元")
    else:
        md_lines.append("- 暂无消费数据")

    md_lines.append("\n> 积累更多数据，可扩展分析晚睡、情绪、消费之间关联。")
    report_text = "\n".join(md_lines)
    with open("report.md", "w", encoding="utf-8") as f:
        f.write(report_text)
    print("\n===== 复盘报告 =====")
    print(report_text)
    print("\n📄报告已保存至 report.md")

#查看全部记录
def query_records(username):
    data = load_data()
    u = data["users"][username]
    print("\n---学习记录---")
    for s in u["study"]:print(s)
    print("\n---睡眠记录---")
    for s in u["sleep"]:print(s)
    print("\n---情绪记录---")
    for s in u["mood"]:print(s)
    print("\n---消费记录---")
    for s in u["consume"]:print(s)

def main():
    init_data()
    print("==== 个人多维生活行为复盘系统 ====")
    while True:
        print("\n1 注册  2 登录  0 退出")
        op = input("请选择：")
        if op == "0":
            break
        elif op == "1":
            un = input("用户名：")
            pw = input("密码：")
            ok, msg = register_user(un, pw)
            print(msg)
        elif op == "2":
            un = input("用户名：")
            pw = input("密码：")
            ok, msg = login_user(un, pw)
            print(msg)
            if ok:
                while True:
                    print("\n【用户菜单】")
                    print("1 添加学习记录｜2 添加睡眠记录｜3 添加情绪记录｜4 添加消费记录")
                    print("5 查询全部记录｜6 生成复盘报告｜9 返回登录页")
                    sub = input("选择：")
                    if sub == "1": add_study_record(un)
                    elif sub == "2": add_sleep_record(un)
                    elif sub == "3": add_mood_record(un)
                    elif sub == "4": add_consume_record(un)
                    elif sub == "5": query_records(un)
                    elif sub == "6": generate_analysis_report(un)
                    elif sub == "9": break
            else:
                continue
        else:
            print("输入错误")

if __name__ == "__main__":
    main()
