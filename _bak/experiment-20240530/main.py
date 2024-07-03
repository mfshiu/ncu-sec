import json
import multiprocessing
import random
import signal
import threading 
import time
from typing import List

from abdi_config import AbdiConfig
from config import get_config
from counter import ThreadSafeCounter
from holon.HolonicAgent import HolonicAgent
import logit
from stopwatch import Stopwatch
from worker import Worker


logger = logit.get_logger()


class WorkingTest(HolonicAgent):
    def __init__(self, cfg):
        super().__init__(cfg)

        self.sw = Stopwatch()


    def on_connected(self):
        # self.locker = Lock()
        self.subscribe("work_start", topic_handler=self.start_working)
        self.subscribe("job_done", topic_handler=self.handle_job_done)


    def start_working(self, topic:str, payload):
        logger.info(f'\n----- Start Working -----')

        jobs = json.loads(payload.decode())
        workers_count = int(jobs['workers_count'])
        jobs_count = int(jobs['jobs_count'])
        job_load = int(jobs['job_load'])
        logger.info(f"workers_count: {workers_count}, jobs_count: {jobs_count}, job_load: {job_load}")
        
        self.worker_counter = ThreadSafeCounter()
        self.workers: List[Worker] = []
        for _ in range(workers_count):
            a = Worker(self.config, worker_id=self.worker_counter.increment())
            self.workers.append(a)
            a.start()
            
        time.sleep(2)   # Waiting for workers to complete connection.

        # with self.locker:
        self.jobs_status = [0 for _ in range(jobs_count)]
        
        def send_jobs():
            for i in range(0, jobs_count):
                job = json.dumps({
                    "id": i,
                    "load": job_load
                })
                logger.debug(f"publish job: {job}")
                self.publish(topic="job", payload=job)
                # time.sleep(random.randint(100, 3000)/1000)
                time.sleep(.1)
        threading.Thread(target=send_jobs).start()
            
        logger.info(f"Start working at: {Stopwatch.format_time(self.sw.start())}")


    def handle_job_done(self, topic:str, payload):
        job_id = int(payload.decode())
        # with self.locker:
        self.jobs_status[job_id] = 1
        logger.debug(f"jobs_status: {self.jobs_status}")
        logger.info(f"Job {job_id} has been completed.")
        
        if sum(self.jobs_status) == len(self.jobs_status):
            logger.info(f"Elapsed: {Stopwatch.format_elapsed_time(self.sw.stop()[0])}")
            logger.info(f"All the jobs has been completed.")
            self.publish("worker_termination")



if __name__ == '__main__':
    logger.info(f'***** Experiment start *****')

    def signal_handler(signal, frame):
        logger.warning("System was interrupted.")
    signal.signal(signal.SIGINT, signal_handler)

    multiprocessing.set_start_method('spawn')

    WorkingTest(AbdiConfig(get_config())).start(head=False)
