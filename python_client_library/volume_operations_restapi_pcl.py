#! /usr/bin/env python3

"""
ONTAP REST API Python Sample Scripts

This script was developed by NetApp to help demonstrate NetApp technologies. This
script is not officially supported as a standard NetApp product.

Purpose: THE FOLLOWING SCRIPT SHOWS VOLUME OPERATIONS USING REST API PCL

usage: python3 volume_operations_restapi_pcl.py [-h] -c CLUSTER [-u API_USER]
                                        [-p API_PASS]

Copyright (c) 2020 NetApp, Inc. All Rights Reserved.
Licensed under the BSD 3-Clause “New” or Revised” License (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
https://opensource.org/licenses/BSD-3-Clause

"""
import argparse
from getpass import getpass
import logging

from netapp_ontap import config, HostConnection, NetAppRestError
from netapp_ontap.resources import Svm, Volume, Aggregate

def get_size(vol_size):
    """Convert MBs to Byte"""
    tmp = int(vol_size) * 1024 * 1024
    return tmp

def show_aggregate():
    """Lists the Aggregate"""
    print("\n List of Aggregates:- \n")
    try:
        for aggregatelist in Aggregate.get_collection():
            print(aggregatelist.name)
    except NetAppRestError as error:
        print("HTTP Error Code is " % error.http_err_response.http_response.text)
        print("Exception caught :" + str(error))

def show_svm():
    """Lists SVM"""
    print()
    print("Getting SVM Details")
    print("===================")
    try:
        for svm in Svm.get_collection(fields="uuid"):
            print("SVM name:-%s ; SVM uuid:-%s " % (svm.name, svm.uuid))
    except NetAppRestError as error:
        print("HTTP Error Code is " % error.http_err_response.http_response.text)
        print("Exception caught :" + str(error))

def show_volume():
    """Lists Volumes"""
    show_svm()
    print()
    svm_name = input(
        "Enter the SVM from which the Volumes need to be listed:-")
    print()
    print("Getting Volume Details")
    print("======================")
    try:
        for volume in Volume.get_collection(
                **{"svm.name": svm_name}, fields="uuid"):
            print(
                "Volume Name = %s;  Volume UUID = %s" %
                (volume.name, volume.uuid))
    except NetAppRestError as error:
        print("HTTP Error Code is " % error.http_err_response.http_response.text)
        print("Exception caught :" + str(error))

def create_volume():
    """Create volumes"""
    print()
    show_svm()
    print()
    svmname = input(
        "Enter the name of the SVM on which the volume needs to be created:- ")
    dataobj = {}
    tmp1 = {"name": svmname}
    dataobj['svm'] = tmp1
    print()
    show_aggregate()
    print()
    aggrname = input(
        "Enter the name of the Aggregate on which the volume needs to be created:- ")
    tmp2 = [{"name": aggrname}]
    dataobj['aggregates'] = tmp2
    print()
    volname = input("Enter the name of the Volume:- ")
    dataobj['name'] = volname
    print()
    vol_size = input("Enter the size of the Volume in MBs:- ")
    tmp3 = get_size(vol_size)
    dataobj['size'] = tmp3
    print()
    voltype = input("Enter the Volume Type[rw/dp]:- ")
    dataobj['type'] = voltype
    print()
    styletype = input("Enter the Volume Style Type:-[flexvol] ")
    dataobj['style'] = styletype
    print()
    autosize = input("Would you like to enable Autosize (y/n): ")
    if autosize == 'y':
        print("Enter the following Details")
        grow_threshold = input("grow_threshold?:- ")
        maximum = input("maximum?:- ")
        minimum = input("minimum?:- ")
        mode = input("mode?:- ")
        shrink_threshold = input("shrink_threshold?:- ")
        autosizejson = {
            "grow_threshold": grow_threshold,
            "maximum": maximum,
            "minimum": minimum,
            "mode": mode,
            "shrink_threshold": shrink_threshold
        }
        dataobj['autosize'] = autosizejson
    print()

    efficiency = input("Would you like to enable Efficiency (y/n): ")
    if efficiency == 'y':
        print("Enter the following Details")
        compaction = input("compaction?:- ")
        compression = input("compression?:- ")
        cross_volume_dedupe = input("cross_volume_dedupe?:- ")
        dedupe = input("dedupe?:- ")
        policy_name_e = input("Efficiency Policy Name?:- ")
        efficiencyjson = {
            "compaction": compaction,
            "compression": compression,
            "cross_volume_dedupe": cross_volume_dedupe,
            "dedupe": dedupe,
            "policy": {
                "name": policy_name_e
            }
        }
        dataobj['efficiency'] = efficiencyjson

    print()
    encryption = input("Would you like to enable Encryption (y/n): ")
    if encryption == 'y':
        print("Enter the following Details")
        enabled_encry = input("Enable Encryption ?:- ")
        encryptionjson = {
            "enabled": bool(enabled_encry),
            "status": {}
        }
        dataobj['encryption'] = encryptionjson

    print()
    files = input("Would you like to enable Max File Count (y/n): ")
    if files == 'y':
        print("Enter the following Details")
        maximum_files = input("Max File Count?:- ")
        filesjson = {
            "maximum": maximum_files
        }
        dataobj['files'] = filesjson

    print()
    nas = input("Would you like to enable NAS parameters (y/n): ")
    if nas == 'y':
        print("Enter the following Details")
        export_policy_name = input("export_policy_name?:- ")
        path = input("path?:- ")
        security_style = input("security_style?:- ")
        unix_permissions = input("unix_permissions?:- ")
        nasjson = {
            "export_policy":
            {
                "name": export_policy_name
            },
            "path": path,
            "security_style": security_style,
            "unix_permissions": unix_permissions
        }
        dataobj['nas'] = nasjson

    print()
    qos = input("Would you like to enable QoS (y/n): ")
    if qos == 'y':
        print("Enter the following Details")
        max_throughput_iops = input("max_throughput_iops?:- ")
        max_throughput_mbps = input("max_throughput_mbps?:- ")
        min_throughput_iops = input("min_throughput_iops?:- ")
        qosname = input("qosname?:- ")
        qosjson = {"policy":
                   {
                       "max_throughput_iops": max_throughput_iops,
                       "max_throughput_mbps": max_throughput_mbps,
                       "min_throughput_iops": min_throughput_iops,
                       "name": qosname
                   }
                   }
        dataobj['qos'] = qosjson

    print()
    quota = input("Would you like to enable Quota (y/n): ")
    if quota == 'y':
        print("Enter the following Details")
        enable_quota = input("enable_quota?:- ")
        quotajson = {"enabled": bool(enable_quota)}
        dataobj['quota'] = quotajson

    try:
        volume = Volume.from_dict(dataobj)
        if volume.post(poll=True):
            print("SVM  %s created Successfully" % volume.name)
    except NetAppRestError as error:
        print("HTTP Error Code is " % error.http_err_response.http_response.text)
        print("Exception caught :" + str(error))

