"""演示如何登录 XMUM 选课系统（只做登录，不抢课）。"""

import os

import requests
from dotenv import load_dotenv

from xmum.constants import LOGIN_PAGE_URL, LOGIN_URL, USER_AGENT, CYAN, GREEN, RED, log


def create_session() -> requests.Session:
    """创建新的 HTTP 会话，并设置浏览器标识。"""
    # 使用 requests.Session 保存 Cookie，后续访问会自动带上登录状态
    session = requests.Session()
    # 设置 User-Agent，伪装成正常浏览器访问
    session.headers["User-Agent"] = USER_AGENT
    return session


def load_credentials() -> tuple[str | None, str | None]:
    """从 .env 文件中读取学号和密码。"""
    # 读取当前目录下的 .env 文件，把里面的配置加载到环境变量中
    load_dotenv()

    # 从环境变量中取出学号和密码
    username = os.getenv("XMU_USERNAME")
    password = os.getenv("XMU_PASSWORD")

    # 如果有任意一个为空，返回 (None, None) 方便后面统一判断
    if not username or not password:
        log("ERROR: 请在 .env 中设置 XMU_USERNAME 和 XMU_PASSWORD", RED)
        return None, None

    return username, password


def login_xmum() -> bool:
    """执行完整的登录流程，并在终端给出反馈。"""
    # 第一步：从 .env 里读取账号密码
    username, password = load_credentials()
    if username is None or password is None:
        # 如果没有正确读取到账号密码，这里直接返回 False 表示登录失败
        return False

    # 第二步：创建一个新的 HTTP 会话
    session = create_session()

    # 第三步：先访问登录页，拿到服务器设置的初始 Cookie
    log(f"Logging in as {username} ...", CYAN)
    session.get(LOGIN_PAGE_URL)

    # 第四步：向登录接口发送 POST 请求，提交账号密码
    response = session.post(
        LOGIN_URL,
        data={
            "username": username,
            "password": password,
            "user_lb": "Student",  # 固定为学生
        },
        allow_redirects=True,  # 允许自动跟随重定向
    )

    # 第五步：根据返回的 HTML 判断是否还停留在登录页
    text = response.text
    is_login_page = "form1" in text and "user_lb" in text

    # 如果依然是登录页，说明登录失败（账号密码错误或其他原因）
    if is_login_page:
        hint = ""
        if "wrong" in text.lower():
            hint = "（用户名或密码错误）"
        log(f"Login FAILED{hint} — 请检查账号密码或稍后再试。", RED)
        return False

    # 如果没有停留在登录页，视为登录成功
    log("Login successful! 已成功登录 XMUM 选课系统。", GREEN)
    return True


def main() -> None:
    """脚本入口：尝试登录，并打印最终结果。"""
    # 调用上面的登录函数，如果返回 True 说明登录成功，否则登录失败
    success = login_xmum()
    if success:
        log("脚本结束：登录流程已完成，可以继续后续操作。", GREEN)
    else:
        log("脚本结束：登录失败，请根据提示检查配置。", RED)


if __name__ == "__main__":
    main()

