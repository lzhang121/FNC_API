
@echo off
chcp 65001
REM 进入项目目录
cd /d %~dp0

REM 创建虚拟环境
if not exist venv (
    python -m venv .venv
    echo 虚拟环境已创建
)

REM 激活虚拟环境
call .venv\Scripts\activate.bat
echo 虚拟环境已激活

REM 安装依赖
pip install --upgrade pip
pip install -r requirements.txt

REM 运行 pytest
del /q "C:\Users\linsh\git\FNC_API\allure-results\*.*"
del /q "C:\Users\linsh\git\FNC_API\logs\*.*"
pytest --env=test --alluredir=.\allure-results

REM 启动 Allure 报告
allure serve .\allure-results
pause
