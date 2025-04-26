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

## 运行步骤

1. 一键运行主程序：
  修改配置文件config.toml
  运行start.bat文件
2. 手动部署启动程序
  修改配置文件config.toml
```bash
pip install -r requirements.txt
python main.py
```

2. 通过系统托盘图标控制：
   - 右键点击托盘图标可以显示/隐藏宠物
   - 选择"退出"可以关闭程序

## 使用说明

对于桌宠：
- 左键拖拽：移动宠物位置
- 双击宠物：触发互动动作
- 右键点击：打开功能菜单
  - 隐藏：隐藏宠物
  - 截图：截图并且发给mmc
  - 聊聊天：打开对话输入框
  - 退出：关闭程序

右下角任务栏图标：
- 显示宠物：将桌宠显示在面板上
- 显示/隐藏终端: 默认隐藏终端以优化视觉效果，显示终端以方便调试

## 可能会出现的问题

1.Could not load the Qt platform plugin “windows“ in ““ 
  参考https://blog.csdn.net/weixin_46599926/article/details/132576385


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