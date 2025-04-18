@echo off
chcp 65001 > nul
title 桌宠一键启动工具
color 17  :: 蓝色背景(1)，白色文字(7)

REM 定义颜色变量（调整为适合蓝色背景的颜色）
set ESC=[
set GREEN=%ESC%92m
set BLUE=%ESC%94m
set YELLOW=%ESC%93m
set RED=%ESC%91m
set CYAN=%ESC%96m
set WHITE=%ESC%97m
set RESET=%ESC%0m

REM ==============================================
REM 智能启动脚本（跳过已安装的maim_message）
REM 功能：
REM 1. 仅首次运行时安装maim_message（开发模式）
REM 2. 自动检查并安装其他依赖（如tomli）
REM 3. 更快的启动速度（跳过重复安装）
REM ==============================================

:INIT
echo.
echo %BLUE%[INFO]%RESET%%WHITE% 正在初始化桌宠系统...%RESET%
echo.

REM 检查Python和pip
python --version >nul 2>&1 || (
    echo %RED%[ERROR]%RESET%%WHITE% 未检测到Python或未添加到PATH%RESET%
    pause
    exit /b 1
)

pip --version >nul 2>&1 || (
    echo %RED%[ERROR]%RESET%%WHITE% 未找到pip%RESET%
    pause
    exit /b 1
)

REM ==============================================
REM 依赖安装部分（跳过已安装的maim_message）
REM ==============================================

:CHECK_DEPS
echo %BLUE%[INFO]%RESET%%WHITE% 正在检查依赖...%RESET%

REM 检查并安装requirements.txt中的依赖
if exist "requirements.txt" (
    pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple --quiet
    if %errorlevel% neq 0 (
        echo %RED%[ERROR]%RESET%%WHITE% 依赖安装失败%RESET%
        pause
        exit /b 1
    )
)

REM 检查tomli是否安装（必需）
pip show tomli >nul 2>&1 || (
    echo %BLUE%[INFO]%RESET%%WHITE% 正在安装tomli...%RESET%
    pip install tomli -i https://pypi.tuna.tsinghua.edu.cn/simple --quiet
)

REM ==============================================
REM 仅首次安装maim_message（通过标记文件判断）
REM ==============================================

:CHECK_MAIM_MSG
if not exist "maim_message\pyproject.toml" goto RUN_MAIN

REM 检查标记文件（存在则跳过安装）
if exist ".maim_msg_installed" (
    echo %GREEN%[INFO]%RESET%%WHITE% 检测到maim_message已安装，跳过...%RESET%
    goto RUN_MAIN
)

echo %BLUE%[INFO]%RESET%%WHITE% 首次运行，正在安装maim_message（开发模式）...%RESET%
cd maim_message
pip install -e . --quiet
cd ..
if %errorlevel% neq 0 (
    echo %RED%[ERROR]%RESET%%WHITE% maim_message安装失败%RESET%
    pause
    exit /b 1
)

REM 创建标记文件（避免重复安装）
echo Installed at %date% %time% > .maim_msg_installed
echo %GREEN%[SUCCESS]%RESET%%WHITE% maim_message安装完成%RESET%

REM ==============================================
REM 启动主程序
REM ==============================================

:RUN_MAIN
echo.
echo %BLUE%[INFO]%RESET%%WHITE% 正在启动主程序...%RESET%
python main.py

if %errorlevel% neq 0 (
    echo %RED%[ERROR]%RESET%%WHITE% 主程序异常退出 (代码: %errorlevel%)%RESET%
    pause
    exit /b 1
)

exit /b 0