import pickle
import os
import sys
import random
import threading
import numpy as np
import pexpect
import time
from contextlib import contextmanager
from datetime import datetime
from threading import Thread
from typing import Dict, List
from docker.errors import NotFound

from lid_ds.core.image import StdinCommand, Image, ExecCommand
from lid_ds.sim import gen_schedule_wait_times, Sampler
from lid_ds.utils.docker_utils import get_ip_address
from lid_ds.core.collector.collector import Collector
from lid_ds.core.objects.victim import  kill_child
from lid_ds.utils import log
from lid_ds.core.objects.attacker import ScenarioAttacker
from lid_ds.core.objects.environment import ScenarioEnvironment
from lid_ds.core.objects.normal import ScenarioNormal

MAIN_DIR=os.getcwd()
HOST_IP=""
start_time=""

Scenario_args={
        "normal":          f"--ip {HOST_IP}:32277",

        "CVE_2012_2122":   f"-H {HOST_IP} -P 33060",
        "CVE_2020_1938":   f"-H {HOST_IP} -P 38009",
        "CVE_2022_0543":   f"-H {HOST_IP} -P 63790",
        "CVE_2022_22947":  f"-H {HOST_IP} -P 32277",
        "CVE_2022_22965":  f"-H {HOST_IP} -P 32277",      

        "Redis_unacc":     f"-H {HOST_IP} -P 63790",
        "Mysql_unacc":     f"-H {HOST_IP} -P 33060",

        "Docker_sock":     f"-H {HOST_IP} -P 32277",
        "Host_Mount":      f"-H {HOST_IP} -P 32277",
        "K8s_API":         f"-H {HOST_IP} -P 32277",
    }

SCENARIO_LABEL=dict(zip(Scenario_args.keys(),range(len(Scenario_args))))
ATK_TIMESTAMPS={l:set() for l in SCENARIO_LABEL.values()}

SYSDIG_ARGS='--unbuffered -k "<k8s-api-server>" -K <k8s-profile-path>/client.crt:<k8s-profile-path>/client.key'
SYSDIG_RULE='k8s.pod.label.app in (employee, gateway, kamysql, vulredis) and not evt.type in (futex,stat)'

def _sysdig(buffer_size):
    global start_time
    start_time = datetime.now().strftime("%m%d%H%M%S")
    sysdig_out_path = os.path.join(MAIN_DIR, ".scaps", f'{start_time}.scap')
    return pexpect.spawn(f'sudo sysdig -A -pk -w {sysdig_out_path} -s {buffer_size} {SYSDIG_ARGS} {SYSDIG_RULE}')

@contextmanager
def record_container(do_record, buffer_size=1600):
    if do_record:
        sysdig = _sysdig(buffer_size)
        yield sysdig
        print(f"killing sysdig at {datetime.now()} {time.time_ns()}")
        kill_child(sysdig)
    else:
        yield None

class Action():
    def __init__(self,name,image,cmd_arg,entrypoint=None):
        self.name=name
        self.image=Image(image,
                         init_args="/bin/bash -c \"sleep 3600\"",
                         command=ExecCommand(f"python3 /app/run.py {cmd_arg}"),
                         volumes=[f'{os.path.join(MAIN_DIR,name)}:/app'])