def patch_volume():
    """Update Volume"""
    print("=============================================")
    print()
    show_volume()
    print()
    vol_name = input(
        "Enter the name  of the volume that needs to be modified:- ")

    try:
        vol = Volume.find(name=vol_name)
    except NetAppRestError as error:
        print("HTTP Error Code is " % error.http_err_response.http_response.text)
        print("Exception caught :" + str(error))

    print()
    nambool = input("Would you like to change the volume name (y/n):- ")
    if nambool == 'y':
        nam = input("Enter the new name of the Volume: ")
        vol.name = nam

    print()
    sizebool = input("Would you like to change the volume size (y/n) :- ")
    if sizebool == 'y':
        vol_size = input("Enter the new size of the Volume: ")
        vol_size_format = get_size(vol_size)
        vol.size = vol_size_format

    print()
    autosizebool = input(
        "Would you like to change the autosize options of the volume (y/n):- ")
    if autosizebool == 'y':
        print("Enter the following Details")
        grow_threshold = input("grow_threshold?:- ")
        maximum = input("maximum?:- ")
        minimum = input("minimum?:- ")
        mode = input("mode?:- ")
        shrink_threshold = input("shrink_threshold?:- ")
        autosizejson = {
            "grow_threshold": grow_threshold,
            "maximum": maximum,
            "minimum": minimum,
            "mode": mode,
            "shrink_threshold": shrink_threshold
        }
        vol.autosize = autosizejson

    print()
    efficiency = input("Would you like to enable Efficiency (y/n): ")
    if efficiency == 'y':
        print("Enter the following Details")
        compaction = input("compaction?:- ")
        compression = input("compression?:- ")
        cross_volume_dedupe = input("cross_volume_dedupe?:- ")
        dedupe = input("dedupe?:- ")
        policy_name_e = input("Efficiency Policy Name?:- ")
        efficiencyjson = {
            "compaction": compaction,
            "compression": compression,
            "cross_volume_dedupe": cross_volume_dedupe,
            "dedupe": dedupe,
            "policy":
            {"name": policy_name_e}
        }
        vol.efficiency = efficiencyjson

    print()
    encryption = input("Would you like to enable Encryption (y/n): ")
    if encryption == 'y':
        print("Enter the following Details")
        enabled_encry = input("Enable Encryption ?:- ")
        encryptionjson = {
            "enabled": bool(enabled_encry),
            "status": {}
        }
        vol.encryption = encryptionjson

    print()
    files = input("Would you like to enable Max File Count (y/n): ")
    if files == 'y':
        print("Enter the following Details")
        maximum_files = input("Max File Count?:- ")
        filesjson = {
            "maximum": maximum_files
        }
        vol.files = filesjson

    print()
    nas = input("Would you like to enable NAS parameters (y/n): ")
    if nas == 'y':
        print("Enter the following Details")
        export_policy_name = input("export_policy_name?:- ")
        path = input("path?:- ")
        security_style = input("security_style?:- ")
        unix_permissions = input("unix_permissions?:- ")
        nasjson = {
            "export_policy":
            {"name": export_policy_name},
            "path": path,
            "security_style": security_style,
            "unix_permissions": unix_permissions
        }
        vol.nas = nasjson

    print()
    qos = input("Would you like to enable QoS (y/n): ")
    if qos == 'y':
        print("Enter the following Details")
        max_throughput_iops = input("max_throughput_iops?:- ")
        max_throughput_mbps = input("max_throughput_mbps?:- ")
        min_throughput_iops = input("min_throughput_iops?:- ")
        qosname = input("qosname?:- ")
        qosjson = {
            "policy":
            {"max_throughput_iops": max_throughput_iops,
             "max_throughput_mbps": max_throughput_mbps,
             "min_throughput_iops": min_throughput_iops,
             "name": qosname
             }
        }
        vol.qos = qosjson

    print()
    quota = input("Would you like to enable Quota (y/n): ")
    if quota == 'y':
        print("Enter the following Details")
        enable_quota = input("enable_quota?:- ")
        quotajson = {
            "enabled": bool(enable_quota)
        }
        vol.quota = quotajson

    try:
        if vol.patch(poll=True):
            print("The Volume  has been updated/patched Successfully")
    except NetAppRestError as error:
        print("HTTP Error Code is " % error.http_err_response.http_response.text)
        print("Exception caught :" + str(error))

