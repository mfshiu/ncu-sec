import json
import psutil
import random
import signal
import threading
import time

import helper
from holon.HolonicAgent import HolonicAgent
from holon.logistics.request_logistic import RequestLogistic
from holon.logistics.response_logistic import ResponseLogistic

from abdi_config import AbdiConfig
from empty_logistic import EmptyLogistic

logger = helper.get_logger()



class Reporter(HolonicAgent):
    def __init__(self, cfg:AbdiConfig):
        super().__init__(cfg)
        self.total_clients = cfg.get('clients')
        self.start_cpu = cfg.get('system_cpu')
        self.start_memory = cfg.get('system_memory')
        self.elapsed_times = []
        self.testing = True
        self.resource_usages = []


    def on_connected(self):
        self.subscribe("report.elapsed", topic_handler=self.handle_elapsed)
        
        
    def handle_elapsed(self, topic:str, payload):
        elapsed_milis = float(payload.decode('utf-8'))
        print(f"elapsed_milis: {elapsed_milis}, len: {len(self.elapsed_times)}, total_clients: {self.total_clients}")
        self.elapsed_times.append(elapsed_milis)
        if self.total_clients == len(self.elapsed_times):
            avg = sum(self.elapsed_times) / self.total_clients
            print(f"\033[95mAverage elapsed miliseconds:\033[0m {avg}")
            self.testing = False


    def on_interval(self):
        self.system_cpu = psutil.cpu_percent(interval=1)
        self.system_memory = psutil.virtual_memory().used / (1024**2)
        
        if self.testing:
            print(f"\033[90mCPU: {self.system_cpu}%, Memory: {self.system_memory} MB\033[0m")            
            self.resource_usages.append((self.system_cpu, self.system_memory))
        else:
            if self.resource_usages:
                avg_cpu = sum([x[0]-self.start_cpu for x in self.resource_usages]) / len(self.resource_usages)
                avg_mem = sum([x[1]-self.start_memory for x in self.resource_usages]) / len(self.resource_usages)
                self.resource_usages.clear()
                print(f"\033[93mIncreased CPU:\033[0m {avg_cpu}%")
                print(f"\033[93mIncreased Memory:\033[0m {avg_mem} MB")



class Service1(HolonicAgent):
    def __init__(self, cfg:AbdiConfig):
        super().__init__(cfg)
        self.mode = cfg.get('mode')


    def on_connected(self):
        self.response_logistic = EmptyLogistic(agent=self) if self.mode == 'control' else ResponseLogistic(agent=self)
        print(f"response_logistic type: {type(self.response_logistic)}")

        # self.subscribe("service1", topic_handler=self.handle_service)
        self.response_logistic.subscribe("service1", topic_handler=self.handle_service)
        
        
    def handle_service(self, topic:str, payload, request_payload):
        time.sleep(random.uniform(.005, .015))
        
        self.response_logistic.publish('service1.resp', payload, request_payload)
        # self.publish('service1.resp', payload)



class Client1(HolonicAgent):
    def __init__(self, cfg:AbdiConfig):
        super().__init__(cfg)
        self.mode = cfg.get('mode')
        self.total_messages = cfg.get('client_messages')


    def on_connected(self):
        self.start_times = []
        self.elapsed_times = []
        self.request_logistic = EmptyLogistic(self) if self.mode == 'control' else RequestLogistic(self)
        
        # self.subscribe("service1.resp", topic_handler=self.handle_response)
        self.request_logistic.subscribe("service1.resp", topic_handler=self.handle_response)

        def send_requests():
            for i in range(self.total_messages):
                time.sleep(random.uniform(.5, 1.5))
                data = {'agent_id': self.agent_id, 'number': i}
                print(f"\033[34mRequest:\033[0m {self.short_id}-{data['number']}")
                self.start_times.append(time.time())
                # self.publish('service1', json.dumps(data))
                self.request_logistic.publish('service1', json.dumps(data))
            # print(f"start_times: {self.start_times}")
        threading.Thread(target=send_requests).start()
        
        
    def handle_response(self, topic:str, payload):
        # print(f"Client1, handle_response, topic: {topic}, payload: {payload}")
        now = time.time()
        if isinstance(payload, str):
            data = json.loads(payload)
        else:
            data = json.loads(payload.decode('utf-8', 'ignore'))
        if data['agent_id'] != self.agent_id:
            return

        i = data['number']
        print(f"\033[32mResponsed:\033[0m {self.short_id}-{i}")        
        self.elapsed_times.append(now - self.start_times[i])
        if len(self.elapsed_times) == self.total_messages:
            # print(f"len(self.elapsed_times): {len(self.elapsed_times)}, count: {count}, len(self.start_times): {len(self.start_times)}")
            avg_elapsed = sum(self.elapsed_times) / self.total_messages * 1000
            self.publish('report.elapsed', avg_elapsed)
            print(f"\033[93m[{self.short_id}] Average elapsed time:\033[0m {avg_elapsed} ms")



class ManyToOne(HolonicAgent):
    def __init__(self, cfg:AbdiConfig):
        super().__init__(cfg)
        
        self.head_agents.append(Reporter(cfg))
        self.body_agents.append(Service1(cfg))
        for _ in range(cfg.get('clients')):
            self.body_agents.append(Client1(cfg))


 
if __name__ == '__main__':
    logger.info(f'***** ManyToOneControl start *****')

    def signal_handler(signal, frame):
        logger.warning("System was interrupted.")
    signal.signal(signal.SIGINT, signal_handler)

    system_cpu = psutil.cpu_percent(interval=1)
    system_memory = psutil.virtual_memory().used / (1024**2)
    
    # multiprocessing.set_start_method('spawn')
    cfg = AbdiConfig(helper.get_config())
    cfg.set('mode', 'control')
    # cfg.set('mode', 'treatment')
    cfg.set('clients', 100)
    cfg.set('client_messages', 10)
    cfg.set('system_cpu', system_cpu)
    cfg.set('system_memory', system_memory)
    ManyToOne(cfg).start()
    