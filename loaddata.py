import pandas as pd

# Function to load datasets as there are some inconsistencies between file formats
def load_data(path):
    # Set fixed column names to read
    column_names = ['Date_flow', 'start', 'Durat', 'Prot', 'Src_IP_Addr:Port', '->',
       'Dst_IP_Addr:Port', 'Flags', 'Tos', 'Packets', 'Bytes', 'Flows',
       'Label']
    
    df = pd.read_csv(path, names=column_names, header=None, delim_whitespace=True, skiprows=1)
    
    # Split ip_address and port into separate columns
    df[['src_ip','src_port']] = df['Src_IP_Addr:Port'].str.split(":", n=1, expand=True) 
    df[['dst_ip','dst_port']] = df['Dst_IP_Addr:Port'].str.split(":", n=1, expand=True) 
    
    # Drop old columns
    df.drop(columns=['Src_IP_Addr:Port', 'Dst_IP_Addr:Port', '->'], inplace = True) 
    
    return df

# Get sequential IP addresses connected to the host_ip
def load_ip_sequence(df, host_ip):
    
    def filter_ip(row):
        if row['src_ip'] == host_ip:
            return row['dst_ip']
        else:
            return row['src_ip']
    
    # Filter out rows without host_ip
    df = df[['src_ip', 'dst_ip']]
    df = df[(df['src_ip'] == host_ip) | (df['dst_ip'] == host_ip)]
    
    # Filter out host_ip, store the other ip
    df['connected'] = df.apply(filter_ip, axis=1)
    
    return df['connected'].tolist()