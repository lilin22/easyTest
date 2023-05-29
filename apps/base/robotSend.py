from msgSend.models import robotMsgManage
import time,datetime,requests,json
import logging

vst_logger = logging.getLogger("visit")
svr_logger = logging.getLogger("server")

def robotMsg(projectId,content):
    rmm = robotMsgManage.objects.filter(projectId=projectId).last()
    sendStatus = rmm.sendStatus
    if sendStatus == '1':
        robotUrl = rmm.robotUrl
        try:
            headers = {"Content-Type": "application/json"}
            data = {"msgtype": "text", "text": {"content": content}}
            vst_logger.info('发送消息通知请求参数：' + json.dumps(data, ensure_ascii=False))
            res = requests.post(url=robotUrl, headers=headers, data=json.dumps(data, ensure_ascii=False).encode("utf-8"))
            rsn = json.loads(res.text)
            if rsn['errcode'] == 0:
                vst_logger.info('发送消息通知成功，返回内容：' + res.text)
            else:
                vst_logger.error('发送消息通知失败，返回内容：' + res.text)
        except BaseException as msg:
            vst_logger.error('发送消息通知失败：' + msg)