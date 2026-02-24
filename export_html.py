"""从 XMUM 选课系统抓取课程数据，并生成为一个本地 HTML 页面。"""

from typing import Any
import html
import os

from fetch_courses import fetch_course_data


def build_html_page(data: dict[str, Any]) -> str:
    """把抓取到的课程数据，拼成一整段 HTML 字符串。"""
    # 取出不同类型的课程列表和学分信息，如果不存在就用空列表 / 空字典兜底
    available = data.get("available_courses") or []
    registered = data.get("registered_courses") or []
    credit = data.get("credit_info") or {}

    # 使用一个列表一步步累积每一行 HTML，最后再用 join 拼成完整字符串
    parts: list[str] = []

    # HTML 文档头部，包含基础结构和简单的内联样式，方便在浏览器中美观展示
    parts.append("<!DOCTYPE html>")
    parts.append("<html lang='en'>")
    parts.append("<head>")
    parts.append("  <meta charset='utf-8'>")
    parts.append("  <title>XMUM Courses</title>")
    parts.append("  <style>")
    parts.append("    body { font-family: system-ui, -apple-system, BlinkMacSystemFont, sans-serif; margin: 20px; }")
    parts.append("    h1 { margin-bottom: 0.2rem; }")
    parts.append("    h2 { margin-top: 1.6rem; }")
    parts.append("    table { border-collapse: collapse; width: 100%; margin-top: 0.6rem; }")
    parts.append("    th, td { border: 1px solid #ddd; padding: 6px 8px; font-size: 14px; }")
    parts.append("    th { background: #f2f2f2; text-align: left; }")
    parts.append("    tr:nth-child(even) { background: #fafafa; }")
    parts.append("    .number-ok { color: #008000; }")   # 报名人数未超出名额
    parts.append("    .number-over { color: #c08000; }") # 报名人数超过名额
    parts.append("  </style>")
    parts.append("</head>")
    parts.append("<body>")

    # 页面标题
    parts.append("<h1>XMUM Course Overview</h1>")

    # 如果有学分信息，在页面顶部显示一行汇总
    if credit:
        round_text = html.escape(str(credit.get("round", "?")))
        stage_text = html.escape(str(credit.get("stage", "?")))
        chosen = credit.get("chosen_credits", "?")
        max_c = credit.get("max_credits", "?")
        parts.append(
            f"<p><strong>Round:</strong> {round_text} &nbsp; "
            f"<strong>Stage:</strong> {stage_text} &nbsp; "
            f"<strong>Credits:</strong> {chosen}/{max_c}</p>"
        )

    # 已选课程表格
    parts.append("<h2>Registered Courses</h2>")
    if not registered:
        parts.append("<p>No registered courses.</p>")
    else:
        parts.append("<table>")
        parts.append(
            "<tr>"
            "<th>Code</th>"
            "<th>Name</th>"
            "<th>Field</th>"
            "<th>Credit</th>"
            "<th>Quota</th>"
            "<th>Apply</th>"
            "</tr>"
        )
        for c in registered:
            code = html.escape(str(c.get("code", "")))
            name = html.escape(str(c.get("name", "")))
            field = html.escape(str(c.get("field", "")))
            credit_val = html.escape(str(c.get("credit", "")))
            quota_val = c.get("quota", -1)
            applicant_val = c.get("applicant", -1)

            # 根据报名人数是否超过名额，决定 Apply 单元格的样式
            if isinstance(quota_val, int) and isinstance(applicant_val, int) and quota_val >= 0 and applicant_val >= 0:
                if applicant_val > quota_val:
                    apply_class = "number-over"
                else:
                    apply_class = "number-ok"
            else:
                apply_class = "number-over"

            parts.append(
                "<tr>"
                f"<td>{code}</td>"
                f"<td>{name}</td>"
                f"<td>{field}</td>"
                f"<td>{credit_val}</td>"
                f"<td>{quota_val}</td>"
                f"<td class='{apply_class}'>{applicant_val}</td>"
                "</tr>"
            )
        parts.append("</table>")

    # 可选课程表格
    parts.append("<h2>Available Courses</h2>")
    if not available:
        parts.append("<p>No available courses.</p>")
    else:
        parts.append("<table>")
        parts.append(
            "<tr>"
            "<th>Code</th>"
            "<th>Name</th>"
            "<th>Field</th>"
            "<th>Credit</th>"
            "<th>Week</th>"
            "<th>Lecturer</th>"
            "<th>Time/Venue</th>"
            "<th>Quota</th>"
            "<th>Apply</th>"
            "</tr>"
        )
        for c in available:
            code = html.escape(str(c.get("code", "")))
            name = html.escape(str(c.get("name", "")))
            field = html.escape(str(c.get("field", "")))
            credit_val = html.escape(str(c.get("credit", "")))
            week = html.escape(str(c.get("week", "")))
            lecturer = html.escape(str(c.get("lecturer", "")))
            time_venue = html.escape(str(c.get("time_venue", "")))
            quota_val = c.get("quota", -1)
            applicant_val = c.get("applicant", -1)

            # 同样用报名人数和名额比较，决定 Apply 的颜色
            if isinstance(quota_val, int) and isinstance(applicant_val, int) and quota_val >= 0 and applicant_val >= 0:
                if applicant_val > quota_val:
                    apply_class = "number-over"
                else:
                    apply_class = "number-ok"
            else:
                apply_class = "number-over"

            parts.append(
                "<tr>"
                f"<td>{code}</td>"
                f"<td>{name}</td>"
                f"<td>{field}</td>"
                f"<td>{credit_val}</td>"
                f"<td>{week}</td>"
                f"<td>{lecturer}</td>"
                f"<td>{time_venue}</td>"
                f"<td>{quota_val}</td>"
                f"<td class='{apply_class}'>{applicant_val}</td>"
                "</tr>"
            )
        parts.append("</table>")

    parts.append("</body>")
    parts.append("</html>")

    # 返回最终完整的 HTML 字符串
    return "\n".join(parts)


def save_html_file(html_text: str, filename: str = "courses.html") -> str:
    """把生成好的 HTML 字符串写入到本地文件，并返回文件完整路径。"""
    # 这里默认把文件保存在当前项目根目录下
    output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_text)
    return output_path


def main() -> None:
    """脚本入口：抓取课程数据，生成 HTML 页面并保存在本地。"""
    # 第一步：调用已有的抓取函数，拿到结构化的课程数据
    data = fetch_course_data()

    # 第二步：根据数据拼出完整的 HTML 文本
    html_text = build_html_page(data)

    # 第三步：把 HTML 保存到文件，并把文件路径打印出来，方便你打开
    output_path = save_html_file(html_text)
    print(f"HTML 页面已生成：{output_path}")
    print("请在浏览器中打开这个文件，即可查看课程列表。")


if __name__ == "__main__":
    main()

