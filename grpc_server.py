import grpc
import stocks_pb2
import stocks_pb2_grpc
from concurrent import futures
import socket

class send_stocksServicer(stocks_pb2_grpc.send_stocksServicer):
    def sendStocks(self, request, context):

        # print(request.data)

        num = 0

        message = b'['
        
        for item in request.data:
            num += 1
            message += b'{ "id": ' + bytes(str(item.id), encoding='utf-8') + \
                      b', "time": ' + b'"' + bytes(str(item.time), encoding='utf-8') + b'"' + \
                      b', "price": ' + bytes(str(round(item.price, 2)), encoding='utf-8') + \
                      b', "company": ' + bytes(str(item.company), encoding='utf-8') + \
                      b', "change_percent": ' + bytes(str(round(item.change_percent, 4)), encoding='utf-8') + b'}, '
            
        message = message[: -2]
        message += b']'

        print(message)

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect(('127.0.0.1', 9010))
            s.sendall(message)

        return stocks_pb2.number(num = num)
    
def main():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=5))
    stocks_pb2_grpc.add_send_stocksServicer_to_server(send_stocksServicer(), server=server)
    print('server started')
    server.add_insecure_port('[::]:7000')
    server.start()
    server.wait_for_termination()

main()