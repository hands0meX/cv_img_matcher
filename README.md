# opencv 匹配器
<p>
 <img src="https://img.shields.io/badge/python-blue">
 <img src="https://img.shields.io/badge/opencv-red">
 <img src="https://img.shields.io/badge/flask-lightblue">
</p>

## 快速开始
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

## 网络层
## 内核 (匹配、特征提取)
## TODO:
- [x] 图片的特征提取并持久化存储与获取
- [x] 增加server包
- [ ] docker容器化 + k8s集群化
- [ ] 本地服务部署, 图片集放OSS存储
- [ ] 功能 toB