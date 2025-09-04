import json, os, asyncio, grpc, redis
from concurrent import futures
from . import fraud_pb2, fraud_pb2_grpc
r = redis.from_url(os.getenv("REDIS_URL","redis://redis:6379/0"), decode_responses=True)
class S(fraud_pb2_grpc.FraudServiceServicer):
    def GetFeatures(self, request, context):
        s = r.get(f"feast:txn:{request.txn_id}")
        if not s: return fraud_pb2.GetFeaturesResponse(txn_id=request.txn_id, velocity_1h=0, mcc_risk=0.0)
        obj = json.loads(s)
        return fraud_pb2.GetFeaturesResponse(txn_id=request.txn_id, velocity_1h=obj["velocity_1h"], mcc_risk=obj["mcc_risk"])
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))
    fraud_pb2_grpc.add_FraudServiceServicer_to_server(S(), server)
    server.add_insecure_port("[::]:50051")
    server.start(); server.wait_for_termination()
if __name__=="__main__": serve()
