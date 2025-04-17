# MaiM 桌宠

<p align="center">
  <a href="https://github.com/Maple127667/MaiM-desktop-pet">
    <img src="img/small_maimai.png" alt="Logo" width="200">
  </a>
</p>

一个基于PyQt5开发的桌宠应用，具有交互式聊天功能和精美的界面设计。其聊天核心为[麦麦Bot](https://github.com/MaiM-with-u/MaiBot)，一款专注于 群组聊天 的赛博网友（非常专注）QQ BOT

## 功能特点

- 可爱的桌宠形象（麦麦）
- 支持实时对话交互
- 支持拖拽移动
- 置顶显示
- 气泡对话框
- 系统托盘支持
- 流畅的动画效果

## 系统要求

- Python 3.8+
- Windows/Linux/MacOS

## 部署步骤

由于依赖于MMC（MaiMBot Core），因此你需要先根据[麦麦Bot部署文档](https://docs.mai-mai.org/manual/deployment/mmc_deploy.html)将MMC启动起来。

启动MMC之后，如果你未修改配置文件，则默认使用`127.0.0.1:8000`作为MMC的websocket地址


1. 克隆项目到本地：
```bash
git clone git@github.com:Maple127667/MaiM-desktop-pet.git
cd MaiM-desktop-pet
```

2. 安装依赖包：

安装依赖前建议使用虚拟环境，此处默认已使用麦麦部署时的虚拟环境。

```bash
pip install -r requirements.txt
```

注意：其中的`maim_message`包需要根据麦麦部署文档中的部署步骤进行安装。

3. 在MMC的配置文件`bot_config.toml`中的[platforms]配置中添加如下内容，并按照MMC部署文档启动MMC
   
```toml
[platforms] # 必填项目，填写每个平台适配器提供的链接
nonebot-qq = "http://127.0.0.1:18002/api/message" # 默认的配置
desktop-pet = "http://127.0.0.1:18003/api/message" # 新添加的本项目的配置
```

## 运行步骤

1. 直接运行主程序：
```bash
python main.py
```

2. 通过系统托盘图标控制：
   - 右键点击托盘图标可以显示/隐藏宠物
   - 选择"退出"可以关闭程序

## 使用说明

- 左键拖拽：移动宠物位置
- 双击宠物：触发互动动作
- 右键点击：打开功能菜单
  - 隐藏：隐藏宠物
  - 聊聊天：打开对话输入框
  - 退出：关闭程序

## 项目结构

```
MaiM-desktop-pet
├─ config.py
├─ data
├─ img
│  ├─ maim.png
│  ├─ maimai.png
│  └─ small_maimai.png
├─ main.py
├─ README.md
├─ src
│  ├─ core
│  │  ├─ chat.py
│  │  ├─ pet.py
│  │  ├─ router.py
│  │  └─ signals.py
│  ├─ features
│  │  ├─ bubble_input.py
│  │  ├─ bubble_menu.py
│  │  ├─ bubble_speech.py
│  │  └─ ScreenshotSelector.py
│  ├─ util
│  │  ├─ image_util.py
│  │  └─ logger.py
│  └─ __init__.py
└─ view
```

## 开发说明

- 使用PyQt5构建GUI界面
- FastAPI提供后端服务
- 多线程处理拖拽和API服务

## 注意事项

- 确保系统已安装Python 3.8或更高版本
- 运行时需要保持网络连接
- 建议使用虚拟环境运行项目