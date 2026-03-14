import os
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from neo4j import GraphDatabase, RoutingControl
from dotenv import load_dotenv
from datetime import datetime
import uuid

load_dotenv()

app = FastAPI(title="Sky Eye OS - Neural Network")

# إعدادات الاتصال
URI = os.getenv("NEO4J_URI")
AUTH = (os.getenv("NEO4J_USER"), os.getenv("NEO4J_PWD"))
DATABASE = os.getenv("NEO4J_DATABASE")

driver = GraphDatabase.driver(URI, auth=AUTH)

# نماذج البيانات
class SkyEyeCommand(BaseModel):
    cypher_query: str
    params: dict = {}
    metadata: dict = {} # لمعرفة مصدر الأمر (صوت، نص، ملف)

# --- محرك العمليات الذكي ---
@app.post("/execute")
def sky_eye_execute(command: SkyEyeCommand):
    """
    المنفذ الرئيسي لأوامر Sky Eye.
    يضيف تلقائياً 'بصمة زمنية' و 'معرف فريد' لكل نود جديد.
    """
    # حماية النظام من الأوامر التدميرية
    forbidden = ["DROP", "DELETE ALL", "TERMINATE"]
    if any(word in command.cypher_query.upper() for word in forbidden):
        raise HTTPException(status_code=403, detail="Security Protocol: Action Denied by Sky Eye.")

    try:
        # دمج بيانات إضافية تلقائياً مثل وقت العملية
        full_params = {
            **command.params,
            "system_time": str(datetime.now()),
            "op_id": str(uuid.uuid4())[:8]
        }

        records, _, _ = driver.execute_query(
            command.cypher_query,
            **full_params,
            database_=DATABASE
        )
        return {"status": "optimized", "data": [dict(r) for r in records]}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# --- نظام البروفايل العميق (Deep Insight v3) ---
@app.get("/stark/intelligence/{entity_name}")
def get_entity_intelligence(entity_name: str):
    """
    يجلب كل شيء: الصور، الملفات، الذكريات، والروابط المخفية.
    """
    query = """
    MATCH (e {name: $name})
    OPTIONAL MATCH (e)-[r]-(related)
    OPTIONAL MATCH (e)-[:HAS_FILE|HAS_IMAGE]->(file)
    RETURN 
        e AS core_data,
        collect(DISTINCT {rel: type(r), target: labels(related)[0], name: related.name}) AS connections,
        collect(DISTINCT {file_url: file.url, desc: file.description, type: file.type}) AS media_vault
    """
    records, _, _ = driver.execute_query(query, name=entity_name, database_=DATABASE)
    
    if not records:
        return {"status": "Unknown", "message": f"Sky Eye has no data on {entity_name}."}

    return {
        "identity": records[0]["core_data"],
        "network": records[0]["connections"],
        "vault": records[0]["media_vault"]
    }

# --- نظام البحث المتعدد (The Eye) ---
@app.get("/sky-eye/vision")
def sky_eye_vision(query_text: str):
    """
    بحث شامل في كل خصائص النودز (الأسماء، النصوص، الأوصاف، التاغات)
    """
    cypher = """
    MATCH (n)
    WHERE any(prop IN keys(n) WHERE toLower(toString(n[prop])) CONTAINS toLower($text))
    RETURN labels(n)[0] AS category, properties(n) AS data
    LIMIT 15
    """
    records, _, _ = driver.execute_query(cypher, text=query_text, database_=DATABASE)
    return {"found_entities": [dict(r) for r in records]}