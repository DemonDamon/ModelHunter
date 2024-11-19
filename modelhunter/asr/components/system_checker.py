import torch
import psutil
from components.logger import Logger

# 实例化日志记录器
logger = Logger.get_logger(__name__)

def check_system_status():
    """
    检查系统状态, 返回GPU或CPU的相关信息。
    """
    try:
        # 检查是否有可用的GPU
        if torch.cuda.is_available():
            gpu_count = torch.cuda.device_count()
            gpu_info = []
            for i in range(gpu_count):
                gpu_info.append({
                    "device_id": i,
                    "name": torch.cuda.get_device_name(i),
                    "total_memory": torch.cuda.get_device_properties(i).total_memory // (1024 ** 2),  # 以MB为单位
                    "free_memory": torch.cuda.memory_reserved(i) // (1024 ** 2),  # 以MB为单位
                    "used_memory": (torch.cuda.memory_allocated(i) // (1024 ** 2)),  # 以MB为单位
                    "gpu_utilization": torch.cuda.get_device_properties(i).multi_processor_count  # 返回处理器数量
                })
            return {"status": "GPU available", "gpu_info": gpu_info}
        
        else:
            # 如果没有GPU可用，返回CPU相关信息
            cpu_usage = psutil.cpu_percent(interval=1)
            cpu_count = psutil.cpu_count(logical=True)
            virtual_memory = psutil.virtual_memory()
            
            cpu_info = {
                "cpu_usage": cpu_usage,
                "cpu_count": cpu_count,
                "total_memory": virtual_memory.total // (1024 ** 2),  # 以MB为单位
                "available_memory": virtual_memory.available // (1024 ** 2),  # 以MB为单位
            }
            return {"status": "CPU only", "cpu_info": cpu_info}

    except Exception as e:
        logger.error(f"Failed to check system status: {str(e)}")
        raise
