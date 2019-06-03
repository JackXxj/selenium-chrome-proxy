实现"Selenium + Chrome"使用带用户名密码认证的代理

两份配置文件：
    1、manifest.json文件内容保持不变；
    2、background.js文件的bypassList字段内容修改为具体使用代理ip的网站域名（就是代理ip接口的域名）。