def delete_volume():
    """Delete Volume"""
    print("=============================================")
    print()
    show_volume()
    print()
    volname = input("Enter the name of the volume that needs to be Deleted:- ")

    try:
        vol = Volume.find(name=volname)
    except NetAppRestError as error:
        print("HTTP Error Code is " % error.http_err_response.http_response.text)
        print("Exception caught :" + str(error))

    try:
        if vol.delete(poll=True):
            print("Volume  has been deleted Successfully.")
    except NetAppRestError as error:
        print("HTTP Error Code is " % error.http_err_response.http_response.text)
        print("Exception caught :" + str(error))

def clone_volume():
    """Clone volume"""
    print("=============================================")
    print()
    show_volume()
    print()
    print("=============================================")
    print("Please give in the following details for creating clone.")
    print()
    svm_name = input(
        "Enter the NAME of the SVM the parent volume belongs to:-  ")
    svm_uuid = input(
        "Enter the UUID of the SVM the parent volume belongs to [UUID]:- ")
    vol_name = input("Enter the NAME of the volume that needs to be Cloned:- ")
    vol_uuid = input(
        "Enter the UUID of the volume that needs to be Cloned [UUID]:- ")
    print()
    dataobj = {}
    clone_name = input("Enter the name of the clone:- ")

    tmp = {'uuid': svm_uuid}
    dataobj['svm'] = tmp

    dataobj['name'] = clone_name

    clone_volume_json = {
        "is_flexclone": bool("true"),
        "parent_svm":
        {
            "name": svm_name,
            "uuid": svm_uuid
        },
        "parent_volume": {
            "name": vol_name,
            "uuid": vol_uuid
        }
    }

    dataobj['clone'] = clone_volume_json

    try:
        volume = Volume.from_dict(dataobj)
        if volume.post(poll=True):
            print("SVM  %s created Successfully" % volume.name)
    except NetAppRestError as error:
        print("HTTP Error Code is " % error.http_err_response.http_response.text)
        print("Exception caught :" + str(error))

def volume_ops():
    """Volume Operations"""
    print()
    print("THE FOLLOWING SCRIPT SHOWS VOLUME OPERATIONS USING REST API PYTHON CLIENT LIBRARY:- ")
    print("====================================================================================")
    print()
    volumebool = input(
        "What Volume Operation would you like to do? [show/create/update/delete/clone] ")
    if volumebool == 'show':
        show_volume()
    if volumebool == 'create':
        create_volume()
    if volumebool == 'update':
        patch_volume()
    if volumebool == 'delete':
        delete_volume()
    if volumebool == 'clone':
        clone_volume()

def parse_args() -> argparse.Namespace:
    """Parse the command line arguments from the user"""

    parser = argparse.ArgumentParser(
        description="VOLUME OPERATIONS USING REST API PYTHON CLIENT LIBRARY:-")
    parser.add_argument(
        "-c", "--cluster", required=True, help="API server IP:port details"
    )
    parser.add_argument(
        "-u",
        "--api_user",
        default="admin",
        help="API Username")
    parser.add_argument("-p", "--api_pass", help="API Password")
    parsed_args = parser.parse_args()

    # collect the password without echo if not already provided
    if not parsed_args.api_pass:
        parsed_args.api_pass = getpass()

    return parsed_args


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="[%(asctime)s] [%(levelname)5s] [%(module)s:%(lineno)s] %(message)s",
    )
    ARGS = parse_args()
    config.CONNECTION = HostConnection(
        ARGS.cluster,
        username=ARGS.api_user,
        password=ARGS.api_pass,
        verify=False,
    )
    volume_ops()
