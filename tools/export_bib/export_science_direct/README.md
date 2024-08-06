1.安装Google Chrome（链接如下）
https://www.google.com/chrome/

2.Google Chrome打开"设置"--"关于Chrome"--"版本"（比如 113.0.5672.126）

3.安装chromedriver（链接如下）,需要找到对应版本，没有完全一致的就用最接近的，
比如113的Chrome可以用113.0.5672.63的chromedriver。
windows系统都下载chromedriver_win32.zip。
https://npm.taobao.org/mirrors/chromedriver/

4.将chromedriver解压到Google Chrome目录下，windows默认的路径可能如下：
C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe
C:\Program Files\Google\Chrome\Application\chromedriver.exe

5.mac需要把chromedriver放到usr/local/bin目录下，执行下面命令
sudo mv /User/XXX/download /usr/local/bin

6.命令行执行"chromedriver"检查是否安装成功

7.将DownloadScienceBib.py中的executable_path进行修改成对应的目录
executable_path='C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe'

