from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import UserPreference
from pydantic import BaseModel
from typing import List

router = APIRouter()

class PreferenceCreate(BaseModel):
    category: str
    weight: float = 1.0

class PreferenceResponse(BaseModel):
    id: int
    user_id: int
    category: str
    weight: float

@router.get("/{user_id}", response_model=List[PreferenceResponse])
async def get_user_preferences(user_id: int, db: Session = Depends(get_db)):
    """Get user preferences"""
    try:
        preferences = db.query(UserPreference).filter(
            UserPreference.user_id == user_id
        ).all()
        
        return [
            PreferenceResponse(
                id=pref.id,
                user_id=pref.user_id,
                category=pref.category,
                weight=pref.weight
            )
            for pref in preferences
        ]
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching preferences: {str(e)}")

@router.post("/{user_id}")
async def create_user_preference(
    user_id: int,
    preference: PreferenceCreate,
    db: Session = Depends(get_db)
):
    """Create or update user preference"""
    try:
        # Check if preference already exists
        existing_pref = db.query(UserPreference).filter(
            UserPreference.user_id == user_id,
            UserPreference.category == preference.category
        ).first()
        
        if existing_pref:
            # Update existing preference
            existing_pref.weight = preference.weight
            db.commit()
            return {"message": "Preference updated successfully"}
        else:
            # Create new preference
            new_pref = UserPreference(
                user_id=user_id,
                category=preference.category,
                weight=preference.weight
            )
            db.add(new_pref)
            db.commit()
            return {"message": "Preference created successfully"}
            
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error creating preference: {str(e)}")

@router.delete("/{user_id}/{category}")
async def delete_user_preference(
    user_id: int,
    category: str,
    db: Session = Depends(get_db)
):
    """Delete user preference"""
    try:
        preference = db.query(UserPreference).filter(
            UserPreference.user_id == user_id,
            UserPreference.category == category
        ).first()
        
        if not preference:
            raise HTTPException(status_code=404, detail="Preference not found")
        
        db.delete(preference)
        db.commit()
        
        return {"message": "Preference deleted successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error deleting preference: {str(e)}") 