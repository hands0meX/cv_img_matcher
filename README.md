# opencv 匹配器
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
```shell
python fast_run.py
```
``` matcher.Match函数 指定一张本地目标图片的地址 ```
### 本地环境
0. 前置条件
python>=3.8
1. 安装pip包
```shell
pip install --no-cache-dir -r requirements.txt
```
2. 运行fast_build.py 或 fast_match.py 快速体验
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
docker run -d -p 5000:5000 matcher_flask:v1
```
## 网络层
## 内核 (匹配、特征提取)
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
- [ ] upload上传的图片使用buffer, imread读取buffer直接提取