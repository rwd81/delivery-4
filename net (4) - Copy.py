from netmiko import ConnectHandler
import time
import os
import difflib


print('')
print ('hello, can we have some details first ')
print('')


device = {
    'device_type': 'cisco_ios',
    'host': '192.168.1.194',              
    'username': 'admin',       # admin
    'password': input('Password? '),      # cisco
    'secret': input('secret password? '),  # cisco
}

os.system('cls') #note to self change to clear for mac terminal, clear the screen

#establishes the connection
connection = ConnectHandler(**device)
connection.enable()

#loading menu
loading_list = ['.', '..', '...', 'Welcome to my script ']
s = 1
e = 0
while e < s:
    for loading in loading_list:
        print(loading, end="\r", flush=True)
        time.sleep(0.5)
    e += 1

#menu options
while True:
    print('\nChoose the option:')
    print(' 1- show interface brief')
    print(' 2- change hostname ')
    print(' 3- Save running-config to local')                  #the file is called configuration
    print(' 4- write memory')                           
    print(' 5- compare startup to running config')             #IMPORTANT pls choose option 3 first
    print(' 6- compare local to running config ')              #IMPORTANT pls choose option 3 first
    print(' 7- create loopback1 interface')
                                                                #task 3
    print(' 8- new interface called fastethernet 0/1')
    print(' 9- configure OSPF')
    print(' 10- exit')

    op = input('Option: ') 
    
    if op == '1':
        # Show IP interface brief
        ip_int_brief = connection.send_command('show ip interface brief')
        print(ip_int_brief)
    
        
    elif op == '2':
        #name
        n = input("Enter new hostname")
        hostname_change = connection.send_config_set([f"hostname {n}"])
        print('changed to', n )
 
    elif op == '3':
        save_config = connection.send_command('show running-config')
        with open("configuration.txt", 'w') as file:
           file.write(save_config)
        print('saved')

    elif op == '4':
        wr = [
            'end',
            'wr'
        ]
        wr_config = connection.send_config_set(wr)
        print(wr_config)

                                                                        #task 2
    elif op == '5':       #startup to running config
        
        #compare running config to startup config
        running_config = connection.send_command("show running-config")
        startup_config = connection.send_command("show startup-config")

        #show specefic section from running config
        hostname_run = connection.send_command("show running | include hostname")
        int_run = connection.send_command("show running | include interface")
        users_run = connection.send_command("show running | include username")

        #startup config
        hostname_start = connection.send_command("show running | include hostname")
        int_start = connection.send_command("show running | include interface")
        users_start = connection.send_command("show running | include username")

        print('---------------------Hostname--------------------------')
        print("Running:", (hostname_run))
        print("Startup:", (hostname_start))

        print('---------------------Interfaces-----------------------')
        print("Running:", (int_run))
        print("Startup:", (int_start))

        print('-------------------- Username-----------------------')
        print("Running:", (users_run))
        print("Startup:", (users_start))

        #optional simple print command I made thats says if they are identical
        basic_R = [                                                     #list of commands basic 
        'show running-config | include hostname',
        'show running-config | include interface',
        'show running-config | include username',
        'show running-config | include vty'
        ]

        basic_R_send = ''
        for commands in basic_R:
            basic_R_send += connection.send_command(commands) + "\n"        #loop, send the commands one after another

        basic_S = [
            'show startup-config | include hostname',
            'show startup-config | include interface',
            'show startup-config | include username',
            'show startup-config | include vty'
            ]

        basic_S_send = ''
        for commands in basic_S:
            basic_S_send += connection.send_command(commands) + "\n"
           
        if basic_R_send != basic_S_send:
            print('they are not the identical')
                
        elif basic_R_send == basic_R_send:
            print('they are the same')

        else: 
            print('')

    elif op == '6':     #compare running config to local config


        from difflib import ndiff                               
                                        
        #running config
        #storing the running config
        running_config = connection.send_command("show running-config").splitlines()  #variable for running config #variable for running config
        
        #open or create the local file as read
        with open("configuration.txt", "r") as file:                                #saved on your configuration locally check current directory
            local_config = file.readlines()

        #comparison                               
        difference = ndiff(running_config, local_config)                            #used diflb librabry for comparison
        
        #loop 
        for dif in difference:                                                       #loops through the differences
           print(dif)


#task 3

    elif op == '7':

        loopbackconfig = [                                                  #list of commands to make loopback1
            'interface loopback1',
            'ip address 10.0.0.1 255.255.255.0',
            'no shutdown'
        ]

        loopback = connection.send_config_set(loopbackconfig)               #sends the lists of commands to the cisco ios

        print(loopback)

        # Show IP interface brief
        ip_int_brief = connection.send_command('show ip interface brief')
        print(ip_int_brief)
    

    elif op == '8':
        interface_config = [
            'interface FastEthernet0/1',
            'ip address 192.168.1.100 255.255.255.0',
            'no shutdown'
        ]

        interface1 = connection.send_config_set(interface_config)

        print(interface1)
        
        # Show IP interface brief
        ip_int_brief = connection.send_command('show ip interface brief')
        print(ip_int_brief)
    
    
    elif op == '9':

        ospf_config = [
           'router ospf 1',
           'router-id 1.1.1.1',
           'network 192.168.1.0 0.0.0.255 area 0'
       ]
        ospf = connection.send_config_set(ospf_config)
        print(ospf)




        ospf1 = connection.send_command('show ip ospf')
        print(ospf1)

    elif op == '10':
        print("Exitting")
        break



    else:
        print("Invalid option. Please try again.")

# Close the connection
connection.disconnect()