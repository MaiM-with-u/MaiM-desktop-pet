import asyncio
from src.core.signals import signals_bus
from maim_message import (
    Router,
    RouteConfig,
    TargetConfig,
)
from config import Config

config = Config()


# 配置路由config 
# 从RouteConfig类构建route_config实例
route_config = RouteConfig( 
    #根据TargetConfig类构建一个合法的route_config
    route_config={
        config.platfrom: TargetConfig( 
            url= config.url ,
            token=None,  # 如果需要token验证则在这里设置
        ),
    #     # 可配置多个平台连接
    #     "platform2": TargetConfig(
    #         url="ws://127.0.0.1:19000/ws",
    #         token="your_auth_token_here",  # 示例：带认证token的连接 
    #     ),
    }
)

# 使用刚刚构建的route_config,从类Router创建路由器实例router
router = Router(route_config)

async def main():
    # 使用实例router的方法注册消息处理器
    router.register_class_handler(message_handler) #message_handler示例见下方

    try:
        # 启动路由器（会自动连接所有配置的平台）
        router_task = asyncio.create_task(router.run())

        # 等待连接建立
        await asyncio.sleep(2)

        # 保持运行直到被中断
        await router_task

    finally:
        print("正在关闭连接...")
        await router.stop()
        print("已关闭所有连接")


async def message_handler(message):
    """
    一个作为示例的消息处理函数
    从mmc发来的消息将会进入此函数
    你需要解析消息，并且向指定平台捏造合适的消息发送
    如将mmc的MessageBase消息转换为onebotV11协议消息发送到QQ
    或者根据其他协议发送到其他平台
    """
    # 提取消息内容
    print(f"收到消息: {message}")
    message_segment = message.get('message_segment', {})
    message_content = str(message_segment.get('data', ""))
    signals_bus.message_received.emit(message_content)  # 跨线程安全


async def delayed_fade_out(bubble, delay):
    """异步延迟执行淡出效果"""
    await asyncio.sleep(delay)
    bubble.fade_out()
