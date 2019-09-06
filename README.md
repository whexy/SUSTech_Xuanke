# 选课脚本

[新增] 适配 2019 年度秋季学期选课系统。

[修复] 修复了因递交请求过快导致服务器拒接连接的问题。

[新增] 判断登录是否成功。

[⚠️] 仍然使用 HTTPS，因此有几率无法登陆系统 。

脚本面向湖南强智科技教务系统“教师学生端”下的“选课中心”功能。

**重要提示：代码仅供参考，请自行实现脚本功能，切勿在真实环境中直接运行本脚本。因直接运行本脚本而产生的各种后果请自行承担。**



# 原理阐述

使用 requests 库登录教务系统。再递交选课的 GET 请求，分析系统的返回值，实现循环选课。

使用脚本前，请保证系统已安装 python3.6 以上版本，以及 requests 库。使用脚本时，请保证网络连接通畅，并连接校园内网。

