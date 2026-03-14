# from fastapi import FastAPI

# app = FastAPI()


# @app.get("/")
# def read_root():
#     return {"Hello": "World"}

# @app.get("/friends/{name}")
# def get_friends(name: str):
#     records, _, _ = driver.execute_query(
#         "MATCH (a:Person)-[:KNOWS]->(friend) WHERE a.name = $name "
#         "RETURN friend.name ORDER BY friend.name",
#         name=name,
#         database_="neo4j",
#         routing_=RoutingControl.READ,
#     )

#     return {"friends": [r["friend.name"] for r in records]}
