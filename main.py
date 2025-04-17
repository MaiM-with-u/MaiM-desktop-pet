import sys
import threading
from PyQt5.QtWidgets import QApplication

app = QApplication(sys.argv)

def run():
    import asyncio
    from src.core.router import main
    asyncio.run(main())

if __name__ == "__main__":
    # 在单独线程中运行FastAPI
    api_thread = threading.Thread(target=run, daemon=True)
    api_thread.start()
    
    from src.core.pet import chat_pet
    chat_pet.show()
    sys.exit(app.exec_())