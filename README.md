# OPENCV 匹配器
<p>
 <img src="https://img.shields.io/badge/python-blue">
 <img src="https://img.shields.io/badge/opencv-red">
 <img src="https://img.shields.io/badge/flask-lightblue">
</p>

## 快速开始
### conda环境
0. 安装conda  
[https://docs.anaconda.com/free/miniconda/](https://docs.anaconda.com/free/miniconda/)
1. conda环境安装
```shell
conda env create -f environment.yml & conda activate matcher
```
2. 在根目录的 static 文件夹创建文件夹foo,并将图片放入 foo 文件夹中
```shell
mkdir -p static/foo
```
3. 体验
- 提取图片特征
```shell
python fast_build.py
```
> --debug 开启debug
> --force 强制覆盖数据集  

- 对图片集匹配并寻找最匹配的图
```shell
python fast_match.py
```
> --debug 开启debug  
> --show 显示匹配图

``` 注意: 存储之后的数据集的特征检测模式必须和匹配时候设置的相同! ```

4. 检测耗时情况
```shell
python -m line_profiler fast_build.lprof
python -m line_profiler fast_match.lprof
```


### 本地环境
1. 安装pip包
```shell
pip install --no-cache-dir -r requirements.txt
```
2. 运行fast_build.py 或 fast_match.py 快速体验
3. 运行本地服务
```shell
python -m server.app
```
### docker环境(flask服务)
0. 安装docker

桌面版：https://www.docker.com/products/docker-desktop  

服务器版：https://docs.docker.com/engine/install/#server
1. 打镜像
```shell
docker build -t matcher_flask:v1 .
```
2. 运行容器
```shell
docker run --rm -d -p 5000:5000 matcher_flask:v1
```
## 网络层
## 内核 (匹配、特征提取)
### 特征检测方法对比:
| - | 时间(ms) | 存储(M) | 图片 | 测试次数 
| - | --- | --- | --- | ---
| SIFT| 1680 ~ 1770 | 12 | 4 | 10
| ORB | 172 ~ 179 | 8.5 | 4 | 10

### 特征匹配方法对比:
| - | 时间(ms) | 图片 | 测试次数 | 精确度 |
| - | --- | --- | --- | -- |
BF | 87 ~ 89 | 4 | 10 | 较FLANN好
FLANN | 135 ~ 147 | 4 | 10 | -

``` 以上是在SIFT特征的KNN匹配情况， FLANN在其他情况未知错误待处理! ```

## 打包/上传
```shell
conda env export --no-builds > environment.yml
pip freeze > requirements.txt
```
## TODO:
- [x] 图片的特征提取并持久化存储与获取
- [x] 增加server包
- [x] docker容器化
- [ ] 本地服务部署, 图片集放OSS存储
- [ ] 功能 toB
- [x] upload上传的图片使用buffer, imread读取buffer直接提取