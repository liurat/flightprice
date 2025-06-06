# 机场三字代码字典
AIRPORT_CODES = {
    # 华北地区
    "北京": "BJS",  # 北京首都国际机场
    "天津": "TSN",  # 天津滨海国际机场
    "石家庄": "SJW",  # 石家庄正定国际机场
    "太原": "TYN",  # 太原武宿国际机场
    "呼和浩特": "HET",  # 呼和浩特白塔国际机场

    # 华东地区
    "上海": "SHA",  # 上海虹桥国际机场
    "上海浦东": "PVG",  # 上海浦东国际机场
    "南京": "NKG",  # 南京禄口国际机场
    "杭州": "HGH",  # 杭州萧山国际机场
    "宁波": "NGB",  # 宁波栎社国际机场
    "温州": "WNZ",  # 温州龙湾国际机场
    "合肥": "HFE",  # 合肥新桥国际机场
    "福州": "FOC",  # 福州长乐国际机场
    "厦门": "XMN",  # 厦门高崎国际机场
    "济南": "TNA",  # 济南遥墙国际机场
    "青岛": "TAO",  # 青岛流亭国际机场

    # 华南地区
    "广州": "CAN",  # 广州白云国际机场
    "深圳": "SZX",  # 深圳宝安国际机场
    "珠海": "ZUH",  # 珠海金湾国际机场
    "南宁": "NNG",  # 南宁吴圩国际机场
    "海口": "HAK",  # 海口美兰国际机场
    "三亚": "SYX",  # 三亚凤凰国际机场

    # 华中地区
    "武汉": "WUH",  # 武汉天河国际机场
    "长沙": "CSX",  # 长沙黄花国际机场
    "南昌": "KHN",  # 南昌昌北国际机场
    "郑州": "CGO",  # 郑州新郑国际机场

    # 西南地区
    "重庆": "CKG",  # 重庆江北国际机场
    "成都": "CTU",  # 成都双流国际机场
    "贵阳": "KWE",  # 贵阳龙洞堡国际机场
    "昆明": "KMG",  # 昆明长水国际机场
    "拉萨": "LXA",  # 拉萨贡嘎国际机场

    # 西北地区
    "西安": "SIA",  # 西安咸阳国际机场
    "兰州": "LHW",  # 兰州中川国际机场
    "西宁": "XNN",  # 西宁曹家堡国际机场
    "银川": "INC",  # 银川河东国际机场
    "乌鲁木齐": "URC",  # 乌鲁木齐地窝堡国际机场

    # 东北地区
    "沈阳": "SHE",  # 沈阳桃仙国际机场
    "大连": "DLC",  # 大连周水子国际机场
    "长春": "CGQ",  # 长春龙嘉国际机场
    "哈尔滨": "HRB",  # 哈尔滨太平国际机场
}

# 反向映射（三字码到城市名）
CITY_CODES = {code: city for city, code in AIRPORT_CODES.items()}

def get_airport_code(city_name):
    """
    获取城市对应的机场三字代码
    :param city_name: 城市名称
    :return: 机场三字代码，如果未找到则返回None
    """
    return AIRPORT_CODES.get(city_name)

def get_city_name(airport_code):
    """
    获取机场三字代码对应的城市名称
    :param airport_code: 机场三字代码
    :return: 城市名称，如果未找到则返回None
    """
    return CITY_CODES.get(airport_code.upper() if airport_code else None) 