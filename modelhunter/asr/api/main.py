from fastapi import FastAPI
import uvicorn
from api.models import training, inference, evaluation  
from components.logger import Logger
from components.system_checker import check_system_status

logger = Logger.get_logger(__name__)

app = FastAPI()

@app.get("/status")#检查系统状态「主要检查gpu和cpu配置」
def get_status():
    try:
        status_info = check_system_status()
        return status_info
    except Exception as e:
        logger.error(f"Error in /status API: {str(e)}")
        return {"status": "error", "message": str(e)}
    
@app.post("/training")#微调训练选项
def trigger_training():
    try:
        training()
        return {"status": "success", "message": "Training started successfully"}
    except Exception as e:
        logger.error(f"Error in /training API: {str(e)}")
        return {"status": "error", "message": str(e)}

@app.post("/inference")#推理训练选项
def trigger_inference():
    try:
        inference()
        return {"status": "success", "message": "Inference started successfully"}
    except Exception as e:
        logger.error(f"Error in /inference API: {str(e)}")
        return {"status": "error", "message": str(e)}

@app.post("/evaluation")#评估训练选项
def trigger_evaluation():
    try:
        evaluation()
        return {"status": "success", "message": "Evaluation started successfully"}
    except Exception as e:
        logger.error(f"Error in /evaluation API: {str(e)}")
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
