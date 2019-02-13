
Konfiguracja wizneta: 
	mac 	--->	0x00 0x08 0xdc 0xab 0xcd 0xef		
	ip 		--->	192.168.1.57							
	maska 	--->  	255.255.255.0							
	brama 	--->  	192.168.1.1
	
Konfiguracja polaczenia z serwerem:
	ip		--->	192.168.1.192
	socekt	--->	5000
	

Po dodaniu bibliotek do projektu w main() programu wywołujemy:
	
	config_wiznet();		
	config_server_param();
	
W pętli głównej programu:
	
	send_to_server();
	
