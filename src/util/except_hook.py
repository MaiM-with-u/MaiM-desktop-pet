import sys
import traceback

def except_hook(exc_type, exc_value, exc_traceback):
    """全局异常钩子，在控制台输出详细的错误信息"""
    # 获取完整的异常堆栈
    error_msg = "".join(traceback.format_exception(exc_type, exc_value, exc_traceback))
    
    print("\n=== 未处理的异常 ===")
    print(error_msg)
    print("===================\n")

# 安装全局异常钩子
sys.excepthook = except_hook
