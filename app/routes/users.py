from fastapi import APIRouter, HTTPException
from app.database import get_database

router = APIRouter()


@router.get("/users/count")
async def get_user_count():
    """Returns the total number of documents in the users collection."""
    try:
        db = get_database()
        count = await db["users"].count_documents({})
        return {"count": count}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/users/count/by-college")
async def get_user_count_by_college():
    """Returns user count grouped by the college_show field."""
    try:
        db = get_database()
        pipeline = [
            {
                "$group": {
                    "_id": "$college_show",
                    "count": {"$sum": 1},
                }
            },
            {"$sort": {"count": -1}},
        ]
        cursor = db["users"].aggregate(pipeline)
        results = await cursor.to_list(length=None)
        return [
            {"college": item["_id"], "count": item["count"]}
            for item in results
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
