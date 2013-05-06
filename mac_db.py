from super_dict import Super_dict
import pickle

class Mac_db(Super_dict):
    def __init__(self):
        Super_dict.__init__(self)
        """
        MAC parse tool
        
        sh mac-add dyn
        vlan   mac address     type    learn     age              ports
        *  124  0021.5e97.7b34   dynamic  Yes         30   Te1/3
        
        2nd variation
        vlan   mac address     type    learn            ports
        *  112  0023.7d35.1470   dynamic  Yes   Po2
        
        3rd variation - 
        vlan   mac address     type        protocols               port
        201    000c.29e0.cd3e   dynamic ip,ipx,assigned,other GigabitEthernet2/9
        
        self.dict_db format is [mac][host_port_vlan][date]    
        (c) 2012, 2013 Intelligent Planet Ltd
        """
        
        self.verbose = 0
        self.space_size = 40
        self.load_file = 'c:/mac_load'
        self.dict_file = 'c:/mac_db'
        
        self.open_dict()
       
        
    def load(self):
        file = open(self.load_file, 'rU')
        host = ''
        for row in file:
            if row:
                if '#' in row: host = row.split('#')[0]
                if '>' in row: host = row.split('>')[0]
                out = row.split()
                port = mac = vlan = ''
                
                if out:    #check for hex encoded data
                    for i in range(2):
                        try: int(out[0])
                        except: 
                            if out: out.pop(0)
                
                    try:
                        mac = out[1]
                        vlan = out[0]
                        port = out[len(out) -1]
                        int(vlan)    #test for number
                    except: 
                        if self.verbose > -1: print 'error', out
                
                entry =  '%s_%s_Vlan%s' % (host, port, vlan)    #host_port_vlan

                if mac and len(mac) == 14 and '.' in mac:
                    if self.verbose > 0: print mac, entry, '\n', row, '\n', out, '\n'
                    try: self.dict_db[mac]
                    except: self.dict_db[mac] = {}
                    self.dict_db[mac][entry] = self.date
  
        
if __name__ == "__main__":
    x = Macs()
    x.load()
    x.save()
    end = raw_input('press enter to exit')
        
        
