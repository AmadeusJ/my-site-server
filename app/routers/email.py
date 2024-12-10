from fastapi import APIRouter, HTTPException
from app.mailer import send_email
from app.schemas import EmailSchema, ResponseModel
from app.routers.websocket import manager   # 연결된 웹소켓 관리자


router = APIRouter()

@router.post("/email", response_model=ResponseModel)
async def send_email_route(data: EmailSchema):
    try:
        send_result = send_email(data.email, "Test Email", "This is a test email")
        if send_result:
          status = "success"
          system_message = {
            "sender_id": "jdw",
            "receiver_id": data.user_id,
            "content": "메일 주셔서 감사합니다!\n빠르게 답장드리겠습니다! :D",
            "is_system_message": True,
          }
          message = "이메일 전송 완료"
        else:
            status = "error"
            system_message = {
                "sender_id": "jdw",
                "receiver_id": data.user_id,
                "content": "메일 전송에 실패했습니다..ㅠㅠ\n대신 일반 메세지로 전송됩니다..!",
                "is_system_message": True,
            }
            message = "이메일 전송 실패"
        await manager.send_system_message_to_user(data.user_id, system_message)
        return ResponseModel(status=status, data=system_message, message=message)

    except Exception as e:
        return ResponseModel(status="error", data=None, message=str(e))