class SpringK8sExploitScenario():
    def __init__(
            self,
            do_record,
            normal_action,
            exploit_actions,
            wait_times,
            recording_time,
            atk_queue,
            storage_services=None,
    ):
        self.do_record=do_record
        self.recording_time=recording_time
        self.atk_queue=atk_queue
        self.logger = log.get_logger("control_script", ScenarioEnvironment().logging_queue)
        self.logging_thread = Thread(target=log.print_logs)
        self.logging_thread.start()
        self.storage_services = storage_services if storage_services else []
        self.normal = ScenarioNormal(normal_action.image, wait_times)
        self.exploit_containers:Dict[str,ScenarioAttacker]={}
        for act in exploit_actions:
            self.exploit_containers[act.name]=ScenarioAttacker(act.image)

    def _container_init(self):
        self.logger.info(f"Starting normal container")
        self.normal.start_containers()
        
        for ec in self.exploit_containers.values():
            self.logger.info("Starting exploit container")
            ec.start_container()

    def execute_exploit(self, atk):
        e_container=self.exploit_containers[atk]
        tss=[]
        for command in e_container.image.commands:
            self.logger.info('Executing the exploit #%s step %s now at %s' % (atk, command.name, time.time()))
            code, out = e_container.container.exec_run(command.command)
            if code!=0:
                self.logger.info(f"Exploit #{atk} failed. Error:")
                for line in out.decode("utf-8").split("\n")[:-1]:
                    self.logger.info(line)
            else:
                for line in out.decode("utf-8").split("\n")[:-1]:
                    self.logger.info(line)
                    tss.append(line)
                assert(len(tss)==2)
                ATK_TIMESTAMPS[SCENARIO_LABEL[atk]].add((tss[0],tss[1],))

    def _warmup(self):
        Collector().set_warmup_end()
        self.logger.info('Start Normal Behaviours for Scenario: ')
        wts = self.normal.start_simulation()
        for t, atk in self.atk_queue:
            threading.Timer(t, self.execute_exploit, args=[atk]).start()
        self.logger.debug("Simulating with %s" % wts)
        time.sleep(4)

    def _recording(self):
        self.logger.info('Start Recording Scenario: ')
        with record_container(self.do_record) as sysdig:
            time.sleep(self.recording_time)

    def _postprocessing(self):
        Collector().write(self.storage_services)

    def _teardown(self):
        for ec in self.exploit_containers.values():
            try:
                ec.teardown()
            except NotFound:
                self.logger.info('Attacker already shut down')
        try:
            self.normal.teardown()
        except NotFound:
            self.logger.info('normal already shut down')
        ScenarioEnvironment().network.remove()


    def __call__(self):
        try:
            self._container_init()
            self.logger.info(f'Simulating Scenario: {0}')
            self._warmup()
            self._recording() 
        finally:
            self._teardown()
        self._postprocessing()
        log.stop()
        self.logging_thread.join()


if __name__ == '__main__':
    recording_time = 60
    ATK_RATIO=0.0

    if ATK_RATIO>0.00001: atk_count=1 if ATK_RATIO*recording_time<1 else int(ATK_RATIO*recording_time)
    else: atk_count=0

    tfl=recording_time/(atk_count+1)
    fluct_sec = 18

    actions=[]
    exps=['Docker_sock', 'CVE_2012_2122', 'CVE_2022_0543', 'CVE_2022_22947' ]
    atk_queue=[]

    if atk_count>0:
        for s in exps:
            actions.append(Action(s,"python-requests",Scenario_args[s]))
            ts=np.linspace(0.1*recording_time, 0.9*recording_time, atk_count+2).tolist()[1:-1]
            ts=[ t+random.uniform(-fluct_sec, fluct_sec) for t in ts ]
            for t in ts:
                atk_queue.append((t, s))

    min_user_count = 10
    max_user_count = 100
    user_count = random.randint(min_user_count, max_user_count)
    wait_times = Sampler("Aug28").ip_timerange_sampling(user_count, recording_time, 5)
    normal_act=Action("normal","python-requests",Scenario_args["normal"])
    normal_act.image=Image("python-requests", command=StdinCommand(""), init_args=f"python3 /app/run.py --ip {HOST_IP}:32277"
                        , volumes=[f'{MAIN_DIR}/1normal:/app'])

    scaping = SpringK8sExploitScenario(
        do_record=True,
        normal_action=normal_act,
        exploit_actions=actions,
        wait_times=wait_times,
        recording_time=recording_time,
        atk_queue=atk_queue
    )
    scaping()
    with open(f'{MAIN_DIR}/.scaps/{start_time}.label','wb') as f:
        pickle.dump(ATK_TIMESTAMPS,f)

