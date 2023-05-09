import grpc
import stocks_pb2
import stocks_pb2_grpc
from concurrent import futures
import socket

class send_stocksServicer(stocks_pb2_grpc.send_stocksServicer):
    def sendStocks(self, request, context):

        print(request.id, request.time, request.price, request.company, request.change_percent)

        json = {}

        json['id'] = request.id
        json['time'] = request.time
        json['price'] = request.price
        json['company'] = request.company
        json['change_percent'] = request.change_percent

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect(('127.0.0.1', 9010))
            s.sendall(b'{id: ' + bytes(str(json['id']), encoding='utf-8') + 
                      b', time: ' + b'"' + bytes(str(json['time']), encoding='utf-8') + b'"' +
                      b', price: ' + bytes(str(json['price']), encoding='utf-8') + 
                      b', company: ' + bytes(str(json['company']), encoding='utf-8') + 
                      b', change_percent: ' + bytes(str(json['change_percent']), encoding='utf-8') + b'}')

        return stocks_pb2.number(num = 1)
    
def main():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=5))
    stocks_pb2_grpc.add_send_stocksServicer_to_server(send_stocksServicer(), server=server)
    print('server started')
    server.add_insecure_port('[::]:7000')
    server.start()
    server.wait_for_termination()

main()