# Using the Lab on Demand to run sample scripts

The NetApp Lab on Demand (LOD) provides a convenient and secure environment for testing your sample Python scripts. Before running the scripts, you'll need to initialize the LOD environment.

## Before you begin

You need a NetApp support account to sign in to the Lab on Demand.

## Steps

1. Using a browser, access the [Lab On Demand](https://labondemand.netapp.com/) web site and sign in using your NetApp account.

2. Click *Full Library* on the left and choose the "Exploring the ONTAP REST API v1.2" Lab-On-Demand solution.

3. Sign in to the `rhel1` machine in the provisioned lab.

4. Clone the `ontap-rest-python` repository using the following command at the CLI prompt:

   `git clone https://github.com/NetApp/ontap-rest-python.git`

5. Initialize the lab environment by running the `lod_init.sh` initialization script provided in the **lod** folder of this repository.

   `./lod/lod_init.sh`

6. If you encounter a *permission denied* error, modify the execute permission using the following command and then rerun the script.

   `chmod 777 ./lod/lod_init.sh`

7. Run the sample scripts in the repository subfolders **examples/python_client_library** and **examples/rest-api**.