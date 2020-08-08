#!/usr/bin/env python3

import netifaces as netif
import subprocess
import sys
import re

def batctlMeshif(cmdnargs):
  # try to determine batctl version
  lines = call(['batctl', '-v'])
  version = 0
  for line in lines:
    m = re.match(r'batctl debian-([0-9]+)', line)
    if m:
    	version = int(m.group(1))
  if version >= 2020:
    cmd = ['batctl', 'meshif']
  else:
    cmd = ['batctl', '-m']
  cmd.extend(cmdnargs)
  return call(cmd)

def call(cmdnargs):
  try:
    output = subprocess.check_output(cmdnargs, stderr=subprocess.STDOUT)
    lines = output.splitlines()
    lines = [line.decode('utf-8') for line in lines]
  except subprocess.CalledProcessError as err:
    print(err)
  except:
    print(str(sys.exc_info()[0]))
  else:
    return lines

  return []

def merge(a, b):
  if isinstance(a, dict) and isinstance(b, dict):
    d = dict(a)
    d.update({k: merge(a.get(k, None), b[k]) for k in b})
    return d

  if isinstance(a, list) and isinstance(b, list):
    return [merge(x, y) for x, y in itertools.izip_longest(a, b)]

  return a if b is None else b

def getInterfaceMAC(interface):
  try:
    interface = netif.ifaddresses(interface)
    mac = interface[netif.AF_LINK]
    return mac[0]['addr']
  except:
    return None

