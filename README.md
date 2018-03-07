# troubledmonkey

## Requires:

### Python3 Requires

```
pip3
Flask-RESTful
Flask-SQLAlchemy
pymysql
mitmproxy
facebook-wda
```

### external Requires

```
mysql
android sdk
node-js
```

## IOS quick start

1.启动web
cd  Documents/tmonkey
npm run dev

2.启动webdriver
xcodebuild -project /Users/panyeli/Documents/WebDriverAgent/WebDriverAgent.xcodeproj -scheme WebDriverAgentRunner -destination "id=f1360880fddf64d717b303860c09b7a201675e18" test

3.启动mitmdup
cd Documents/troubledmonkey
mitmdump -s "proxy.py --bar"

4.iproxy 8100 8100

5.手机设置代理