import grpc
import stocks_pb2
import stocks_pb2_grpc
from concurrent import futures
import socket

class send_stocksServicer(stocks_pb2_grpc.send_stocksServicer):
    def sendStocks(self, request, context):

        message = b'['
        
        for item in request.data:
            message += b'{ "id": ' + bytes(str(item.id), encoding='utf-8') + \
                      b', time: ' + b'"' + bytes(str(item.time), encoding='utf-8') + b'"' + \
                      b', price: ' + bytes(str(item.price), encoding='utf-8') + \
                      b', company: ' + bytes(str(item.company), encoding='utf-8') + \
                      b', change_percent: ' + bytes(str(item.change_percent), encoding='utf-8') + b'}, '
            
        message = message[: -2]
        message += b']'

        print(1)

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect(('127.0.0.1', 9010))
            s.sendall(message)

        print(2)

        return stocks_pb2.number(num = 0)
    
def main():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=5))
    stocks_pb2_grpc.add_send_stocksServicer_to_server(send_stocksServicer(), server=server)
    print('server started')
    server.add_insecure_port('[::]:7000')
    server.start()
    server.wait_for_termination()

main()