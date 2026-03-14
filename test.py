from neo4j import GraphDatabase, RoutingControl

URI = "neo4j+ssc://6129ee96.databases.neo4j.io" 
AUTH = ("6129ee96", "He2eBn-44DObNhfVK5HKIxz1eJREgpR5nuqsfeb73xQ")

def print_friends(driver, name):
    records, _, _ = driver.execute_query(
        "MATCH (a:Person)-[:KNOWS]->(friend) WHERE a.name = $name "
        "RETURN friend.name ORDER BY friend.name",
        name=name, 
        database_="6129ee96",
        routing_=RoutingControl.READ,
    )
    for record in records:
        print(f"Friend: {record['friend.name']}")

# كود الاتصال
with GraphDatabase.driver(URI, auth=AUTH) as driver:
    try:
        driver.verify_connectivity()
        print("✅ Connection Successful!")
        print_friends(driver, "Stark")
    except Exception as e:
        print(f"❌ Still failing: {e}")



