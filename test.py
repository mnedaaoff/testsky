from fastapi import FastAPI
from neo4j import GraphDatabase, RoutingControl

app = FastAPI()

# بيانات الاتصال بقاعدة Neo4j
URI = "neo4j+ssc://6129ee96.databases.neo4j.io"
AUTH = ("6129ee96", "He2eBn-44DObNhfVK5HKIxz1eJREgpR5nuqsfeb73xQ")
DATABASE = "6129ee96"

# إنشاء Driver ثابت للاستخدام لكل الـ requests
driver = GraphDatabase.driver(URI, auth=AUTH)

@app.get("/friends")
def get_all_friends():
    """
    يعرض كل الأشخاص وعلاقاتهم في قاعدة البيانات كـ JSON
    """
    query = """
    MATCH (a:Person)-[:KNOWS]->(friend)
    RETURN a.name AS person, collect(friend.name) AS friends
    ORDER BY a.name
    """
    records, _, _ = driver.execute_query(
        query,
        database_=DATABASE,
        routing_=RoutingControl.READ
    )

    result = []
    for record in records:
        result.append({
            "person": record["person"],
            "friends": record["friends"]
        })
    return result