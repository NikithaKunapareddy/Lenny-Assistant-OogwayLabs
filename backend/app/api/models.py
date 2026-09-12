from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.llm.factory import llm_manager

router = APIRouter(prefix="/models", tags=["Models"])

class SwitchModelRequest(BaseModel):
    provider: str

@router.get("")
def get_model_status():
    return llm_manager.list_providers()

@router.post("/switch")
def switch_model(req: SwitchModelRequest):
    success = llm_manager.set_active_provider(req.provider)
    if not success:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported model provider '{req.provider}'. Available: {list(llm_manager._providers.keys())}"
        )
    return {
        "status": "success",
        "active_provider": llm_manager.active_provider,
        "message": f"Successfully switched to provider '{llm_manager.active_provider}'"
    }
