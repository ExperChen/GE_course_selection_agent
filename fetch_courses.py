"""只爬取 XMUM 选课系统课程数据，不进行抢课操作。"""

from typing import Any

from dotenv import load_dotenv

from xmum.commands import _fetch_all_courses  # 复用项目内部的分页抓取逻辑
from xmum.constants import BOLD, BLUE, CYAN, GREEN, RED, RESET, YELLOW, log
from xmum.session import Session


def fetch_course_data() -> dict[str, Any]:
    """登录并爬取课程数据，返回结构化结果。"""
    # 第一步：加载 .env，确保账号密码被放入环境变量
    load_dotenv()

    # 第二步：创建 Session，会在第一次请求时自动登录
    sess = Session()

    # 第三步：调用项目内部的 _fetch_all_courses，拿到所有分页的数据
    all_courses, registered, credit_info, first_html = _fetch_all_courses(sess)

    # 第四步：把抓取到的结果整理成一个字典返回，方便后续处理或保存
    return {
        "available_courses": all_courses,
        "registered_courses": registered,
        "credit_info": credit_info,
        "first_page_html": first_html,
    }


def pretty_print_courses(data: dict[str, Any]) -> None:
    """在终端友好地打印课程信息，便于快速查看。"""
    available = data.get("available_courses") or []
    registered = data.get("registered_courses") or []
    credit = data.get("credit_info")

    if credit:
        print(
            f"\n{BOLD}Round: {credit['round']} | "
            f"Stage: {credit['stage']} | "
            f"Credits: {credit['chosen_credits']}/{credit['max_credits']}{RESET}"
        )

    if registered:
        print(f"\n{BOLD}=== Registered Courses ==={RESET}")
        for c in registered:
            print(
                f"  {c['code']} {c['name']} ({c['credit']}cr) "
                f"— {c['applicant']}/{c['quota']} applicants "
                f"[cancel_id={c['cancel_xkid']}]"
            )

    if not available:
        log("No available course data found.", YELLOW)
        return

    print(f"\n{BOLD}=== Available Courses ({len(available)} total) ==={RESET}")
    header = (
        f"{'Code':<8} {'Course Name':<36} {'GE Field':<12} {'Lecturer':<16} "
        f"{'Time/Venue':<26} {'Cr':>3} {'Quota':>6} {'Apply':>6}"
    )
    print(BOLD + header + RESET)
    print("-" * len(header))

    for c in available:
        quota_val = c["quota"]
        applicant_val = c["applicant"]

        if quota_val >= 0 and applicant_val >= 0:
            if applicant_val > quota_val:
                apply_color = YELLOW
            else:
                apply_color = GREEN
        else:
            apply_color = YELLOW

        print(
            f"{c['code']:<8} {c['name']:<36} {c['field']:<12} {c['lecturer']:<16} "
            f"{c['time_venue']:<26} {c['credit']:>3} "
            f"{BLUE}{quota_val:>6}{RESET} "
            f"{apply_color}{applicant_val:>6}{RESET}"
        )

    print()


def main() -> None:
    """脚本入口：只爬取课程数据并打印简单结果。"""
    # 调用上面的函数抓取所有课程数据
    data = fetch_course_data()

    # 在终端打印简单汇总，方便你快速确认爬取是否成功
    pretty_print_courses(data)


if __name__ == "__main__":
    main()
