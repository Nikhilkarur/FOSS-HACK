from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
import models
from database import get_db

router = APIRouter(prefix="/level", tags=["gamification"])

def calculate_level(xp: int) -> int:
    """ Simple leveling formula: Level 1 = 0 XP, Level 2 = 50 XP, Level N = (N-1) * 50 """
    if xp < 0:
        return 1
    return (xp // 50) + 1

@router.get("/{user_id}")
def get_user_level(user_id: int, db: Session = Depends(get_db)):
    """
    Returns the user's current 'Nutrition Level' and XP points based on their healthy food choices.
    """
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Get total healthy scans
    healthy_xp = db.query(models.ScanHistory).filter(
        models.ScanHistory.user_id == user_id,
        models.ScanHistory.verdict == "Healthy"
    ).count() * 10  # 10 XP per healthy scan

    water_xp = db.query(models.ScanHistory).filter(
        models.ScanHistory.user_id == user_id,
        models.ScanHistory.verdict == "Water"
    ).count() * 5  # 5 XP per water log

    # Penalty for unhealthy scans
    unhealthy_penalty = db.query(models.ScanHistory).filter(
        models.ScanHistory.user_id == user_id,
        models.ScanHistory.verdict == "Unhealthy"
    ).count() * 2  # -2 XP per unhealthy scan

    total_xp = healthy_xp + water_xp - unhealthy_penalty
    if total_xp < 0:
        total_xp = 0

    current_level = calculate_level(total_xp)
    xp_for_next_level = current_level * 50
    xp_progress = total_xp % 50

    return {
        "user_id": user_id,
        "level": current_level,
        "total_xp": total_xp,
        "xp_to_next_level": 50 - xp_progress,
        "progress_percentage": round((xp_progress / 50) * 100, 1),
        "breakdown": {
            "healthy_scans_xp": healthy_xp,
            "hydration_xp": water_xp,
            "unhealthy_penalties": -unhealthy_penalty
        }
    }
