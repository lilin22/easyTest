from msgSend.models import msgSendManage
import time,datetime,requests,json
import logging

vst_logger = logging.getLogger("visit")
svr_logger = logging.getLogger("server")

def sendMsg(projectId,content):
    msm = msgSendManage.objects.filter(projectId=projectId).last()
    sendStatus = msm.sendStatus
    if sendStatus == '1':
        accessToken_uri = msm.accessToken_uri
        corpid = msm.corpid
        corpsecret = msm.corpsecret
        accessToken = msm.accessToken
        expires_in = msm.expires_in
        msgSend_uri = msm.msgSend_uri
        touser = msm.touser
        msgtype = msm.msgtype
        agentid = msm.agentid
        safe = msm.safe
        enable_id_trans = msm.enable_id_trans
        enable_duplicate_check = msm.enable_duplicate_check
        duplicate_check_interval = msm.duplicate_check_interval
        updateTime = msm.updateTime
        params = {'corpid': corpid, 'corpsecret': corpsecret}
        nowTimeStamp = time.mktime(datetime.datetime.now().timetuple())
        updateTimeStamp = time.mktime(updateTime.timetuple())
        if (int(nowTimeStamp) - int(updateTimeStamp)) >= int(expires_in / 2):
            res = requests.get(url=accessToken_uri, params=params)
            rsn = json.loads(res.text)
            if rsn['errcode'] == 0:
                vst_logger.info("获取企业微信发消息accessToken成功，返回内容：" + res.text)
                accessToken = rsn['access_token']
                expires_in = rsn['expires_in']
                createTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                updateTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                msgSendManage.objects.filter(projectId=projectId).update(accessToken=accessToken,expires_in=expires_in,createTime=createTime,updateTime=updateTime)
            else:
                vst_logger.error("获取企业微信发消息accessToken失败，返回内容：" + res.text)
        else:
            msgurl = msgSend_uri + '?access_token=' + accessToken
            data = {"touser": touser,
                    "msgtype": msgtype,
                    "agentid": int(agentid),
                    "text": {
                        "content": content
                    },
                    "safe": int(safe),
                    "enable_id_trans": int(enable_id_trans),
                    "enable_duplicate_check": int(enable_duplicate_check),
                    "duplicate_check_interval": int(duplicate_check_interval)
                    }
            vst_logger.info('发送消息通知请求参数：' + json.dumps(data, ensure_ascii=False))
            res = requests.post(url=msgurl, data=json.dumps(data, ensure_ascii=False).encode("utf-8"))
            rsn = json.loads(res.text)
            if rsn['errcode'] == 0:
                vst_logger.info('发送消息通知成功，返回内容：' + res.text)
            else:
                vst_logger.error('发送消息通知失败，返回内容：' + res.text)