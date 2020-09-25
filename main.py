from netmiko import ConnectHandler
from pathlib import Path
from datetime import datetime
import os, time, logging,schedule

device = {
    "device_type": "autodetect",
    "host": "10.201.72.28",
    "username": "admin",
    "password": "Tecel2020!"
}
def configure_log():
    """
    Creates the logs subdirectory if there is none, and configures the actual log.
    """
    path = Path(__file__).parent
    path = (path / "logs/").resolve()
    if not Path.exists(path):
        Path.mkdir(path)
    log_filename = datetime.now().strftime('{}/logfile_%H_%M_%S_%d_%m_%Y.log'.format(path))
    print('The data will be stored in: {}'.format(log_filename))
    logging.basicConfig(filename=log_filename, level=logging.INFO)
    logging.getLogger("paramiko").setLevel(logging.WARNING)
    logging.getLogger("schedule").setLevel(logging.WARNING)

def command_cycle():
    """
    Creates a conection handler with netmiko and sends commands to the FTD server
    Then disconnects
    Places all the information gathered into a log file defined by configure_log
    """
    net_connect = ConnectHandler(**device)
    logging.info("*******************************START at {}*******************************".format(datetime.now().strftime("%H_%M_%S_%d_%m_%Y")))
    logging.info(net_connect.send_command("show cpu usage"))
    logging.info(net_connect.send_command("show snmp-server statistics"))
    logging.info(net_connect.send_command_timing("expert"))
    logging.info( net_connect.send_command("top -b -n 1"))
    logging.info("*******************************END*******************************")
    net_connect.disconnect()

if __name__ == "__main__":
    schedule.every(15).minutes.do(command_cycle)
    configure_log()
    command_cycle()
    while True:
        schedule.run_pending()
        time.sleep(1)
    
    
    

   
