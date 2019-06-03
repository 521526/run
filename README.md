### 跑步与签到自动化脚本
- 脚本部分来自于 蛋蛋超人
- 食用方式：linux 服务器上使用crontab这个定时的东西，
    - crontab 一般你买的云服务器上都会安装
    - 如果没安装：安装命令` yum install crontabs`
    - 启动crontab：`systemctl start crond`
    - 使用crontab -e：进入编辑
        - 格式：
        - `*  *  *  *  *  command`
        - `分 时 日 月 周   命令`
        - 直接开花：
        ```
        # 周二到周日 7.05 12.05 21.05 签到
        5 7,12,21 * * 2-7 python /tmp/go/sign_in.py
        # 周二到周日 7.10 跑步
        10 7 * * 2-7 python /tmp/go/run.py
        # 周一 7.10 12.40，21.40 签到
        40 7,12,21 * * 1 python /tmp/go/sign_in.py
        # 周一 7.45跑步
        45 7 * * 1 python /tmp/go/run.py
        ```
    - crontab -l 查看已经开启的任务
- 可能出的问题
    - 时区问题
        - openvz结构vps
        ```
        rm -rf /etc/localtime
        ln -s /usr/share/zoneinfo/Asia/Shanghai /etc/localtime
        
        yum install -y ntp
        ntpdate -d us.pool.ntp.org 
        ntpdate us.pool.ntp.org 
        date -R # 检查时间是否已经同步
        ```
    - 死锁问题
        - 并没解决
