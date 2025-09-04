import os, requests
AIRBYTE_URL=os.getenv("AIRBYTE_URL","http://localhost:8001/api/v1")
CONNECTION_ID=os.getenv("AIRBYTE_CONNECTION_ID","00000000-0000-0000-0000-000000000000")
def run():
    try:
        r=requests.post(f"{AIRBYTE_URL}/connections/sync", json={"connectionId":CONNECTION_ID}); r.raise_for_status()
    except Exception as e:
        print("airbyte sync failed:", e)
if __name__=="__main__": run()
