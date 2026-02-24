from dotenv import load_dotenv
from bs4 import BeautifulSoup

from xmum.constants import INFO_URL, GREEN, YELLOW, log
from xmum.session import Session


def fetch_personal_info_html() -> str:
    load_dotenv()
    sess = Session()
    sess.ensure_logged_in()                         
    resp = sess._request("GET", INFO_URL)
    if sess._is_login_page(resp.text):
        sess._relogin()
        resp = sess._request("GET", INFO_URL)
    return resp.text


def parse_personal_info(html_text: str) -> list[tuple[str, str]]:
    soup = BeautifulSoup(html_text, "html.parser")
    items: list[tuple[str, str]] = []

    for table in soup.find_all("table"):
        for row in table.find_all("tr"):
            cells = row.find_all(["th", "td"])
            if len(cells) < 2:
                continue
            key = cells[0].get_text(" ", strip=True)
            value = cells[1].get_text(" ", strip=True)
            if key and value:
                items.append((key, value))

    if not items:
        for dl in soup.find_all("dl"):
            dts = dl.find_all("dt")
            dds = dl.find_all("dd")
            for dt, dd in zip(dts, dds):
                key = dt.get_text(" ", strip=True)
                value = dd.get_text(" ", strip=True)
                if key and value:
                    items.append((key, value))

    return items


def pretty_print_info(items: list[tuple[str, str]]) -> None:
    if not items:
        log("未解析到个人信息。", YELLOW)
        return
    log("个人信息：", GREEN)
    for key, value in items:
        print(f"{key}: {value}")


def main() -> None:
    html_text = fetch_personal_info_html()
    items = parse_personal_info(html_text)
    pretty_print_info(items)


if __name__ == "__main__":
    main()
