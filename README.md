# shooter_getsubs
# 通过射手API获取电影(中文)字幕的脚本
###### 本脚本基于python3.x

原本想写个PHP版的，卡在不能处理2G以上文件的问题上。后来就写了个python版的出来，才发现github已经有至少4个python版了。配合NAS的下载软件`Transmission`目前使用满意。（也许没什么问题的话懒癌持续发作不会再更新了）


## 用法
### 1.下载两个py文件
### 2.参考以下命令执行
```
python3 getsubs.py 视频文件所在的路径
```    
或者(win已经配置好环境变量或者在linux下) 
```
getsubs.py 视频文件所在的路径
```
例如
```
#getsubs.py e:\download\movies\Finding.Dory.2016.720p.BluRay.x264-WiKi
#done
```
会扫描`e:\download\movies\Finding.Dory.2016.720p.BluRay.x264-WiKi`路径下支持的视频文件格式（`.mp4`,`.wmv`,`.avi`,`.mkv`,`.mpeg`），取文件最大的一个作为目标，计算特征码通过射手的API检索匹配的(中文)字幕文件，一旦找到，下载到当前视频的路径下。
多个字幕文件 会依次命名为 
```
视频文件名.字幕格式扩展名
视频文件名.1.扩展名
视频文件名.2.扩展名
视频文件名.3.扩展名
……
```
### 3.打开支持外挂字幕的播放器，have fun

## 异常处理

### 没有传参或传参路径不存在或路径下没有支持的文件格式

提示对应错误，跳出

### 没有匹配的字幕

提示没找到，跳出

### 提示路径已经扫描过不执行

删除路径下的`subsscaned.mark`文件即可，这个文件是用于标记已经扫描过的路径，减少重复的运算和请求（原本是打算做批量获取的时候用，还没实现）

## 注意事项

* getsubs.py 必须与 mod_shooter.py 放在同一路径下
* 传入的参数必须是一个路径而不是文件，因为考虑到下载通常以文件夹归档而且也不想全部视频文件和字幕都堆列在一个路径下这样太凌乱


## 与transmission配合使用
(待补充)


## 其他

接口返回部分字幕与片源时间轴有偏移(delay),不同的播放器对于这个时间修正的处理和支持还未统一，暂时未想到很好的处理办法。射手播放器使用`.delay`文件标记时间偏移，但我的投影仪并不支持。较理想的做法是对字幕文件用`SrtEditPortable`之类的字幕文件编辑工具进行校准。

在win10与centos7下测试通过。

初次写python，有bug或问题可加我QQ`87898577`或[网易博客](http://snmoney.blog.163.com)交流

###### 衷心感谢射手与各字幕组、字幕提供个人的无私奉献
