import logging
import time
from pathlib import Path

from device_info import iosxe_device
from scrapli import Scrape

logging.basicConfig(
    filename=f"{Path(__file__).resolve().parents[0]}/scrape_driver.log", level=logging.DEBUG
)
logger = logging.getLogger("scrapli")

conn = Scrape(**iosxe_device)
conn.open()

print("***** Get Prompt:")
print(conn.channel.get_prompt())

print("***** Show run | i hostname:")
result = conn.channel.send_input("show run | i hostname")
print(result, result.result)

print("***** Clear logging buffer:")
interact = ["clear logg", "Clear logging buffer [confirm]", "", "csr1000v#"]
result = conn.channel.send_inputs_interact(interact)
print(result, result[0].result)

print("***** Disable Paging:")
result = conn.channel.send_input("term length 0")
print(result, result.result)

print("***** Show run:")
result = conn.channel.send_input("show run")
print(result, result.result)

if iosxe_device["keepalive"]:
    print("***** Waiting for keepalive....")
    time.sleep(5)

conn.close()
