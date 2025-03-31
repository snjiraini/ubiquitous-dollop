# Dhamana - Tokenizing securities
## _Summary_
Dhamana is a django application leveraging Hedera and hedera-sdk-py sdk for securities tokenization. 
The admin section allows Securities exchanges to:
- Add companies and their industries
- List company bonds and tokenize the bonds on hedera
- Manage investors and create hedera accounts for investors.
- Admin can view pending bids from investors and can Accept or Reject bids.
- Distribute tokens to investors based on successful bids. _[This feature is yet to be implemented]_
- Admin will have ability to distribute coupon payments to token holders _[This feature is yet to be implemented]_

The investor, once setup can:
- List available bonds
- Bid for available bonds and specify amount they wish to invest
- _In future, investor can send tokens to private wallet and trade the tokens on the secondary market_

## Install hedera-sdk-py

```sh
pip install hedera-sdk-py
```

## Install Java JVM
- Make sure to install Hedera Java SDK Git submodule
- Build Hedera Java SDK JAR
- You must make sure JAVA_HOME is set to a JRE/JDK that's >=11. Do a `echo $JAVA_HOME` on Linux/MacOS or `echo %JAVA_HOME%` on Windows to confirm.

MacOS example:

    export JAVA_HOME=/Library/Java/JavaVirtualMachines/jdk-16.0.2.jdk/Contents/Home

Linux example:

    export JAVA_HOME=/usr/lib/jvm/java-16-openjdk-amd64

Windows:

Type to search "advanced system", you should see "View Advanced System settings", click it, then click "Environment Variables..."

On Windows, if you get "no jvm dll found" error, you need to add %JAVA_HOME%/bin/server (i.e. C:\Program Files\Java\jdk-11.0.10\bin\server) to your path.

## Install django

```sh
pip install django
```
## Run the Dhamana django application
Navigate to the corporatebonds folder
```sh
~/myrepos/ubiquitous-dollop/corporatebonds
```
## Build the sqlite database from the django model and create an admin user
```sh
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

## Create .env file to store the Hedera Operator ID and PrivateKeys
Navigate to the corporatebonds folder
```sh
~/ubiquitous-dollop/corporatebonds/bonds
```
```sh
JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
HEDERA_NETWORK=testnet
OPERATOR_ID=0.0.5726xxx
OPERATOR_KEY=30300xxxxxxxxx
SDK_LOG_LEVEL=WARN
```
## Run the app
```sh
python manage.py runserver
```

## Initial app setup
Log in to the admin portal: http://127.0.0.1:8000/admin/
- Create users: Every investor and admin user will need  a username
- Create companies
- Create company bonds to be listed. _A tokenized bond is also created on Hedera testnet on Save_
- Create investors and link them to a username. _A hedera account is created on Save_

## Log in as investor
- Place a bid for the listed bonds.
- Once logged in, Hedera account and balance is displayed
- Investor can view their bids and their status [pending, accepted, rejected]
- 



