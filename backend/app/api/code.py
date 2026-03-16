from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from app.services.code_runner import CodeRunner
from app.models.user import User
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/code", tags=["code"])

class CodeRunRequest(BaseModel):
    language: str
    code: str
    input_data: str | None = None

class CodeRunResponse(BaseModel):
    output: str
    error: str
    elapsed_time: float
    status: str

@router.post("/run", response_model=CodeRunResponse)
async def run_code(
    request: CodeRunRequest,
    current_user: User = Depends(lambda: None),
):
    """Run code using Judge0 API"""
    
    runner = CodeRunner()
    
    try:
        result = await runner.run(
            language=request.language,
            code=request.code,
            input_data=request.input_data or ""
        )
        
        return CodeRunResponse(**result)
    
    except Exception as e:
        logger.error(f"Code run error: {e}")
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

@router.post("/format")
async def format_code(
    language: str,
    code: str
):
    """Format code"""
    
    runner = CodeRunner()
    formatted = await runner.format_code(language, code)
    
    return {"formatted_code": formatted}