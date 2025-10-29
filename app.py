from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel
from typing import List, Optional
import os, time, uuid
import boto3
from dotenv import load_dotenv

load_dotenv()
TABLE_NAME = os.getenv("TABLE_NAME")
if not TABLE_NAME:
    raise RuntimeError("TABLE_NAME not set")

dynamo = boto3.resource("dynamodb")
table = dynamo.Table(TABLE_NAME)

app = FastAPI(title="FeatureRequestSerivice")

class CreateRequestIn(BaseModel):
    title: str
    description: Optional[str] = None

class FeatureRequest(BaseModel):
    requestId: str
    clientId: str
    title: str
    description: Optional[str] = None
    likesCount: int
    createdAt: str

def now_iso():
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

@app.post("/requests", response_model=FeatureRequest)
def create_request(body: CreateRequestIn, x_client_id: str = Header(..., alias="X-Client-Id")):
    rid = str(uuid.uuid4())
    item = {
        "requestId": rid,            # PK
        "clientId": x_client_id,     # used by GSIs
        "title": body.title,
        "description": body.description or "",
        "likesCount": 0,
        "createdAt": now_iso(),
    }
    table.put_item(Item=item)
    return item

@app.post("/requests/{request_id}/like", response_model=FeatureRequest)
def like_request(request_id: str, x_client_id: str = Header(..., alias="X-Client-Id")):
    try:
        resp = table.update_item(
            Key={"requestId": request_id},
            UpdateExpression="ADD likesCount :one",
            ExpressionAttributeValues={":one": 1, ":c": x_client_id},
            ConditionExpression="attribute_exists(requestId) AND clientId = :c",
            ReturnValues="ALL_NEW",
        )
        return resp["Attributes"]
    except table.meta.client.exceptions.ConditionalCheckFailedException:
        raise HTTPException(status_code=404, detail="request not found for this client")

@app.get("/requests/top", response_model=List[FeatureRequest])
def get_top_requests(limit: int = 10, x_client_id: str = Header(..., alias="X-Client-Id")):
    resp = table.query(
        IndexName="GSI_TopByLikes",
        KeyConditionExpression="clientId = :c",
        ExpressionAttributeValues={":c": x_client_id},
        ScanIndexForward=False,  # likesCount DESC
        Limit=limit
    )
    return resp.get("Items", [])

@app.get("/requests", response_model=List[FeatureRequest])
def list_requests(limit: int = 50, newest_first: bool = True, x_client_id: str = Header(..., alias="X-Client-Id")):
    resp = table.query(
        IndexName="GSI_Newest",
        KeyConditionExpression="clientId = :c",
        ExpressionAttributeValues={":c": x_client_id},
        ScanIndexForward=not newest_first,  # createdAt DESC if newest_first=True
        Limit=limit
    )
    return resp.get("Items", [])