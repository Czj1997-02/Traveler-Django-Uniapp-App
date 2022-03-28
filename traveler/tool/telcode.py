def telcode(tel,way):
    # 生成随机码
    import random
    str = ""
    for i in range(6):
        ch = chr(random.randrange(ord('0'), ord('9') + 1))
        str += ch

    # 发送验证码
    import requests
    URL='https://226c2531.bspapp.com/teltest/?a=' + tel + '&b=' + str + '&c=' + way
    shuju = requests.get(URL)

    # 判断状态
    if shuju.status_code == 200:
        return str
    else:
        return 'error'
