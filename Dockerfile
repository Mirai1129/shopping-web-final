# 使用官方的 Python 3.10 镜像作为基础镜像
FROM python:3.10

# 设置工作目录
WORKDIR /app

# 复制当前目录下的所有文件到容器的 /app 目录
COPY . /app

# 安装依赖项
RUN pip install --no-cache-dir -r requirements.txt

# 暴露应用程序运行的端口
EXPOSE 5000

# 定义环境变量
ENV FLASK_APP=run.py
ENV FLASK_RUN_HOST=0.0.0.0

# 启动应用程序
CMD ["python", "run.py"]
