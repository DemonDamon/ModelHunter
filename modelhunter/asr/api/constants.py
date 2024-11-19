# constants.py

class StatusCode:
    """HTTP 状态码"""
    OK = 200
    CREATED = 201
    ACCEPTED = 202
    NO_CONTENT = 204
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    NOT_FOUND = 404
    METHOD_NOT_ALLOWED = 405
    INTERNAL_SERVER_ERROR = 500
    SERVICE_UNAVAILABLE = 503

class Routes:
    """API 路由路径"""
    INFERENCE = "/inference"
    TRAINING = "/training"
    EVALUATION = "/evaluation"
    STATUS = "/status"

class Methods:
    """HTTP 方法"""
    POST = "POST"
    GET = "GET"

class Responses:
    """API 响应消息"""
    STATUS_AVAILABLE = {"status": "Service is available"}
    STATUS_UNAVAILABLE = {"status": "Service is unavailable"}
    SUCCESS = {"result": "success"}
    FAILURE = {"result": "failure"}
    INFERENCE_SUCCESS = {"message": "Inference completed successfully"}
    TRAINING_STARTED = {"message": "Training started successfully"}
    EVALUATION_COMPLETED = {"message": "Evaluation completed successfully"}

class ServerMode:
    """服务器运行模式"""
    INFERENCE = "inference"
    TRAINING = "training"
    EVALUATION = "evaluation"
    STATUS = "status"

class LogMessages:
    """日志信息"""
    START_TRAINING = "Starting training process."
    START_INFERENCE = "Starting inference process."
    START_EVALUATION = "Starting evaluation process."
    ERROR_INFERENCE = "Error during inference process."
    ERROR_TRAINING = "Error during training process."
    ERROR_EVALUATION = "Error during evaluation process."

