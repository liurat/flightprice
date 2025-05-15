from airport_codes import get_airport_code

# 出发地配置
DEPARTURE_CITY = "广州"  # 例如：上海、北京、广州等
DEPARTURE_CODE = "CAN"

# 目的地配置
DESTINATION_CITY = "昆明"  # 例如：北京、深圳、成都等
DESTINATION_CODE = "KMG"

# 日期配置
DEPARTURE_DATE = "2025-05-28"  # 出发日期，格式：YYYY-MM-DD

# 目标航班配置（可以配置多个航班号）
TARGET_FLIGHTS = [
    "CZ3409"
]

# 爬虫配置
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
}

# 携程机票搜索URL模板
CTRIP_URL_TEMPLATE = "https://flights.ctrip.com/online/list/oneway-{departure}-{destination}?depdate={date}&cabin=y_s_c_f&adult=1&child=0&infant=0"

# 检查配置是否有效
if not DEPARTURE_CODE:
    raise ValueError(f"未找到出发城市 '{DEPARTURE_CITY}' 的机场代码")
if not DESTINATION_CODE:
    raise ValueError(f"未找到目的地城市 '{DESTINATION_CITY}' 的机场代码") 